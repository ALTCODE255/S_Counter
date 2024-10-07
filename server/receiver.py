import os

from dotenv import dotenv_values, load_dotenv
from flask import Flask, request
from flask_httpauth import HTTPTokenAuth
from werkzeug.middleware.proxy_fix import ProxyFix

from db_functions import getCount, incCounter

app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")
load_dotenv()
config = dotenv_values()
app.config.from_mapping(config)


@auth.verify_token
def verify_token(token):
    if token == config.get("TOKEN"):
        return True


@app.route("/increment", methods=["POST"])
@auth.login_required
def increment():
    word = request.headers["inc-col"]
    incCounter(word, 1)
    return str(getCount(word))


@app.route("/get_count/<col>", methods=["GET"])
@auth.login_required
def get_count(col):
    return str(getCount(col))


if __name__ == "__main__":
    from waitress import serve

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    serve(app, port=os.getenv("PORT"), host=os.getenv("HOST"))
