import tweepy
import pygsheets
import json
import os

directory = os.path.realpath(os.path.dirname(__file__))

with open(directory + "/creds.json") as credentials:
    keys = json.load(credentials)

client = tweepy.Client(consumer_key=keys["consumer_key"], consumer_secret=keys["consumer_secret"], access_token=keys["access_token"], access_token_secret=keys["access_token_secret"])

gc = pygsheets.authorize(service_file=directory + "/gsheets.json")
sh = gc.open("The Sheet of Series that Start with S")
wks = sh[1]


def getStats() -> str:
    return wks.get_value("B2", value_render=pygsheets.ValueRenderOption.UNFORMATTED_VALUE)


client.create_tweet(text=getStats())
