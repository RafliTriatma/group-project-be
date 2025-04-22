import uuid

from flask import Flask, render_template, jsonify, request

# # from auth.login import login_required
# from middleware.auth import auth_middleware
# # from models.user import dummy_users
# from router.auth import auth_router
# from router.user import user_router
# from router.account import account_router
# from router.transaction import transaction_router
from utils.database import init_db

# import models  # noqa: F401


def create_app(config_module="config.local"):
    app = Flask(__name__, template_folder='templates')

    username = 'postgres.qmevwrwkraypcvhjxrvw'
    password = 'Finalproject1-'
    host = 'aws-0-us-east-2.pooler.supabase.com'
    database = 'postgres'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}/{database}'
    init_db(app)

    app.register_blueprint(user_router)
    app.register_blueprint(auth_router)
    app.register_blueprint(account_router)
    app.register_blueprint(transaction_router)


    @app.before_request
    def before_request():
        print("BEFORE REQUEST")
        print(request.method)
        auth_middleware()


    @app.after_request
    def after_request(response):
        request_id = str(uuid.uuid4())
        response.headers["X-Request-ID"] = request_id
        return response


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404



    @app.route("/")
    def index():
        return render_template("index.html")

    return app