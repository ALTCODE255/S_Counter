from itertools import product
from string import printable
import sys

import keyboard
import paramiko
from dotenv import load_dotenv
from PIL import Image
from pystray import Icon, Menu, MenuItem
from plyer import notification

load_dotenv()


def updateCount(inc_col: str) -> str:
    HOST = os.getenv("EXTERNAL_IP")
    PORT = os.getenv("PI_PORT")
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, PORT, username="pi", key_filename="pi_key")
    _stdin, _stdout, _stderr = client.exec_command(
        f"cd Projects/S_Counter && python db_functions.py {inc_col}"
    )
    count = _stdout.read().decode()
    client.close()
    return count


def showUpdateToast(col: str):
    new_value = updateCount(col)
    notification.notify(
        title="Counted!", message=f"{col}: {new_value}", app_icon="icon.ico", timeout=2
    )


def restartSelf():
    icon.stop()
    os.execv(sys.executable, ['python'] + sys.argv)


def killSelf():
    icon.stop()
    os._exit(0)


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

keyboard.add_hotkey("ctrl+alt+1", lambda: showUpdateToast("Sonic"))
keyboard.add_hotkey("ctrl+alt+2", lambda: showUpdateToast("Shuuen"))


icon = Icon(
    name="Code",
    icon=Image.open("icon.ico"),
    title="S Counter",
    menu=Menu(
        MenuItem("Restart", lambda: restartSelf()),
        MenuItem("Exit", lambda: killSelf()),
    ),
)
icon.run()
keyboard.wait()
