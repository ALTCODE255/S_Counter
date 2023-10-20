import os
import sqlite3
import sys
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv
from homeassistant_api import Client


def getCount(col: str) -> int:
    sqliteConnection = sqlite3.connect(os.getenv("DIR_PATH") + "counter.db")
    cursor = sqliteConnection.cursor()
    cursor.execute(f"SELECT {col} FROM S_Counter ORDER BY Date DESC LIMIT 1")
    current_count = int(cursor.fetchall()[0][0])
    cursor.close()
    sqliteConnection.close()
    return current_count


def incCounter(col: str, num: int):
    sqliteConnection = sqlite3.connect(os.getenv("DIR_PATH") + "counter.db")
    cursor = sqliteConnection.cursor()
    cursor.execute(
        f"UPDATE S_Counter SET {col} = {col} + {num} WHERE Date = (SELECT MAX(Date) FROM S_Counter)"
    )
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()
    updateHomeAssistant()


def getStatistics() -> tuple[dict]:
    sqliteConnection = sqlite3.connect(os.getenv("DIR_PATH") + "counter.db")
    cursor = sqliteConnection.cursor()
    cursor.execute(
                    """SELECT
                        SUM(Shuuen), ROUND(AVG(Shuuen), 2), MAX(Shuuen),
                        SUM(Sonic), ROUND(AVG(Sonic), 2), MAX(Sonic)
                    FROM S_Counter"""
    )
    values_tuple = cursor.fetchone()
    cursor.close()
    sqliteConnection.close()
    return (
        {
            "Word": "Shuuen",
            "SUM": values_tuple[0],
            "AVG": values_tuple[1],
            "MAX": values_tuple[2],
        },
        {
            "Word": "Sonic",
            "SUM": values_tuple[3],
            "AVG": values_tuple[4],
            "MAX": values_tuple[5],
        },
    )


def addNewDayRow():
    today = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d")
    sqliteConnection = sqlite3.connect(os.getenv("DIR_PATH") + "counter.db")
    cursor = sqliteConnection.cursor()
    try:
        cursor.execute(f"INSERT INTO S_Counter (Date) VALUES ('{today}')")
    except sqlite3.IntegrityError:
        pass
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()
    updateHomeAssistant()


def updateHomeAssistant():
    load_dotenv()
    requests.packages.urllib3.disable_warnings()
    with Client(
        os.getenv("INTERNAL_IP"), os.getenv("HA_TOKEN"), verify_ssl=False
    ) as client:
        counter = client.get_domain("input_number")
        counter.set_value(
            value=getCount("Shuuen"), entity_id="input_number.shuuen_counter"
        )
        counter.set_value(
            value=getCount("Sonic"), entity_id="input_number.sonic_counter"
        )


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        num = sys.argv[2] if len(sys.argv) > 2 else 1
        incCounter(sys.argv[1], num)
        print(getCount(sys.argv[1]))
