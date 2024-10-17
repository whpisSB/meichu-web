import pytest
from model.models import *
from controller.user_auth import generate_token
from os.path import exists
from os import remove
import random

@pytest.mark.parametrize(
    "user_id, user_type, endpoint, method", [
        (100001, 'restaurant_1', '/admin/add_dish', 'POST'),
        (100003, 'restaurant_2', '/admin/monthly_report', 'GET'),
        (100004, 'worker', '/admin/get_menus', 'GET'),
        (100005, 'worker', '/admin/update_price', 'POST'),
        (100006, 'worker', '/admin/update_menu', 'POST'),
        (100004, 'worker', '/admin/add_restaurant', 'POST')
    ]
)
def test_admin_invalid_credentials(client, user_id, user_type, endpoint, method):
    token = generate_token(user_id, user_type)
    response = None
    if method == 'GET':
        response = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
    else:
        response = client.post(endpoint, headers={'Authorization': 'Bearer ' + token}, json={})
    assert response.status_code == 403

def test_admin_add_dish_picture_not_exist(client):
    token = generate_token(100002, 'admin')
    response = client.post('/admin/add_dish', headers={'Authorization': 'Bearer ' + token}, json={
        'restaurant_id': 2,
        'name': 'test_dish',
        'description': 'test_description',
        'combo': 0,
        'picture_filename': 'hello.jpg',
        'price': 100
    })
    assert response.status_code == 200
    assert response.json['status'] == 'fail'
    assert response.json['error'] == 'Picture has not been uploaded'

def test_admin_add_dish_success(client, session):
    token = generate_token(100002, 'admin')
    response = client.post('/admin/add_dish', headers={'Authorization': 'Bearer ' + token}, json={
        'restaurant_id': 2,
        'name': 'test_dish',
        'description': 'test_description',
        'combo': 0,
        'picture_filename': 'chicken.jpg',
        'price': 100
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    dish = session.query(Dish_Info).filter(Dish_Info.Name == 'test_dish').first()
    assert dish is not None

def test_admin_monthly_report_generate(client):
    token = generate_token(100002, 'admin')
    if exists('./monthly_report/2024_6.csv'):
        remove('./monthly_report/2024_6.csv')
    response = client.get('/admin/monthly_report', json={"year": 2024, "month": 6}, headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    assert exists('./monthly_report/2024_6.csv')
    remove('./monthly_report/2024_6.csv')

    assert 'Content-Disposition' in response.headers
    assert 'attachment' in response.headers['Content-Disposition']
    assert 'filename=' in response.headers['Content-Disposition']
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    data = response.data.decode('utf-8')
    assert data.find("餐廳") != -1
    assert data.find("總營收") != -1
    assert data.find("訂單平均價格") != -1
    assert data.find("餐廳評分") != -1
    assert data.find("餐點平均評分") != -1

def test_admin_monthly_report_already_exist(client):
    token = generate_token(100002, 'admin')
    response = client.get('/admin/monthly_report', json={"year": 2024, "month": 5}, headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    assert 'Content-Disposition' in response.headers
    assert 'attachment' in response.headers['Content-Disposition']
    assert 'filename=' in response.headers['Content-Disposition']
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    data = response.data.decode('utf-8')
    assert data.find("餐廳") != -1
    assert data.find("總營收") != -1
    assert data.find("訂單平均價格") != -1
    assert data.find("餐廳評分") != -1
    assert data.find("餐點平均評分") != -1

def test_admin_get_menus(client):
    token = generate_token(100002, 'admin')
    response = client.get('/admin/get_menus', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    assert "restaurants" in response.json

    for restaurant in response.json["restaurants"]:
        assert "restaurant_id" in restaurant
        assert "restaurant_name" in restaurant
        assert "phone" in restaurant
        assert "open_time" in restaurant
        assert "close_time" in restaurant
        assert "overall_rating" in restaurant
        assert "dishes" in restaurant
        for dish in restaurant["dishes"]:
            assert "dish_id" in dish
            assert "dish_name" in dish
            assert "combo" in dish
            assert "price" in dish
            assert "available" in dish
            assert "ordered_times" in dish
            assert "rating" in dish

def test_admin_update_price_success(client, session):
    token = generate_token(100002, 'admin')
    dish = session.query(Dish_Info).filter_by(DishID=1).first()
    response = client.post('/admin/update_price', headers={'Authorization': 'Bearer ' + token}, json={
        'dish_id': 1,
        'updated_price': 2000
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert dish.Price == 2000

def test_admin_update_price_invalid_dish_id(client):
    token = generate_token(100002, 'admin')
    response = client.post('/admin/update_price', headers={'Authorization': 'Bearer ' + token}, json={  
        'dish_id': 1000,
        'updated_price': 2000
    })
    assert response.status_code == 200
    assert response.json['status'] == 'fail'
    assert response.json['error'] == 'Invalid dish id'

def test_admin_add_restaurant(client, session):
    token = generate_token(100002, 'admin')
    response = client.post('/admin/add_restaurant', headers={'Authorization': 'Bearer ' + token}, json={
        'restaurant_name': 'test_restaurant',
        'phone': '12345678',
        'open_time': '08:00',
        'close_time': '20:00',
        'description': 'test_description',
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert "restaurant_id" in response.json
    restaurant = session.query(Restaurant_Info).filter_by(RestaurantID=response.json["restaurant_id"]).first()
    assert restaurant is not None
    assert restaurant.RestaurantName == 'test_restaurant'

def test_admin_update_menu_success(client, session):
    token = generate_token(100002, 'admin')
    dishes = session.query(Dish_Info).filter_by(RestaurantID=1).all()
    random.shuffle(dishes)
    available = [dishes[i].DishID for i in range(len(dishes) // 2)]
    response = client.post('/admin/update_menu', headers={'Authorization': 'Bearer ' + token}, json={
        "available_dish_id": available
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    for i in range(len(dishes)):
        assert dishes[i].Available == (dishes[i].DishID in available)

def test_admin_update_menu_invalid_dish_id(client, session):
    token = generate_token(100002, 'admin')
    dish = session.query(Dish_Info).filter_by(DishID=1).first()
    original_status = dish.Available
    response = client.post('/admin/update_menu', headers={'Authorization': 'Bearer ' + token}, json={
        "available_dish_id": [1000, 200] if original_status else [1, 1000, 200]
    })
    assert response.status_code == 200
    assert response.json['status'] == 'fail'
    assert response.json['error'].find('Invalid dish id') != -1
    assert dish.Available == original_status

def test_admin_monthly_payment_report(client):
    token = generate_token(100002, 'admin')
    response = client.post('/admin/monthly_payment_report', json={"year": 2024, "month": 6}, headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    assert 'Content-Disposition' in response.headers
    assert 'attachment' in response.headers['Content-Disposition']
    assert 'filename=' in response.headers['Content-Disposition']
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'