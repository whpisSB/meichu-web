from flask import request, jsonify, send_from_directory
from random import shuffle
from model.models import Dish_Info, db, Restaurant_Info, Orders, Staff_Info
from flask_jwt_extended import jwt_required
from controller.user_auth import check_permission, get_restaurant_id
from datetime import datetime, timedelta
from sqlalchemy import func
import os

UPLOAD_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in UPLOAD_ALLOWED_EXTENSIONS

@jwt_required()
def add_dish():
    if not check_permission('admin'):
        return jsonify({'error': 'Permission Denied'}), 403
    restaurant_id = request.get_json().get('restaurant_id')
    dish_name = request.get_json().get('name')
    description = request.get_json().get('description')
    combo = request.get_json().get('combo')
    price = request.get_json().get('price')
    filename = request.get_json().get('picture_filename')
    print(combo, flush=True)
    # TODO: check if the file has been uploaded
    picture_exist = True
    path = os.path.join('static', 'dish', filename)
    picture_exist = os.path.isfile(path)
    if not picture_exist:
        return jsonify({'status': "fail", 'error': 'Picture has not been uploaded'})

    new_dish = Dish_Info(
        Name = dish_name, Description = description, 
        Price = price, Picture = filename, 
        RestaurantID = restaurant_id, Combo = combo, 
        Available = True, Rating = 0, 
        RatingCnt = 0, TimesOfOrder = 0
    )
    db.session.add(new_dish)
    db.session.commit()
    return jsonify({'status': 'success'})
    
@jwt_required()
def upload_picture(type):
    if not check_permission('admin'):
        return jsonify({'error': 'Permission Denied'}), 403
    
    restaurant_id = request.form.get('restaurant_id')

    # error handling
    if type not in ['cover', 'dish']:
        return jsonify({'status': 'fail', 'error': 'Invalid type'})
    if not allowed_file(request.files['image'].filename):
        return jsonify({'status': 'fail', 'error': 'Invalid file type'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'status': 'fail', 'error': 'No selected file'})

    filename = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    shuffle(filename)
    filename = ''.join(filename[:10]) + '.' + file.filename.split('.')[-1]
    path = os.path.join('static', type, filename)
    file.save(path)

    # TODO test this part
    if type == 'cover':
        restaurant = Restaurant_Info.query.filter_by(RestaurantID=restaurant_id).first()
        restaurant.Picture = filename
        db.session.commit()
    
    return jsonify({'status': 'success', 'filename': filename})

@jwt_required()
def update_menu():
    if not check_permission('admin'):
        return jsonify({'error': 'Permission Denied'}), 403
    
    dishes = request.get_json().get('available_dish_id')
    dishes.sort()
    head = 0
    
    dish_info = Dish_Info.query.order_by(Dish_Info.DishID).all()
    if dish_info[-1].DishID < dishes[-1]:
        return jsonify({'status': 'fail', 'error': f'Invalid dish id {dishes[-1]} or below'})
    for dish in dish_info:
        if dish.DishID == dishes[head]:
            dish.Available = True
            if head != len(dishes) - 1:
                head += 1
        elif dish.DishID > dishes[head] and head != len(dishes) - 1:
            return jsonify({'status': 'fail', 'error': f'Invalid dish id {dishes[head]}'})
        else:
            dish.Available = False
    db.session.commit()
    return jsonify({'status': 'success'})

@jwt_required()
def get_menus():
    if not check_permission('admin'):
        return jsonify({'error': 'Permission Denied'}), 403
    
    returned_data = []
    restaurants = Restaurant_Info.query.all()
    for restaurant in restaurants:
        restaurant_id = restaurant.RestaurantID
        dishes = Dish_Info.query.filter_by(RestaurantID=restaurant_id).all()
        dish_list = []
        for dish in dishes:
            dish_list.append({
                'dish_id': dish.DishID,
                'dish_name': dish.Name,
                'combo': dish.Combo,
                'price': dish.Price,
                'available': dish.Available,
                'ordered_times': dish.TimesOfOrder,
                'rating': dish.Rating
            })
        returned_data.append({
            'restaurant_id': restaurant_id,
            'restaurant_name': restaurant.RestaurantName,
            "phone": restaurant.PhoneNumber,
            "open_time": str(restaurant.OpenTime)[:-3],
            "close_time": str(restaurant.CloseTime)[:-3],
            "overall_rating": restaurant.Rating,
            'dishes': dish_list
        })
    return jsonify({'restaurants': returned_data})

@jwt_required()
def update_price():
    if not check_permission('admin'):
        return jsonify({'error': 'Permission Denied'}), 403
    dish_id = request.get_json().get('dish_id')
    price = request.get_json().get('updated_price')
    print(dish_id, price)
    dish = Dish_Info.query.filter_by(DishID=dish_id).first()
    if dish is None:
        return jsonify({'status': 'fail', 'error': 'Invalid dish id'})
    dish.Price = price
    db.session.commit()
    return jsonify({'status': 'success'})

