import sys
import os

import urllib.request
from dotenv import load_dotenv
from plyer import notification


def updateCount(inc_col: str):
    response = urllib.request.urlopen(os.getenv("URL") + inc_col.lower())
    count = response.read().decode("utf-8")
    notification.notify(
        title="Counted!", message=f"{inc_col}: {count}", timeout=1
    )


if __name__ == "__main__":
    load_dotenv()
    updateCount(sys.argv[1])
