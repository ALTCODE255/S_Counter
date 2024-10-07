import os
import sqlite3
from contextlib import closing

from dotenv import dotenv_values, load_dotenv
from flask import Flask, request
from flask_httpauth import HTTPTokenAuth
from werkzeug.middleware.proxy_fix import ProxyFix

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
def incCount():
    req_data = request.get_json()
    if req_data["s_word"] in ("Sonic", "Shuuen") and req_data.get("amount"):
        with closing(sqlite3.connect("counter.db")) as conn, conn:
            conn.execute("INSERT OR IGNORE INTO S_Counter DEFAULT VALUES")
            result = conn.execute(
                f"UPDATE S_Counter \
                  SET {req_data['s_word']} = {req_data['s_word']} + {req_data['amount']} \
                  WHERE Date = date('now', 'localtime') \
                  RETURNING {req_data['s_word']}"
            ).fetchone()[0]
            return str(result)
    else:
        return "Invalid body params. Please include valid 's_word' and 'amount'."


@app.route("/get_count/<col>", methods=["GET"])
@auth.login_required
def getCount(col: str):
    if col in ("Sonic", "Shuuen"):
        with closing(sqlite3.connect("counter.db")) as conn, conn:
            conn.execute("INSERT OR IGNORE INTO S_Counter DEFAULT VALUES")
            result = conn.execute(
                f"SELECT {col} \
                  FROM S_Counter \
                  WHERE Date = date('now', 'localtime')"
            ).fetchone()[0]
        return str(result)
    else:
        return f"Invalid URL param /get_count/{col}"


if __name__ == "__main__":
    from waitress import serve

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    serve(app, port=os.getenv("PORT"), host="0.0.0.0")