@jwt_required()
def get_monthly_report():
    if not check_permission('admin'):
        return jsonify({'error': 'Permission Denied'}), 403
    month = request.get_json().get('month')
    year = request.get_json().get('year')
    now = datetime.now()
    if month < 1 or month > 12 or (year == now.year and month > now.month):
        return jsonify({'status': 'fail', 'error': 'Invalid month'})
    if year > now.year:
        return jsonify({'status': 'fail', 'error': 'Invalid year'})
    if os.path.exists(f"monthly_report/{year}_{month}.csv"):
        return send_from_directory("monthly_report", f"{year}_{month}.csv", as_attachment=True)
    
    result = db.session.query(
        Orders.RestaurantID, 
        Restaurant_Info.RestaurantName,
        func.sum(Orders.TotalPrice).label('total_revenue'),
        func.count(Orders.RestaurantID).label('order_count'),
        Restaurant_Info.Rating.label('restaurant_rating'),) \
    .join(Restaurant_Info, Orders.RestaurantID == Restaurant_Info.RestaurantID, isouter=True) \
    .filter(
        Orders.OrderTime >= datetime(year, month, 1), 
        Orders.OrderTime < datetime(year, month + 1, 1), 
        Orders.Finish == True) \
    .group_by(Orders.RestaurantID) \
    .all()

    result_ = db.session.query(
        Dish_Info.RestaurantID,
        func.avg(Dish_Info.Rating).label('average_rating')
    ).group_by(Dish_Info.RestaurantID).all()

    dishes_rating = {}
    for rating in result_:
        dishes_rating[rating[0]] = rating[1]

    # print(type(result))
    # print(type(result[0]))
    # print(result)
    data = []
    for row in result:
        data.append({
            'restaurant_id': row[0],
            'restaurant_name': row[1],
            'total_revenue': row[2],
            'order_count': row[3],
            'average_order_price': round(row[2] / row[3], 3),
            'restaurant_rating': round(row[4], 1),
            'average_dish_rating': round(dishes_rating[row[0]], 1)
        })
    print(data)

    # geneate monthly report  
    with open(f"monthly_report/{year}_{month}.csv", 'w') as file:
        file.write("Restaurant, Total Revenue, Total Orders, Average Order Price, Restaurant Rating, Average Dish Rating\n")
        for row in data:
            file.write(f"{row['restaurant_name']}, {row['total_revenue']}, {row['order_count']}, {row['average_order_price']}, {row['restaurant_rating']}, {row['average_dish_rating']}\n")
    return send_from_directory("monthly_report", f"{year}_{month}.csv", as_attachment=True)


@jwt_required()
def add_restaurant():
    if not check_permission('admin'):
        return jsonify({'error': 'Permission Denied'}), 403
    restaurant_name = request.get_json().get('restaurant_name')
    phone = request.get_json().get('phone')
    open_time = request.get_json().get('open_time')
    close_time = request.get_json().get('close_time')
    description = request.get_json().get('description')
    new_restaurant = Restaurant_Info(
        RestaurantName = restaurant_name, PhoneNumber = phone,
        OpenTime = timedelta(hours=int(open_time.split(":")[0]), minutes=int(open_time.split(":")[1])), 
        CloseTime = timedelta(hours=int(close_time.split(":")[0]), minutes=int(close_time.split(":")[1])),
        Description = description, Rating = 0,
        RatingCnt = 0, Picture = ''
    )
    db.session.add(new_restaurant)
    db.session.commit()
    return jsonify({'status': 'success', 'restaurant_id': new_restaurant.RestaurantID})


@jwt_required()
def get_monthly_payment_report():
    if not check_permission('admin'):
        return jsonify({'error': 'Permission Denied'}), 403
    month = request.get_json().get('month')
    year = request.get_json().get('year')
    now = datetime.now()
    if month < 1 or month > 12 or (year == now.year and month > now.month):
        return jsonify({'status': 'fail', 'error': 'Invalid month'})
    if year > now.year:
        return jsonify({'status': 'fail', 'error': 'Invalid year'})
    if os.path.exists(f"monthly_report/{year}_{month}_payment.csv"):
        return send_from_directory("monthly_report", f"{year}_{month}_payment.csv", as_attachment=True)

    column = "staff ID, name, on credit(total), order count"
    restaurants = Restaurant_Info.query.all()
    for restaurant in restaurants:
        column += f", on credit({restaurant.RestaurantName}), order count({restaurant.RestaurantName})"
    column += "\n"

    data = {}
    result = db.session.query(
        Staff_Info.StaffID,
        Staff_Info.StaffName,
        func.sum(Orders.TotalPrice).label('total_payment'),
        func.count(Orders.OrderID).label('order_count'),) \
    .join(Orders, Orders.CustomerID == Staff_Info.StaffID, isouter=True) \
    .filter(
        Orders.OrderTime >= datetime(year, month, 1), 
        Orders.OrderTime < datetime(year, month + 1, 1), 
        Orders.Finish == True) \
    .group_by(Staff_Info.StaffID).all()

    for row in result:
        data[row[0]] = [row[0], row[1], row[2], row[3]]
    
    for restaurant in restaurants:
        result = db.session.query(
            Staff_Info.StaffID,
            func.sum(Orders.TotalPrice).label('total_payment'),
            func.count(Orders.OrderID).label('order_count'),) \
        .join(Orders, Orders.CustomerID == Staff_Info.StaffID, isouter=True) \
        .filter(
            Orders.OrderTime >= datetime(year, month, 1), 
            Orders.OrderTime < datetime(year, month + 1, 1), 
            Orders.Finish == True,
            Orders.RestaurantID == restaurant.RestaurantID) \
        .group_by(Staff_Info.StaffID).all()
        for row in result:
            data[row[0]].extend([row[1], row[2]])
    
    with open(f"monthly_report/{year}_{month}_payment.csv", 'w') as file:
        file.write(column)
        for key in data:
            file.write(','.join(map(str, data[key])) + '\n')  

    return send_from_directory("monthly_report", f"{year}_{month}_payment.csv", as_attachment=True)

def reset_paid_flag():
    print("Resetting paid flag")
    staffs = Staff_Info.query.all()
    for staff in staffs:
        staff.Paid = False
    db.session.commit()