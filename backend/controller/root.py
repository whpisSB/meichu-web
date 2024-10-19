from flask import request, jsonify
from datetime import datetime
from model.models import Training_Certifications
from model.models import Pr
from model.models import db
from model.models import Reward
from model.models import User_Rewards
from model.models import TSMC_User
from model.models import Review
import requests

#################### GEN AI ####################
# import random
# import torch
# import numpy as np
# from PIL import Image
# import intel_extension_for_pytorch as ipex
# from diffusers import StableDiffusionPipeline, DDIMScheduler

# scheduler = DDIMScheduler.from_pretrained(
#     "somq/fantassified_icons_v2", subfolder="scheduler"
# )
# pipe = StableDiffusionPipeline.from_pretrained("somq/fantassified_icons_v2").to("cpu")

# # optimize with IPEX
# pipe.unet = ipex.optimize(pipe.unet.eval(), dtype=torch.bfloat16, inplace=True)
# # pipe.vae = ipex.optimize(pipe.vae.eval(), dtype=torch.bfloat16, inplace=True)
# pipe.text_encoder = ipex.optimize(
#     pipe.text_encoder.eval(), dtype=torch.bfloat16, inplace=True
# )
# pipe.safety_checker = ipex.optimize(
#     pipe.safety_checker.eval(), dtype=torch.bfloat16, inplace=True
# )
# pipe.set_progress_bar_config(disable=True)

################################################

NOTIFY_DATE = 5
LINE_SERVER_ENDPOINT = "https://dog-heroic-seal.ngrok-free.app"

def login():
    account = request.get_json().get("user_account")
    password = request.get_json().get("user_password")
    # return jsonify({'user_account': account, 'user_password': password})
    staff = TSMC_User.query.filter_by(Email=account, Password=password).first()
    if staff is None:
        return jsonify({"status" : "error"})
    else:
        return jsonify({"status" : "ok"})

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
    print(data)
    reviewer = TSMC_User.query.filter_by(Github_ID=data['reviewer_id']).first()

    if reviewer is None:
        return jsonify({'message': 'Reviewer not found'}), 404

    data['reviewer_id'] = reviewer.Line_ID
    res = requests.post(f'{LINE_SERVER_ENDPOINT}/review', json=data)

    if res.status_code != 200:
        return jsonify({'message': 'error', 'error': res.text}), 500
    
    return jsonify({'message': 'success'}), 200
    
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
    pass
    # data = request.get_json()
    # prompt = data['prompt']
    # #!!!!!!!!!!!!!!!!!!TO DO!!!!!!!!!!!!!!!!!!!!

    # scheduler = DDIMScheduler.from_pretrained(
    #     "somq/fantassified_icons_v2", subfolder="scheduler"
    # )
    # pipe = StableDiffusionPipeline.from_pretrained("somq/fantassified_icons_v2").to("cpu")

    # # optimize with IPEX
    # pipe.unet = ipex.optimize(pipe.unet.eval(), dtype=torch.bfloat16, inplace=True)
    # pipe.vae = ipex.optimize(pipe.vae.eval(), dtype=torch.bfloat16, inplace=True)
    # pipe.text_encoder = ipex.optimize(
    #     pipe.text_encoder.eval(), dtype=torch.bfloat16, inplace=True
    # )
    # pipe.safety_checker = ipex.optimize(
    #     pipe.safety_checker.eval(), dtype=torch.bfloat16, inplace=True
    # )
    # pipe.set_progress_bar_config(disable=True)

    # return jsonify({'message': 'success'})  

    # seed = random.randint(0, 1_000_000)
    # guide = random.uniform(7.5, 10.0)
    # gen = torch.Generator().manual_seed(seed)

    # with torch.cpu.amp.autocast(enabled=True, dtype=torch.bfloat16):
    #     images = pipe(
    #         prompt,
    #         num_images_per_prompt=1,
    #         num_inference_steps=25,
    #         guidance_scale=guide,
    #         generator=gen,
    #     ).images[0].resize((64, 64), Image.LANCZOS)

    # np_image = np.array(images)
    # if np_image.sum() == 0:
    #     return jsonify({'message': 'NSFW'}), 400    # if the image is NSFW, return 400

    # buffered = io.BytesIO()
    # images.save(buffered, format="JPEG")  # 指定格式
    # encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # return jsonify({'icon': encoded_image})

    # return jsonify({'icon': 'https://google.com'})

def get_user_rewards():
    data = request.get_json()
    line_id = data['line_id']
    
    # Get all reward IDs for the user
    user_rewards = User_Rewards.query.filter_by(Line_ID=line_id).all()
    reward_ids = [ur.RewardID for ur in user_rewards]
    
    # Fetch reward details from the Reward table
    rewards = Reward.query.filter(Reward.RewardID.in_(reward_ids)).all()
    
    response = []
    for reward in rewards:
        response.append({
            'reward_id': reward.RewardID,
            'title': reward.Title,
            'thumbnail_image': reward.ThumbnailImage,
            'description': reward.Description
        })
    
    return jsonify(response)

def get_user_info():
    data = request.get_json()
    email = data['email']
    
    user = TSMC_User.query.filter_by(Email=email).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'name': user.Name,
        'github_id': user.Github_ID,
        'email': user.Email,
        'line_id': user.Line_ID,
        'points': user.Points
    })

def review_result():
    data = request.get_json()
    author_github_id = data['author_id']
    pr_url = data['pr_url']
    reviewer_line_id = data['reviewer_id']
    result = int(data['result'])

    author = TSMC_User.query.filter_by(Github_ID=author_github_id).first()
    author.Points += result
    db.session.add(author)

    reviewer_github_id = TSMC_User.query.filter_by(Line_ID=reviewer_line_id).first().Github_ID
    review = Review(
        AuthorGithubID=author_github_id,
        PRUrl=pr_url,
        ReviewerGithubID=reviewer_github_id,
        Points=result,
        ReviewAt=datetime.now()
    )

    db.session.add(review)
    
    try:
        db.session.commit()
        return jsonify({'message': 'success'}), 200
    except Exception as e:
        # db.session.rollback()
        return jsonify({'message': 'error', 'error': str(e)}), 500