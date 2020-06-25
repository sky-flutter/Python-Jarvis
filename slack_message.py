import os
from slack import WebClient
from config import slack_token
from slack.errors import SlackApiError


webclient = WebClient(token=slack_token)

class SlackMessage:
    def sendMessage(self,id,message):
        try:
            response = webclient.chat_postMessage(
                channel=id,
                text=message
            )
            return "Message sent!"
        except SlackApiError as e:
            return "Error in sending message"
    
    def sendMessageBlock(self,id,title,content,url,image):
        message = "[{'type': 'section','text': {'type': 'mrkdwn','text': '*{title}*\n{url}'}},{'type': 'section','text': {'type': 'mrkdwn','text': '{content}'}},{'type': 'image','title': {'type': 'plain_text'},'image_url': '{image}','alt_text': 'No Image'}]"
        try:
            response = webclient.chat_postMessage(
                channel=id,
                blocks=message
            )
            return "Message sent!"
        except SlackApiError as e:
            return "Error in sending message"


    