import requests
from config import news_api_key
from slack_message import SlackMessage

sm = SlackMessage()


class News:
    def get_news(self, key, id):
        url = f"http://newsapi.org/v2/everything?q={key}&sortBy=publishedAt&apiKey={news_api_key}"
        response = requests.get(url)
        response = response.json()
        if response["status"] == "ok":
            for i in range(5):
                news = response["articles"][i]
                sm.sendMessageBlock(
                    id,
                    news["title"],
                    news["description"],
                    news["url"],
                    news["urlToImage"],
                )


# if __name__ == "__main__":
    # news = News()
    # news.get_news("technology")

