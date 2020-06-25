import os
from dotenv import load_dotenv
load_dotenv(".env")

weather_key = os.getenv("WEATHER_API_KEY")
google_book_key = os.getenv("GOOGLE_BOOK_API_KEY")
slack_token = os.getenv("SLACK_TOKEN")
slack_signin_token = os.getenv("SLACK_SIGNIN_TOKEN")
slack_url = os.getenv("SLACK_URL")
slack_user_list = os.getenv("SLACK_USER_LIST")
news_api_key = os.getenv("NEWS_API_KEY")