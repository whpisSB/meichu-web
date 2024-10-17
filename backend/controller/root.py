from flask import request, jsonify
from model.models import Staff_Info
from controller.user_auth import generate_token
from datetime import datetime

NOTIFY_DATE = 5

def login():
    account = request.get_json().get("user_account")
    password = request.get_json().get("user_password")
    staff = Staff_Info.query.filter_by(Gmail=account, Password=password).first()
    if staff is None:
        return jsonify({'outh_token': "", 'user_identity': "invalid_user"})
    access_token = generate_token(staff.StaffID, staff.Position)
    
    today = datetime.now().day
    notify = False
    if not staff.Paid and today <= NOTIFY_DATE:
        notify = True
    
    if staff.Position.find("restaurant") == -1:
        return jsonify({'outh_token': access_token, 'user_identity': staff.Position, 'notify': notify})
    else:
        return jsonify({'outh_token': access_token, 'user_identity': "restaurant", 
                        'notify': notify, 'restaurant_id': staff.Position.split('_')[1]})

def ping():
    return jsonify({'message': 'pong'})
