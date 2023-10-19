import sqlite3
from datetime import datetime, timedelta


def getCount(col: str) -> int:
    today = (datetime.now() + timedelta(minutes=5)).strftime('%Y-%m-%d')
    sqliteConnection = sqlite3.connect("counter.db")
    cursor = sqliteConnection.cursor()
    cursor.execute(f"SELECT {col} FROM S_Counter WHERE Date = '{today}'")
    current_count = int(cursor.fetchall()[0][0])
    cursor.close()
    sqliteConnection.close()
    return current_count


def incCounter(col: str):
    today = (datetime.now() + timedelta(minutes=5)).strftime('%Y-%m-%d')
    sqliteConnection = sqlite3.connect("counter.db")
    cursor = sqliteConnection.cursor()
    cursor.execute(f"UPDATE S_Counter SET {col} = {col} + 1 WHERE Date = '{today}'")
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()


def getStatistics() -> tuple[dict]:
    sqliteConnection = sqlite3.connect("counter.db")
    cursor = sqliteConnection.cursor()
    cursor.execute('''SELECT
                        SUM(Shuuen), ROUND(AVG(Shuuen), 2), MAX(Shuuen),
                        SUM(Sonic), ROUND(AVG(Sonic), 2), MAX(Sonic)
                    FROM S_Counter''')
    values_tuple = cursor.fetchone()
    cursor.close()
    sqliteConnection.close()
    return (
            {"Word": "Shuuen",
             "SUM": values_tuple[0],
             "AVG": values_tuple[1],
             "MAX": values_tuple[2]},
            {"Word": "Sonic",
             "SUM": values_tuple[3],
             "AVG": values_tuple[4],
             "MAX": values_tuple[5]}
        )


def addNewDayRow():
    today = (datetime.now() + timedelta(minutes=5)).strftime('%Y-%m-%d')
    sqliteConnection = sqlite3.connect("counter.db")
    cursor = sqliteConnection.cursor()
    try:
        cursor.execute(f"INSERT INTO S_Counter (Date) VALUES ('{today}')")
    except sqlite3.IntegrityError:
        pass
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()
