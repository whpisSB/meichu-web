import pytest
from controller.user_auth import generate_token
from model.models import Orders, Order_Dish, Dish_Info, db
from datetime import datetime

@pytest.mark.parametrize(
    "clerk_id, user_type, expected", 
    [
        (
            100001, 'restaurant_1', {
                "number_of_meals": 4,
                "testcase": [1, 0, 0, 1],
                "meals":[
                    { # common
                        "dish_id": 1,
                        "name": "Fried Chicken",
                        "description": "Delicious",
                        "combo": False,
                        "price": 200,
                        "rating": 0,
                        "order_times": 1,
                        "picture": "/static/dish/chicken.jpg",
                        "available": True
                    }, {}, {}, { # combo
                        "dish_id": 4,
                        "name": "Six Nuggets with Coke",
                        "description": "Delicious",
                        "combo": True,
                        "price": 150,
                        "rating": 0,
                        "order_times": 0,
                        "picture": "/static/dish/chicken.jpg",
                        "available": True
                    }
                ]
            }
        ), (
            100003, 'restaurant_2', {
                "number_of_meals": 3,
                "testcase": [0, 1, 0],
                "meals":[
                    {}, { # unavailable
                        "dish_id": 6,
                        "name": "Veggie Delite",
                        "description": "Delicious",
                        "combo": False,
                        "price": 150,
                        "rating": 0,
                        "order_times": 0,
                        "picture": "/static/dish/chicken.jpg",
                        "available": False
                    }, {}
                ]
            }
        )
    ]
)
def test_POS_get_menu_success(client, clerk_id, user_type, expected):
    restaurant_token = generate_token(clerk_id, user_type)
    response = client.get('/pos/menu', headers={'Authorization': f'Bearer {restaurant_token}'})
    assert response.status_code == 200
    assert len(response.json['meals']) == expected['number_of_meals']
    for i in range(expected['number_of_meals']):
        meal = response.json['meals'][i]
        if expected['testcase'][i]:
            print(f"response: {meal}\nexpected: {expected['meals'][i]}")
            assert meal == expected['meals'][i]

@pytest.mark.parametrize("endpoint, method", \
    [('/pos/menu', 'get'),('/pos/get_order', 'get'), ('/pos/add_order', 'post'), ('/pos/worker_info/100006', 'get')])
def test_POS_with_invalid_token(client, endpoint, method):
    worker_token = generate_token(100005, 'worker')
    if method == 'get':
        response = client.get(endpoint, headers={'Authorization': f'Bearer {worker_token}'})
    else:
        response = client.post(endpoint, headers={'Authorization': f'Bearer {worker_token}'})
    assert response.status_code == 403
    assert response.json['error'] == 'Permission Denied'

@pytest.mark.parametrize(
    "clerk_id, user_type, expected",
    [
        (
            100001, 'restaurant_1', {
                "order_id": 1,
                "customer_id": 100003,
                "customer_name": 'whoami',
                "price": 350,
                "order_time": "",
                "finish": False,
                "dishes":
                [
                    {
                        "dish_id": 1,
                        "number": 1,
                        "dish_name": "Fried Chicken",
                        "price": 200
                    }, {
                        "dish_id": 2,
                        "number": 1,
                        "dish_name": "Hamburger",
                        "price": 150,
                    }
                ]
            }
        )
    ]
)
def test_POS_get_order_format(client, clerk_id, user_type, expected):
    restaurant_token = generate_token(clerk_id, user_type)
    response = client.get('/pos/get_order', headers={'Authorization': f'Bearer {restaurant_token}'})
    assert response.status_code == 200
    assert "orders" in response.json
    orders = response.json['orders']
    for order in orders:
        assert order['order_id'] == expected['order_id']
        assert order['customer_id'] == expected['customer_id']
        assert order['customer_name'] == expected['customer_name']
        assert "order_time" in order
        assert order['finish'] == expected['finish']
        assert order["dishes"] == expected["dishes"]
        print(f"response: {order['dishes']}\nexpected: {expected['dishes']}")

@pytest.mark.parametrize('restaurant_id', [(1), (2), (3)])
def test_POS_get_only_todays_order(client, restaurant_id):
    restaurant_token = generate_token(100003, f'restaurant_{restaurant_id}')
    response = client.get('/pos/get_order', headers={'Authorization': f'Bearer {restaurant_token}'})
    assert response.status_code == 200
    assert "orders" in response.json
    today = datetime.today()
    start = datetime(today.year, today.month, today.day, 0, 0, 0)
    end = datetime(today.year, today.month, today.day, 23, 59, 59)
    for order in response.json['orders']:
        order_time = datetime.strptime(order['order_time'], "%Y-%m-%d %H:%M:%S")
        assert start <= order_time
        assert order_time <= end

