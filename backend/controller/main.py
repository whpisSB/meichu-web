from flask import jsonify, abort, request
from model.models import Restaurant_Info, Dish_Info, Review, Orders, Order_Dish, db
from controller.user_auth import get_user_id
from flask_jwt_extended import jwt_required
from datetime import datetime

@jwt_required()
def get_restaurant_info(id):
    restaurant = Restaurant_Info.query.filter_by(RestaurantID=id).first()
    if restaurant is None:
        abort(404)
    returned_data = dict()
    returned_data = {
        'id': restaurant.RestaurantID,
        'restaurant': restaurant.RestaurantName,
        'phone': restaurant.PhoneNumber,
        'picture': '/static/cover/' + restaurant.Picture,
        'description': restaurant.Description,
        'rating': restaurant.Rating,
        'open_time': str(restaurant.OpenTime),
        'close_time': str(restaurant.CloseTime)
    }
    dishes = Dish_Info.query.filter_by(RestaurantID=id, Available=True).all()
    returned_data['meals'] = []
    for dish in dishes:
        dish_data = {
            'dish_id': dish.DishID,
            'name': dish.Name,
            'description': dish.Description,
            'combo': dish.Combo,
            'price': dish.Price,
            'rating': dish.Rating,
            'order_times': dish.TimesOfOrder,
            'picture': '/static/dish/' + dish.Picture
        }
        returned_data['meals'].append(dish_data)
    return jsonify(returned_data)

@jwt_required()
def add_review():
    order_id = request.get_json().get('order_id')
    overall_rating = request.get_json().get('overall_rating')
    dishes_rating = request.get_json().get('dishes_rating')
    # print(type(dishes_rating))
    
    order = Orders.query.filter_by(OrderID=order_id).first()
    if order is None:
        return jsonify({'error': 'Order not found'}), 404
    if order.Reviewed:
        return jsonify({'error': 'Order has been reviewed'}), 403
    if not order.Finish:
        return jsonify({'error': 'Order not finished'}), 403
    if order.CustomerID != get_user_id():
        return jsonify({'error': 'It\'s not your order.'}), 403
    
    reviews = []
    for dish in dishes_rating:
        review = Review(OrderID=order_id, DishID=dish['dish_id'], Rating=dish['rating'], Time=datetime.now(), CustomerID=order.CustomerID)
        check_order = Order_Dish.query.filter_by(OrderID=order_id, DishID=dish['dish_id']).first()
        if check_order is None:
            return jsonify({'error': 'Dish not found in order'}), 404
        reviews.append(review)

        # update dish rating
        dish_info = Dish_Info.query.filter_by(DishID=dish['dish_id']).first()
        dish_info.Rating = (dish_info.Rating * dish_info.RatingCnt + dish['rating']) / (dish_info.RatingCnt + 1)
        dish_info.RatingCnt += 1
    reviews.append(Review(OrderID=order_id, DishID=0, Rating=overall_rating, Time=datetime.now(), CustomerID=order.CustomerID)) # overall rating
    # update restaurant rating
    restaurant_info = Restaurant_Info.query.filter_by(RestaurantID=order.RestaurantID).first()
    restaurant_info.Rating = (restaurant_info.Rating * restaurant_info.RatingCnt + overall_rating) \
            / (restaurant_info.RatingCnt + 1)
    restaurant_info.RatingCnt += 1
    order.Reviewed = True
    db.session.add_all(reviews)
    db.session.commit()
    return jsonify({'status': 'success'})

@jwt_required()
def history():
    user_id = get_user_id()
    start_date = datetime(year=datetime.now().year, month=datetime.now().month, day=1)
    orders = db.session.query(Orders, Restaurant_Info) \
        .join(Restaurant_Info, Orders.RestaurantID == Restaurant_Info.RestaurantID, isouter=True) \
        .filter(Orders.CustomerID == user_id) \
        .filter(Orders.OrderTime >= start_date) \
        .filter(Orders.OrderTime <= datetime.now()) \
        .all()
    order_list = []
    for order in orders:
        ordered_dishes = db.session.query(Order_Dish, Dish_Info, Review) \
            .join(Dish_Info, Order_Dish.DishID == Dish_Info.DishID, isouter=True) \
            .join(Review, (Order_Dish.DishID == Review.DishID) & (Order_Dish.OrderID == Review.OrderID), isouter=True) \
            .filter(Order_Dish.OrderID == order[0].OrderID).all()
        overall_rating = Review.query.filter_by(OrderID=order[0].OrderID, DishID=0).first()
        dish_list = [{
            "dish_id": dish[0].DishID,
            "dish_name": dish[1].Name,
            "picture": f'/static/dish/{dish[1].Picture}',
            "number": dish[0].Number,
            "price": dish[1].Price,
            "rating": dish[2].Rating if dish[2] is not None else -1
        } for dish in ordered_dishes]
        order_list.append({
            "order_id": order[0].OrderID,
            'order_time': order[0].OrderTime.strftime("%Y-%m-%d %H:%M:%S"),
            'restaurant_id': order[0].RestaurantID,
            'restaurant_name': order[1].RestaurantName,
            'total_price': order[0].TotalPrice,
            'finished': order[0].Finish,
            'reviewed': order[0].Reviewed,
            'overall_rating': overall_rating.Rating if overall_rating is not None else -1,
            'dishes': dish_list
        })
    return jsonify({'orders': order_list})

def get_restaurant_list():
    restaurants = Restaurant_Info.query.all()
    restaurant_list = []
    for restaurant in restaurants:
        restaurant_list.append({
            'id': restaurant.RestaurantID,
            'restaurant': restaurant.RestaurantName,
            'picture': '/static/cover/' + restaurant.Picture,
            'rating': restaurant.Rating
        })
    return jsonify({'restaurants': restaurant_list})