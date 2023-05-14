import os
from datetime import date, datetime, timedelta
from itertools import product
from string import printable

import ezsheets
import keyboard
from PIL import Image
from plyer import notification
from pystray import Icon, Menu, MenuItem

s = ezsheets.Spreadsheet("1VyD1fDG6noKldoNCQIhoGNAX7cTwuP8HAI0PViik0k0")
wks = s[0]


def rowGet() -> str:
    # grab row # of current date
    initial_date = date(2020, 8, 22)
    today = datetime.now() + timedelta(minutes=5)
    delta = today.date() - initial_date
    return delta.days + 3


def getCount(col: int) -> int:
    wks.refresh()
    return int(wks.get(col, rowGet()))


def incCounter(counter: str):
    if counter == "Sonic":
        column = 3
    elif counter == "Shuuen":
        column = 2
    current_value = getCount(column)
    wks.update(column, rowGet(), current_value + 1)
    notification.notify(
        title="Counted!",
        app_name="s_counter.pyw",
        message=f"{counter}: {current_value + 1}",
        app_icon="icon.ico",
        timeout=1,
    )


sonic = list(map("".join, product(*zip("sonic".upper(), "sonic".lower()))))
shuuen = list(map("".join, product(*zip("shuuen".upper(), "shuuen".lower()))))

for case in sonic:
    keyboard.add_word_listener(
        case,
        lambda: incCounter("Sonic"),
        triggers=["space", "enter"] + [*printable],
        match_suffix=True,
    )
for case in shuuen:
    keyboard.add_word_listener(
        case,
        lambda: incCounter("Shuuen"),
        triggers=["space", "enter"] + [*printable],
        match_suffix=True,
    )

keyboard.add_hotkey("alt+1", lambda: incCounter("Sonic"))
keyboard.add_hotkey("alt+2", lambda: incCounter("Shuuen"))


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
