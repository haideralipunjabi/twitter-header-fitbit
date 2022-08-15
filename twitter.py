from itertools import count
from turtle import dot
from unittest import skip
import tweepy
import dotenv
import os

dotenv.load_dotenv()

class TwitterAPI():
    def __init__(self) -> None:
        auth = tweepy.OAuthHandler(consumer_key=os.getenv('CONSUMER_KEY'), consumer_secret=os.getenv('CONSUMER_SECRET'))
        auth.set_access_token(key=os.getenv('ACCESS_TOKEN'), secret=os.getenv('ACCESS_TOKEN_SECRET'))
        self.api = tweepy.API(auth)

    def get_followers(self):
        followers = self.api.get_followers(count=5, skip_status=True)
        return [follower.profile_image_url_https for follower in followers]
    
    def update_header(self,fp):
        self.api.update_profile_banner(fp)

if __name__ == "__main__":
    t = TwitterAPI()
    print(t.get_followers())