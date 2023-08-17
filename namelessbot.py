import os
import tweepy
import ezsheets
from dotenv import load_dotenv

load_dotenv()

client = tweepy.Client(
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
)

s = ezsheets.Spreadsheet("1VyD1fDG6noKldoNCQIhoGNAX7cTwuP8HAI0PViik0k0")
wks = s[1]


def getStats() -> str:
    return wks.get("A2")


client.create_tweet(text=getStats())
