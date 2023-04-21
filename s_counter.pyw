import keyboard
import os
import pygsheets
from datetime import date, datetime, timedelta
from PIL import Image
from plyer import notification
from pystray import Icon, Menu, MenuItem
from string import printable


gc = pygsheets.authorize(service_file="gsheets.json")
sh = gc.open("The Sheet of Series that Start with S")
wks = sh[0]


def rowGet() -> str:
    # grab row # of current date
    initial_date = date(2020, 8, 22)
    today = datetime.now() + timedelta(minutes=5)
    delta = today.date() - initial_date
    return str(delta.days + 4)


def getCount(col: str) -> int:
    return int(
        wks.get_value(
            col + rowGet(),
            value_render=pygsheets.ValueRenderOption.UNFORMATTED_VALUE,
        )
    )


def incCounter(counter):
    if counter == "Sonic":
        column = "C"
    elif counter == "Shuuen":
        column = "B"
    cell = column + rowGet()
    current_value = getCount(column)
    wks.update_value(cell, current_value + 1)
    notification.notify(
        title="Counted!",
        app_name="s_counter.pyw",
        message=f"{counter}: {current_value + 1}",
        app_icon="icon.ico",
        timeout=1
    )



s1_list = ["sonic", "Sonic", "SONIC"]
s2_list = ["shuuen", "Shuuen", "SHUUEN"]

for sonic in s1_list:
    keyboard.add_word_listener(
        sonic, lambda: incCounter("Sonic"), triggers=["space", "enter"] + [*printable], match_suffix=True
    )
for shuuen in s2_list:
    keyboard.add_word_listener(
        shuuen, lambda: incCounter("Shuuen"), triggers=["space", "enter"] + [*printable],
        match_suffix=True
    )

keyboard.add_hotkey("alt+1", lambda: incCounter("Sonic"))
keyboard.add_hotkey("alt+2", lambda: incCounter("Shuuen"))


icon = Icon(
    name="Code",
    icon=Image.open("icon.ico"),
    title="S Counter",
    menu=Menu(
        MenuItem("Restart", lambda: os.system("s_counter.bat")),
        MenuItem("Exit", lambda: os.system("taskkill /f /IM pythonw3.11.exe"))
    )
)
icon.run()
keyboard.wait()
