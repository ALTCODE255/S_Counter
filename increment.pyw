import sys
import os

import paramiko
from dotenv import load_dotenv
from plyer import notification


def connectSSH() -> paramiko.client.SSHClient:
    HOST = os.getenv("EXTERNAL_IP")
    PORT = os.getenv("PI_PORT")
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, PORT, username="pi", key_filename="pi_key")
    return client


def updateCount(inc_col: str):
    _stdin, _stdout, _stderr = client.exec_command(
        "python Projects/S_Counter/db_functions.py " + inc_col
    )
    count = _stdout.read().decode()
    notification.notify(
        title="Counted!", message=f"{inc_col}: {count}", timeout=1
    )


if __name__ == "__main__":
    load_dotenv()
    client = connectSSH()
    updateCount(sys.argv[1])
