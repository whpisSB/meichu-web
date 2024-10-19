from flask import request, jsonify
from model.models import Staff_Info
from controller.user_auth import generate_token
from datetime import datetime
from model.models import Training_Certifications
from model.models import Pr
from model.models import db
from model.models import Reward

NOTIFY_DATE = 5

def login():
    account = request.get_json().get("user_account")
    password = request.get_json().get("user_password")
    # return jsonify({'user_account': account, 'user_password': password})
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

def health_check():
    if request.method == 'GET':
        # Handle POST request
        return jsonify({"message": "Health check POST request received"}), 200
    else:
        # Handle GET request (existing implementation)
        health_data = {
            "status": "ok",
            "timestamp": datetime.datetime.now().isoformat()
        }
        return jsonify(health_data)

def get_training_certifications():
    training = Training_Certifications.query.all()
    training_list = []
    for cert in training:
        training_list.append({
            'Employee_ID': cert.Employee_ID,
            'Training_Name': cert.Training_Name,
            'Completion_Date': cert.Completion_Date,
            'Expire_Date': cert.Expire_Date
        })
    return jsonify(training_list)

def update_pr():
    data = request.get_json()
    
    # Check if data is a single dictionary or a list of dictionaries
    if isinstance(data, dict):
        data = [data]  # Convert single dict to list for consistent processing
    
    return_list = []
    for repo in data:
        pr = Pr(
            RepositoryID=repo['RepositoryID'],
            GithubID=repo['GithubID'],
            CommitCount=repo['CommitCount'],
            Additions=repo['Additions'],
            Deletions=repo['Deletions'],
            Total=repo['Total'],
            Summary=repo['Summary'],
            Reviewers=repo['Reviewers']
        )
        db.session.add(pr)
        return_list.append(repo['RepositoryID'])
        return_list.append(repo['GithubID'])
        return_list.append(repo['CommitCount'])
        return_list.append(repo['Additions'])
        return_list.append(repo['Deletions'])
        return_list.append(repo['Total'])
        return_list.append(repo['Summary'])
        return_list.append(repo['Reviewers'])
    
    try:
        db.session.commit()
        return jsonify({'message': 'success', 'payload': return_list}), 200
    except Exception as e:
        # db.session.rollback()
        return jsonify({'message': 'error', 'error': str(e)}), 500
    
def get_reward():
    reward = Reward.query.all()
    reward_list = []
    for r in reward:
        reward_list.append({
            'RewardID': r.RewardID,
            'Title': r.Title,
            'ThumbnailImage': r.ThumbnailImage,
            'Dhumbnail_image': r.Dhumbnail_image,
            'Points': r.Points
        })
    return jsonify(reward_list)