import sys
import os

import requests
from dotenv import load_dotenv
from plyer import notification


def updateCount(inc_col: str):
    response = requests.post(
        os.getenv("URL") + "/increment",
        headers={
            "Authorization": os.getenv("HEADER_AUTH"),
            "inc-col": inc_col
        },
        verify="cert.pem",
    )
    count = response.content.decode("utf-8")
    notification.notify(title="Counted!", message=f"{inc_col}: {count}", timeout=1)


if __name__ == "__main__":
    load_dotenv()
    updateCount(sys.argv[1])
