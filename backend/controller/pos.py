from flask import request, jsonify
from model.models import db, Dish_Info, Orders, Staff_Info, Order_Dish
from flask_jwt_extended import jwt_required
from controller.user_auth import check_permission, get_restaurant_id
from datetime import datetime

@jwt_required()
def get_menu():
    if not check_permission('restaurant'):
        return jsonify({'error': 'Permission Denied'}), 403
    restaurant_id = get_restaurant_id()
    dishes = Dish_Info.query.filter_by(RestaurantID=restaurant_id).all()
    menu = []
    for dish in dishes:
        menu.append({
            'dish_id': dish.DishID,
            'name': dish.Name,
            'description': dish.Description,
            'combo': dish.Combo,
            'price': dish.Price,
            'rating': dish.Rating,
            "order_times": dish.TimesOfOrder,
            "picture": '/static/dish/' + dish.Picture,
            "available": dish.Available
        })
    return jsonify({'meals': menu})

@jwt_required()
def get_order():
    if not check_permission('restaurant'):
        return jsonify({'error': 'Permission Denied'}), 403
    restaurant_id = get_restaurant_id()
    today = datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, hour=0, minute=0, second=0)
    orders = db.session.query(Orders, Staff_Info) \
        .join(Staff_Info, Orders.CustomerID == Staff_Info.StaffID, isouter=True) \
        .filter(Orders.RestaurantID == restaurant_id) \
        .filter(Orders.OrderTime >= today) \
        .filter(Orders.OrderTime <= datetime.now()).all()
    order_list = []
    for order in orders:
        order_id = order[0].OrderID
        dishes = db.session.query(Order_Dish, Dish_Info) \
            .join(Dish_Info, Order_Dish.DishID == Dish_Info.DishID, isouter=True) \
            .filter(Order_Dish.OrderID == order_id).all()
        dish_list = [{"dish_id": dish[0].DishID, "dish_name": dish[1].Name, \
                      "picture": f'/static/dish/{dish[1].Picture}',"number": dish[0].Number, \
                      "price": dish[1].Price} for dish in dishes]
        # order is a tuple of (Orders, Staff_Info)
        order_list.append({
            'order_id': order[0].OrderID,
            'customer_id': order[0].CustomerID,
            'customer_name': order[1].StaffName,  # Update the column name to Staff_Info.StaffName
            'price': order[0].TotalPrice,
            'order_time': order[0].OrderTime.strftime("%Y-%m-%d %H:%M:%S"),
            'finish': order[0].Finish,
            'dishes': dish_list
        })
    return jsonify({'orders': order_list})

@jwt_required()
def add_order():
    if not check_permission('restaurant'):
        return jsonify({'error': 'Permission Denied'}), 403
    restaurant_id = get_restaurant_id()
    customer_id = request.get_json().get('customer_id')
    dish_list = request.get_json().get('dishes')
    total_price = request.get_json().get('total_price')
    new_order = Orders(
        CustomerID = customer_id, RestaurantID = restaurant_id,
        TotalPrice = total_price, OrderTime = datetime.now(),
        Finish = False, Reviewed = False
    )
    db.session.add(new_order)
    db.session.commit()
    order_id = new_order.OrderID

    dishes = [Order_Dish(OrderID = order_id, DishID = dish["dish_id"], Number = dish["number"]) for dish in dish_list]
    db.session.add_all(dishes)
    db.session.commit()

    return jsonify({'status': 'success', "order_id": order_id})

@jwt_required()
def finish_order(order_id):
    if not check_permission('restaurant'):
        return jsonify({'status': 'error', 'error': 'Permission Denied'}), 403
    restaurant_id = get_restaurant_id()
    order = Orders.query.filter_by(OrderID=order_id).first()
    if not order:
        return jsonify({'status': 'error', 'error': 'Order not found'}), 404
    if str(order.RestaurantID) != str(restaurant_id):
        return jsonify({'status': 'error', 'error': 'Permission Denied, restaurant id not matched'}), 403
    if order.Finish:
        return jsonify({'status': 'error', 'error': 'Order has already finished'})
    order.Finish = True
    ordered_dish = Order_Dish.query.filter_by(OrderID=order_id).all()
    for dish in ordered_dish:
        dish_info = Dish_Info.query.filter_by(DishID=dish.DishID).first()
        dish_info.TimesOfOrder += dish.Number
    db.session.commit()
    return jsonify({'status': 'success'})

@jwt_required()
def get_worker_info(id):
    if not check_permission('restaurant'):
        return jsonify({'error': 'Permission Denied'}), 403
    worker = Staff_Info.query.filter_by(StaffID=id).first()
    if not worker:
        return jsonify({'error': 'Worker not found'}), 404
    return jsonify({
        'id': worker.StaffID,
        'name': worker.StaffName,
        'phone': worker.PhoneNumber
    })

@jwt_required()
def check_paid(customer_id):
    if not check_permission('restaurant'):
        return jsonify({'error': 'Permission Denied'}), 403
    staff = Staff_Info.query.filter_by(StaffID=customer_id).first()
    if not staff:
        return jsonify({'error': 'Invalid Customer ID'}), 404
    return jsonify({'customer_id': staff.StaffID, 'paid': staff.Paid})