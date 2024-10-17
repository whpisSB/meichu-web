from flask import Flask, jsonify
from model.models import db
import atexit
from datetime import datetime
from route.routes import bp_root, bp_main, bp_pos, bp_admin
from controller.admin import reset_paid_flag
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    # flask 2.3x remove buildin config value JSON_SORT_KEYS, so it cannot be set in config.py
    app.json.sort_keys = False 
    db.init_app(app)
    jwt = JWTManager(app)
    jwt.init_app(app)

    scheduler = BackgroundScheduler()
    scheduler.add_job(reset_paid_flag, 'cron', day=1, hour=0, minute=0, second=0, id='reset_paid_flag')
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    app.register_blueprint(bp_root, url_prefix='')  
    app.register_blueprint(bp_main, url_prefix='/main')
    app.register_blueprint(bp_pos, url_prefix='/pos')
    app.register_blueprint(bp_admin, url_prefix='/admin')
    return app

app = create_app()

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)