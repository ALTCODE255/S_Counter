import os
import sqlite3
import sys
from contextlib import closing
from datetime import datetime
from textwrap import dedent

import tweepy
from dotenv import load_dotenv


def getData() -> tuple[tuple[int], tuple[int]]:
    with closing(sqlite3.connect("counter.db")) as conn, conn:
        conn.row_factory = sqlite3.Row
        conn.execute("INSERT OR IGNORE INTO S_Counter DEFAULT VALUES")
        s1 = conn.execute(
            """
                SELECT (
                    SELECT Shuuen FROM S_Counter
                    WHERE DATE = date('now', 'localtime')
                ) AS last,
                    SUM(Shuuen) AS sum,
                    ROUND(AVG(Shuuen), 2) AS avg,
                    MAX(Shuuen) AS max
                FROM S_Counter"""
        ).fetchone()
        s2 = conn.execute(
            """
                SELECT (
                    SELECT Sonic FROM S_Counter
                    WHERE DATE = date('now', 'localtime')
                ) AS last,
                    SUM(Sonic) AS sum,
                    ROUND(AVG(Sonic), 2) AS avg,
                    MAX(Sonic) AS max
                FROM S_Counter"""
        ).fetchone()
        return (s1, s2)


def getTweetText() -> str:
    today = datetime.now().strftime("%Y/%m/%d")
    s1, s2 = getData()
    text = dedent(
        f"""\
                  #namelessbot [{today}]
                  Nameless said "Shuuen" {s1['last']} time{'' if s1['last'] == 1 else 's'} and "Sonic" {s2['last']} time{'' if s2['last'] == 1 else 's'} today.

                  ["Shuuen" Stats]
                  - Total: {s1['sum']}
                  - Average: {s1['avg']}
                  - Personal Best: {s1['max']}

                  ["Sonic" Stats]
                  - Total: {s2['sum']}
                  - Average: {s2['avg']}
                  - Personal Best: {s2['max']}"""
    )
    return text


if __name__ == "__main__":
    os.chdir(sys.path[0])
    load_dotenv()

    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )
    client.create_tweet(text=getTweetText())