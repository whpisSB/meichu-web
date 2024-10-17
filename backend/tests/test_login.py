import pytest

def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json['message'] == 'pong'

@pytest.mark.parametrize(
    "credential ,expected", [
        (
            {"user_account": "ycy.yo@gmail.com", "user_password": "test"},
            {"restaurant_id": 1, "user_identity": "restaurant"}
        ), (
            {"user_account": "hello@world", "user_password": "test"},
            {"user_identity": "admin"}
        ), (
            {"user_account": "benson@gmail.com", "user_password": "test"},
            {"user_identity": "worker"}
        ),(
            {"user_account": "detaomega@gmail.com", "user_password": "test"},
            {"user_identity": "worker"}
        )
    ]
)
def test_login_with_valid_credential(client, credential, expected):
    response = client.post('/login', json=credential)
    assert response.status_code == 200
    assert response.json['user_identity'] == expected['user_identity']
    if expected['user_identity'] == 'restaurant':
        assert int(response.json['restaurant_id']) == expected['restaurant_id']
    assert 'outh_token' in response.json
    assert response.json['outh_token'] is not None


@pytest.mark.parametrize(
    "credential", [
        ({"user_account": "ycy.y@gmai.com", "user_password": "test"}),  # invalid account
        ({"user_account": "hello@world", "user_password": "hello"}),  # invalid password
        ({"user_account": "amber chen", "user_password": "test"}) # use id as account
    ]
)
def test_login_with_invalid_credential(client, credential):
    response = client.post('/login', json=credential)
    assert response.status_code == 200
    assert response.json['user_identity'] == "invalid_user"
    assert 'outh_token' in response.json
    assert response.json['outh_token'] == ''

