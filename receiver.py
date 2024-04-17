import os

from dotenv import load_dotenv
from flask import Flask

from db_functions import getCount, incCounter

app = Flask(__name__)


@app.route('/sonic')
def incrementSonic():
    incCounter("Sonic", 1)
    return str(getCount("Sonic"))


@app.route('/shuuen')
def incrementShuuen():
    incCounter("Shuuen", 1)
    return str(getCount("Shuuen"))


if __name__ == '__main__':
    load_dotenv()
    app.run(port=os.getenv("PORT"), host=os.getenv("HOST"))
