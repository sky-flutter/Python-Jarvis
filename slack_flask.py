from slackeventsapi import SlackEventAdapter
from config import slack_signin_token, slack_token
from flask import Flask
from weather import Weather
from db import DbOperation
from news import News
import wikipedia
import datetime
from slack_message import SlackMessage

app = Flask(__name__)
_news = News()
db_op = DbOperation()
slack_message = SlackMessage()
weather = Weather()


@app.route("/")
def hello():
    return "Hello"


slack_events_adapter = SlackEventAdapter(
    slack_signin_token, endpoint="/slack/events", server=app
)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        return "Good Morning"
    elif hour >= 12 and hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"


@slack_events_adapter.on("message")
def handle_message(event_data):
    print(event_data)

    if event_data is not None:
        try:
           botid = event_data['event']['bot_id'] 
        except Exception as e:
            channel_id = event_data["event"]["channel"]
            payload = (event_data["event"]["text"]).lower()
            user_id = event_data["event"]["user"]
            if "current weather" == payload:
                result = weather.getLocationKey()
                slack_message.sendMessage(channel_id, result)
            elif "news" in payload:
                payload = payload.replace('news','')
                _news.get_news(payload,channel_id)
            elif "wish me" == payload:
                slack_message.sendMessage(channel_id, wishMe())

if __name__ == "__main__":
    app.run(port=3000)
