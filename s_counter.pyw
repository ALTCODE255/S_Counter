import os
from db_functions import getCount, incCounter
from itertools import product
from string import printable

import keyboard
from PIL import Image
from pystray import Icon, Menu, MenuItem
from win10toast import ToastNotifier

toaster = ToastNotifier()


def increment(col: str):
    incCounter(col)
    showUpdateToast(col)


def showUpdateToast(col: str):
    new_value = getCount(col)
    toaster.show_toast(
        "Counted!",
        f"{col}: {new_value}",
        threaded=True,
        icon_path=None,
        duration=1,
    )


sonic = list(map("".join, product(*zip("sonic".upper(), "sonic".lower()))))
shuuen = list(map("".join, product(*zip("shuuen".upper(), "shuuen".lower()))))

for case in sonic:
    keyboard.add_word_listener(
        case,
        lambda: increment("Sonic"),
        triggers=["space", "enter"] + list(printable.strip()),
        match_suffix=True,
    )
for case in shuuen:
    keyboard.add_word_listener(
        case,
        lambda: increment("Shuuen"),
        triggers=["space", "enter"] + list(printable.strip()),
        match_suffix=True,
    )

keyboard.add_hotkey("alt+1", lambda: increment("Sonic"))
keyboard.add_hotkey("alt+2", lambda: increment("Shuuen"))


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
