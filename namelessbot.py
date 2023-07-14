import tweepy
import ezsheets
import json

with open("creds.json") as credentials:
    keys = json.load(credentials)

client = tweepy.Client(
    consumer_key=keys["consumer_key"],
    consumer_secret=keys["consumer_secret"],
    access_token=keys["access_token"],
    access_token_secret=keys["access_token_secret"],
)

s = ezsheets.Spreadsheet("1VyD1fDG6noKldoNCQIhoGNAX7cTwuP8HAI0PViik0k0")
wks = s[1]


def getStats() -> str:
    return wks.get("A2")


client.create_tweet(text=getStats())
