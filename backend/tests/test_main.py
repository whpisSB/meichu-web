import pytest
from controller.user_auth import generate_token
from model.models import *
from os.path import exists
from datetime import datetime

def test_main_get_restaurant_list(client):
    token = generate_token(100004, 'worker')
    response = client.get('/main/restaurant_list', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    assert "restaurants" in response.json
    assert len(response.json["restaurants"]) == 3
    assert "id" in response.json["restaurants"][0]
    assert "restaurant" in response.json["restaurants"][0]
    assert "rating" in response.json["restaurants"][0]
    assert "picture" in response.json["restaurants"][0]

def test_main_get_menu_success(client, session):
    token = generate_token(100004, 'worker')
    response = client.get('/main/restaurant/1', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    restaurant_info = session.query(Restaurant_Info).filter_by(RestaurantID=1).first()
    assert "id" in response.json
    assert response.json["id"] == 1
    assert "restaurant" in response.json
    assert response.json["restaurant"] == restaurant_info.RestaurantName
    assert "phone" in response.json
    assert response.json["phone"] == restaurant_info.PhoneNumber
    assert "picture" in response.json
    assert response.json["picture"] == "/static/cover/" + restaurant_info.Picture
    assert "description" in response.json
    assert response.json["description"] == restaurant_info.Description
    assert "rating" in response.json
    assert response.json["rating"] == restaurant_info.Rating
    assert "open_time" in response.json
    assert int(response.json["open_time"].split(':')[0]) == restaurant_info.OpenTime.seconds // 3600
    assert int(response.json["open_time"].split(':')[1]) == restaurant_info.OpenTime.seconds % 3600 // 60
    assert "close_time" in response.json
    assert int(response.json["close_time"].split(':')[0]) == restaurant_info.CloseTime.seconds // 3600
    assert int(response.json["close_time"].split(':')[1]) == restaurant_info.CloseTime.seconds % 3600 // 60
    assert "meals" in response.json
    dishes = session.query(Dish_Info).filter_by(RestaurantID=1, Available=True).all()
    assert len(response.json["meals"]) == len(dishes)

    # Check the picture
    assert exists("./static/cover/" + restaurant_info.Picture)
    for dish in dishes:
        assert exists("./static/dish/" + dish.Picture)
    
def test_main_get_menu_invalid_restaurant(client):
    token = generate_token(100004, 'worker')
    response = client.get('/main/restaurant/100', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 404

@pytest.mark.parametrize("customer_id", [
    (100004),
    (100005),
    (100006)
])
def test_main_get_history_success(client, session, customer_id):
    token = generate_token(customer_id, 'worker')
    response = client.get('/main/history', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    assert "orders" in response.json
    startdate = datetime(datetime.now().year, datetime.now().month, 1, 0, 0, 0)
    orders = session.query(Orders) \
        .filter_by(CustomerID=customer_id) \
        .filter(Orders.OrderTime >= startdate) \
        .filter(Orders.OrderTime <= datetime.now()) \
        .order_by(Orders.OrderID).all()
    assert len(response.json["orders"]) == len(orders)
    for response_order, expected_order in zip(response.json["orders"], orders):
        assert "order_id" in response_order
        assert response_order["order_id"] == expected_order.OrderID
        assert "restaurant_id" in response_order
        assert "total_price" in response_order
        assert response_order["total_price"] == expected_order.TotalPrice
        assert "order_time" in response_order
        assert response_order["order_time"] == expected_order.OrderTime.strftime('%Y-%m-%d %H:%M:%S')
        assert "finished" in response_order
        assert response_order["finished"] == expected_order.Finish
        assert "reviewed" in response_order
        assert response_order["reviewed"] == expected_order.Reviewed
        assert "overall_rating" in response_order
        overall_rating = session.query(Review) \
            .filter_by(OrderID=expected_order.OrderID) \
            .filter_by(CustomerID=customer_id, DishID=0).first()
        if overall_rating is None:
            assert response_order["overall_rating"] == -1
        else:
            assert response_order["overall_rating"] == overall_rating.Rating
        assert "dishes" in response_order
        order_dishes = session.query(Order_Dish).filter_by(OrderID=expected_order.OrderID).all()
        assert len(response_order["dishes"]) == len(order_dishes)

def test_main_add_review_success(client, session):
    token = generate_token(100003, 'restaurant_2')
    dishes = [0, 1, 2]
    ratings = [5, 4, 3]
    restaurant_id = 1
    dishes_info = session.query(Dish_Info).filter(Dish_Info.DishID.in_(dishes)).order_by(Dish_Info.DishID).all()
    restaurant_info = session.query(Restaurant_Info).filter_by(RestaurantID=restaurant_id).first()
    order = session.query(Orders).filter_by(OrderID = 1).first()
    order.Finish = True
    session.commit()
    before_rating = [restaurant_info.Rating] + [dish.Rating for dish in dishes_info]
    before_rating_cnt = [restaurant_info.RatingCnt] + [dish.RatingCnt for dish in dishes_info]
    response = client.post('/main/add_review', json={
        "order_id": 1,
        "overall_rating": ratings[0],
        "dishes_rating": [{"dish_id": 1, "rating": ratings[1]}, {"dish_id": 2, "rating": ratings[2]}]
    }, headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    assert response.json["status"] == "success"
    for i in range(len(before_rating)):
        if i == 0:
            assert restaurant_info.Rating == (before_rating[i] * before_rating_cnt[i] + ratings[0]) / (before_rating_cnt[i] + 1)
            assert before_rating_cnt[i] == restaurant_info.RatingCnt - 1
        else:
            assert dishes_info[i-1].Rating == (before_rating[i] * before_rating_cnt[i] + ratings[i]) / (before_rating_cnt[i] + 1)
            assert before_rating_cnt[i] == dishes_info[i-1].RatingCnt - 1
    
    review = session.query(Review).filter_by(OrderID=1).all()
    assert len(review) == 3

def test_main_add_review_invalid_order(client, session):
    token = generate_token(100004, 'worker')
    order = session.query(Orders).filter_by(OrderID = 1).first()
    order.Finish = True
    session.commit()
    response = client.post('/main/add_review', json={
        "order_id": 1,
        "overall_rating": 5,
        "dishes_rating": [{"dish_id": 1, "rating": 4}, {"dish_id": 2, "rating": 3}]
    }, headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 403
    assert response.json["error"] == "It's not your order."

def test_main_add_review_invalid_dish(client, session):
    token = generate_token(100003, 'restaurant_2')
    order = session.query(Orders).filter_by(OrderID = 1).first()
    order.Finish = True
    session.commit()
    response = client.post('/main/add_review', json={
        "order_id": 1,
        "overall_rating": 5,
        "dishes_rating": [{"dish_id": 3, "rating": 4}, {"dish_id": 4, "rating": 3}]
    }, headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 404
    assert response.json["error"] == "Dish not found in order"

def test_main_add_review_order_not_finish(client):
    token = generate_token(100003, 'restaurant_2') 
    response = client.post('/main/add_review', json={
        "order_id": 1,
        "overall_rating": 5,
        "dishes_rating": [{"dish_id": 1, "rating": 4}, {"dish_id": 2, "rating": 3}]
    }, headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 403
    assert response.json["error"] == "Order not finished"

def test_main_add_reviewed_order(client):
    token = generate_token(100006, 'worker')
    response = client.post('/main/add_review', json={
        "order_id": 2,
        "overall_rating": 5,
        "dishes_rating": [{"dish_id": 5, "rating": 4}]
    }, headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 403
    assert response.json["error"] == "Order has been reviewed"