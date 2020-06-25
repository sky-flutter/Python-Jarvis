import sqlite3
from config import slack_url, slack_user_list, slack_token
import requests

session = requests.Session()
session.headers.update({"Authorization": "Bearer {0}".format(slack_token)})
con = sqlite3.connect("slack_data.db")

cursor = con.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS tbl_slack_users(id text, name text,real_name text,title text,phone real)"
)
con.commit()


class DbOperation:
    def get_users(self):
        response = session.get(slack_url + slack_user_list)
        response = response.json()

        if response["ok"] == True:
            for members in response["members"]:
                self.add_users_todb(members)
            con.commit()

    def add_users_todb(self, members):
        try:
            id = members["id"]
            name = members["name"]
            realName = members["profile"]["real_name"]
            title = members["profile"]["title"]
            phone = members["profile"]["phone"]
            if realName is None or realName == "":
                realName = "No Name"
            if title is None or title == "":
                title = "No Title"
            if phone is None or phone == "":
                phone = "0000000000"

            strQuery = f"INSERT INTO tbl_slack_users VALUES('{id}','{name}','{realName}','{title}','{phone}')"
            cursor.execute(strQuery)
        except Exception as e:
            print(e)

    def get_user_id(self, name):
        str_query = f"SELECT * FROM tbl_slack_users WHERE real_name LIKE '%{name}%'"
        rows = cursor.execute(str_query)
        row = rows.fetchone()
        try:
            return row[0]
        except:
            return None

    def get_full_name(self, name):
        str_query = f"SELECT * FROM tbl_slack_users WHERE id = '{name}'"
        rows = cursor.execute(str_query)
        row = rows.fetchone()
        try:
            return row[2]
        except:
            return None

if __name__ == "__main__":
    db = DbOperation()
    # db.get_users()
    db.get_full_name("UGL78UZRR")
