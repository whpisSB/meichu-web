from flask import Blueprint
from controller.root import login, ping, health_check,get_training_certifications, update_pr, get_reward
from controller.main import get_restaurant_info, add_review, history, get_restaurant_list
from controller.pos import get_menu, get_order, add_order, finish_order, get_worker_info, check_paid
from controller.admin import add_dish, upload_picture, update_menu, get_monthly_payment_report
from controller.admin import get_menus, update_price, get_monthly_report, add_restaurant

bp_root = Blueprint('bp_root', __name__)
bp_main = Blueprint('bp_main', __name__)
bp_pos = Blueprint('bp_pos', __name__)
bp_admin = Blueprint('bp_admin', __name__)

# prefix: /
bp_root.route('/login', methods=['POST'])(login)
bp_root.route('/ping', methods=['GET'])(ping)
bp_root.route('/health_check', methods=['POST','GET'])(health_check)
bp_root.route('/get_training_certifications', methods=['POST'])(get_training_certifications)
bp_root.route('/pr', methods=['POST'])(update_pr)
bp_root.route('/reward', methods=['GET'])(get_reward)
# prefix: /main
bp_main.route('/restaurant/<id>', methods=['GET'])(get_restaurant_info)
bp_main.route('/add_review', methods=['POST'])(add_review)
bp_main.route('/history', methods=['GET'])(history)
bp_main.route('/restaurant_list', methods=['GET'])(get_restaurant_list)

# prefix: /pos
bp_pos.route('/menu', methods=['GET'])(get_menu)
bp_pos.route('/get_order', methods=['GET'])(get_order)
bp_pos.route('/add_order', methods=['POST'])(add_order)
bp_pos.route('/finish/<order_id>', methods=['POST'])(finish_order)
bp_pos.route('/worker_info/<id>', methods=['GET'])(get_worker_info)
bp_pos.route('/paid/<customer_id>', methods=['GET'])(check_paid)

# prefix: /admin
bp_admin.route('/add_dish', methods=['POST'])(add_dish)
bp_admin.route('/upload/<type>', methods=['POST'])(upload_picture)
bp_admin.route('/update_menu', methods=['POST'])(update_menu)
bp_admin.route('/get_menus', methods=['GET'])(get_menus)
bp_admin.route('/update_price', methods=['POST'])(update_price)
bp_admin.route('/monthly_report', methods=['POST'])(get_monthly_report)
bp_admin.route('/add_restaurant', methods=['POST'])(add_restaurant)
bp_admin.route('/monthly_payment_report', methods=['POST'])(get_monthly_payment_report)