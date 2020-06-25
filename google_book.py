from threading import Timer
from config import google_book_key
import requests,json
import os

class GoogleBook():
    oneDayTimer = 24 * 60 * 60
    def readBookPerDay(self):
        self.getBookContent()
        # Timer(self.oneDayTimer,self.readBookPerDay)


    def getBookContent(self):
        book_url = "https://www.googleapis.com/books/v1/volumes?q=flowers+inauthor:keyes&filter=full&key="+google_book_key
        book_response = requests.get(book_url)  
        book_json = book_response.json()
        print(book_json)


if __name__ == "__main__":
    google_book = GoogleBook()
    google_book.readBookPerDay()