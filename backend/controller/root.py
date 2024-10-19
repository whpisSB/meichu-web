from flask import request, jsonify
from model.models import Staff_Info
from controller.user_auth import generate_token
from datetime import datetime
from model.models import Training_Certifications
from model.models import Pr
from model.models import db
from model.models import Reward
from model.models import User_Rewards
from model.models import TSMC_User

#################### GEN AI ####################
import random
import torch
import numpy as np
from PIL import Image
import intel_extension_for_pytorch as ipex
from diffusers import StableDiffusionPipeline, DDIMScheduler

scheduler = DDIMScheduler.from_pretrained(
    "somq/fantassified_icons_v2", subfolder="scheduler"
)
pipe = StableDiffusionPipeline.from_pretrained("somq/fantassified_icons_v2").to("cpu")

# optimize with IPEX
pipe.unet = ipex.optimize(pipe.unet.eval(), dtype=torch.bfloat16, inplace=True)
# pipe.vae = ipex.optimize(pipe.vae.eval(), dtype=torch.bfloat16, inplace=True)
# pipe.text_encoder = ipex.optimize(
#     pipe.text_encoder.eval(), dtype=torch.bfloat16, inplace=True
# )
# pipe.safety_checker = ipex.optimize(
#     pipe.safety_checker.eval(), dtype=torch.bfloat16, inplace=True
# )
# pipe.set_progress_bar_config(disable=True)

################################################

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
            'reward_id': r.RewardID,
            'title': r.Title,
            'thumbnail_image': r.ThumbnailImage,
            'description': r.Description,
            'points': r.Points
        })
    return jsonify(reward_list)

def exchange_reward():
    data = request.get_json()
    line_id = data['line_id']
    reward_id = data['reward_id']

    # Get the user and reward from the database
    user = TSMC_User.query.filter_by(Line_ID=line_id).first()
    reward = Reward.query.get(reward_id)

    if not user or not reward:
        return jsonify({'message': 'User or reward not found'}), 404

    # Check if user has enough points
    if user.Points < reward.Points:
        return jsonify({'message': 'Not enough points'}), 400

    # Deduct points from user
    user.Points -= reward.Points

    # Create new user_reward entry
    user_reward = User_Rewards(Line_ID=line_id, RewardID=reward_id)
    
    # Add changes to session
    db.session.add(user_reward)
    db.session.add(user)
    
    try:
        # Commit the changes
        db.session.commit()
        return jsonify({
            'message': 'success',
            'remaining_points': user.Points,
            'reward_title': reward.Title,
            'points_deducted': reward.Points
        })
    except Exception as e:
        # If there's an error, rollback the changes
        db.session.rollback()
        return jsonify({'message': 'error', 'error': str(e)}), 500
    

def icon():
    # pass
    data = request.get_json()
    prompt = data['prompt']
    #!!!!!!!!!!!!!!!!!!TO DO!!!!!!!!!!!!!!!!!!!!

    seed = random.randint(0, 1_000_000)
    guide = random.uniform(7.5, 10.0)
    gen = torch.Generator().manual_seed(seed)

    with torch.cpu.amp.autocast(enabled=True, dtype=torch.bfloat16):
        images = pipe(
            prompt,
            num_images_per_prompt=1,
            num_inference_steps=25,
            guidance_scale=guide,
            generator=gen,
        ).images[0].resize((64, 64), Image.LANCZOS)

    np_image = np.array(images)
    if np_image.sum() == 0:
        return jsonify({'message': 'NSFW'}), 400    # if the image is NSFW, return 400

    return jsonify({'icon': np_image.tolist()})

    # return jsonify({'icon': 'https://google.com'})
    