def test_POS_add_order(client, session):
    restaurant_token = generate_token(100003, 'restaurant_2')
    response = client.post('/pos/add_order', headers={'Authorization': f'Bearer {restaurant_token}'}, json={
        "customer_id": 100003,
        "total_price": 430,
        "dishes": [
            {
                "dish_id": 5,
                "number": 3
            }, {
                "dish_id": 7,
                "number": 2
            }
        ]
    })
    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert "order_id" in response.json
    order_id = response.json['order_id']
    order = session.query(Orders).filter_by(OrderID=order_id).first()
    assert order is not None
    assert order.RestaurantID == 2
    assert order.CustomerID == 100003
    assert order.TotalPrice == 430
    assert order.OrderTime is not None
    assert order.Finish == False
    assert order.Reviewed == False

    ordered_dishes = session.query(Order_Dish).filter_by(OrderID=order_id).all()
    assert len(ordered_dishes) == 2
    for dish in ordered_dishes:
        assert dish.OrderID == order_id
        assert dish.DishID in [5, 7]
        if dish.DishID == 5:
            assert dish.Number == 3
        else:
            assert dish.Number == 2

def test_POS_finish_order_success(client, session):
    restaurant_token = generate_token(100001, 'restaurant_1')
    order_id = 1
    ordered_dishes = session.query(Order_Dish).filter_by(OrderID=order_id).all()
    dish_info = {}
    before_order_times = {}
    for ordered_dish in ordered_dishes:
        dish_info[ordered_dish.DishID] = session.query(Dish_Info).filter_by(DishID=ordered_dish.DishID).first()
        before_order_times[ordered_dish.DishID] = dish_info[ordered_dish.DishID].TimesOfOrder
    response = client.post(f'/pos/finish/{order_id}', headers={'Authorization': f'Bearer {restaurant_token}'})
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    for ordered_dish in ordered_dishes:
        assert before_order_times[ordered_dish.DishID] + ordered_dish.Number == dish_info[ordered_dish.DishID].TimesOfOrder

def test_POS_finish_order_invalid_id(client):
    restaurant_token = generate_token(100001, 'restaurant_1')
    response = client.post('/pos/finish/10000', headers={'Authorization': f'Bearer {restaurant_token}'})
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['error'] == 'Order not found'

def test_POS_already_finished_order(client):
    restaurant_token = generate_token(100003, 'restaurant_2')
    order_id = 2
    response = client.post(f'/pos/finish/{order_id}', headers={'Authorization': f'Bearer {restaurant_token}'})
    assert response.status_code == 200
    assert response.json['status'] == 'error'
    assert response.json['error'] == 'Order has already finished'

def test_POS_finish_order_permission_denied(client):
    restaurant_token = generate_token(100003, 'restaurant_2')
    order_id = 1
    response = client.post(f'/pos/finish/{order_id}', headers={'Authorization': f'Bearer {restaurant_token}'})
    assert response.status_code == 403
    assert response.json['status'] == 'error'
    assert response.json['error'] == 'Permission Denied, restaurant id not matched'

def test_POS_get_worker_info(client):
    restaurant_token = generate_token(100003, 'restaurant_2')
    response = client.get('/pos/worker_info/100006', headers={'Authorization': f'Bearer {restaurant_token}'})
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['id'] == 100006
    assert 'name' in response.json
    assert response.json['name'] == 'BruceLin'
    assert 'phone' in response.json
    assert response.json['phone'] == '0943134344'

def test_POS_get_invalid_worker_info(client):
    restaurant_token = generate_token(100003, 'restaurant_2')
    response = client.get('/pos/worker_info/200', headers={'Authorization': f'Bearer {restaurant_token}'})
    assert response.status_code == 404
    assert response.json['error'] == 'Worker not found'

def test_POS_check_paid_status(client):
    restaurant_token = generate_token(100003, 'restaurant_2')
    response = client.get('/pos/paid/100005', headers={'Authorization': f'Bearer {restaurant_token}'})
    assert response.status_code == 200
    assert response.json['customer_id'] == 100005
    assert response.json['paid'] == False