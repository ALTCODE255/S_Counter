import os
from itertools import product
from string import printable

import keyboard
import paramiko
from dotenv import load_dotenv
from PIL import Image
from pystray import Icon, Menu, MenuItem
from plyer import notification

load_dotenv()


def updateCount(inc_col: str) -> str:
    HOST = os.getenv("EXTERNAL_IP")
    PASS = os.getenv("PI_PASS")
    PORT = os.getenv("PI_PORT")
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, PORT, username="pi", password=PASS)
    _stdin, _stdout, _stderr = client.exec_command(
        f"cd Projects/S_Counter && python db_functions.py {inc_col}"
    )
    count = _stdout.read().decode()
    client.close()
    return count


def showUpdateToast(col: str):
    new_value = updateCount(col)
    notification.notify(title="Counted!", message=f"{col}: {new_value}", timeout=2)


sonic = list(map("".join, product(*zip("sonic".upper(), "sonic".lower()))))
shuuen = list(map("".join, product(*zip("shuuen".upper(), "shuuen".lower()))))

for case in sonic:
    keyboard.add_word_listener(
        case,
        lambda: showUpdateToast("Sonic"),
        triggers=["space", "enter"] + list(printable.strip()),
        match_suffix=True,
    )
for case in shuuen:
    keyboard.add_word_listener(
        case,
        lambda: showUpdateToast("Shuuen"),
        triggers=["space", "enter"] + list(printable.strip()),
        match_suffix=True,
    )

keyboard.add_hotkey("alt+1", lambda: showUpdateToast("Sonic"))
keyboard.add_hotkey("alt+2", lambda: showUpdateToast("Shuuen"))


icon = Icon(
    name="Code",
    icon=Image.open("icon.ico"),
    title="S Counter",
    menu=Menu(
        MenuItem("Restart", lambda: os.system("s_counter.bat")),
        MenuItem("Exit", lambda: os.system("taskkill /f /IM pythonw3.11.exe")),
    ),
)
icon.run()
keyboard.wait()
