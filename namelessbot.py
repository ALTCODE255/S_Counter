import os
import sys
from datetime import datetime
from textwrap import dedent

import tweepy
from dotenv import load_dotenv

from db_functions import addNewDayRow, getCount, getStatistics


def getTweetText() -> str:
    today = datetime.now().strftime("%m/%d/%Y")
    overall_stats = getStatistics()
    s1_stats = overall_stats[0]
    s2_stats = overall_stats[1]
    s1 = getCount("Shuuen")
    s2 = getCount("Sonic")
    text = dedent(f"""\
                  #namelessbot [{today}]
                  Nameless said "Shuuen" {s1} time{'' if s1 == 1 else 's'} and "Sonic" {s2} time{'' if s2 == 1 else 's'} today.

                  ["Shuuen" Stats]
                  - Total: {s1_stats["SUM"]}
                  - Average: {s1_stats["AVG"]}
                  - Personal Best: {s1_stats["MAX"]}

                  ["Sonic" Stats]
                  - Total: {s2_stats["SUM"]}
                  - Average: {s2_stats["AVG"]}
                  - Personal Best: {s2_stats["MAX"]}""")
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
    addNewDayRow()
