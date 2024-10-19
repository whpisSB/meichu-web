from flask import Blueprint
from controller.root import login, ping, health_check,get_training_certifications, update_pr, get_reward, exchange_reward, icon, get_user_rewards, get_user_info, review_result, review_history

bp_root = Blueprint('bp_root', __name__)
bp_main = Blueprint('bp_main', __name__)
bp_pos = Blueprint('bp_pos', __name__)
bp_admin = Blueprint('bp_admin', __name__)

# prefix: /
bp_root.route('/login', methods=['POST'])(login)
bp_root.route('/ping', methods=['GET'])(ping)
bp_root.route('/health_check', methods=['POST','GET'])(health_check)
bp_root.route('/get_training_certifications', methods=['GET'])(get_training_certifications)
bp_root.route('/pr', methods=['POST'])(update_pr)
bp_root.route('/reward', methods=['GET'])(get_reward)
bp_root.route('/exchange_reward', methods=['POST'])(exchange_reward)
bp_root.route('/icon', methods=['POST'])(icon)
bp_root.route('/user_rewards', methods=['GET'])(get_user_rewards)
bp_root.route('/user_info', methods=['GET'])(get_user_info)
bp_root.route('/review', methods=['POST'])(review_result)
bp_root.route('/review_history', methods=['GET'])(review_history)