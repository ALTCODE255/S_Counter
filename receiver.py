import os

from dotenv import dotenv_values, load_dotenv
from flask import Flask
from flask_httpauth import HTTPBasicAuth

from db_functions import getCount, incCounter


app = Flask(__name__)
auth = HTTPBasicAuth()
load_dotenv()
config = dotenv_values()
app.config.from_mapping(config)


@auth.verify_password
def verify_password(username, password):
    if username == app.config["USER"] and password == app.config["PASSWORD"]:
        return username


@app.route("/sonic")
@auth.login_required
def incrementSonic():
    incCounter("Sonic", 1)
    return str(getCount("Sonic"))


@app.route("/shuuen")
@auth.login_required
def incrementShuuen():
    incCounter("Shuuen", 1)
    return str(getCount("Shuuen"))


if __name__ == "__main__":
    app.run(port=os.getenv("PORT"), host=os.getenv("HOST"))
