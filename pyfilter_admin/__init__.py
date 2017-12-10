import json
import re
import os
from datetime import timedelta
from flask import Flask
import sqlite3

with open("config.json") as config:
    data = json.load(config)

settings = data["settings"]

create = os.path.exists("PyFilter-Admin.db")

login_db = sqlite3.connect("PyFilter-Admin.db", check_same_thread=False)

if not create:
    cur = login_db.cursor()
    cur.execute("CREATE TABLE users (username text PRIMARY KEY, password text)")
    cur.execute("INSERT INTO users VALUES (?, ?)",
                ("PyFilter", "$2b$12$umkgxD0lM96gBAOx6yYIIOysnsED.Fs5vBb4KOH0fBr1dC2Vo5xHy")
                )
    cur.close()
    login_db.commit()

    with open("key.txt", "wb") as f:
        f.write(os.urandom(24))  # Create secret key for flask sessions

with open("key.txt", "rb") as f:
    key = f.readline()

if settings["database"] == "redis":
    from redis import Redis

    db_info = data["redis"]
    database = ["redis", Redis(host=db_info["host"],
                               password=db_info["password"],
                               db=db_info["database"],
                               decode_responses=True)]
else:

    db_info = data["sqlite"]
    database = ["sqlite", sqlite3.connect(db_info["database"], check_same_thread=False)]

# URL, Text, Icon
header_array = [
    ["/home/", "Dashboard", "dashboard"],
    ["/profile/", "Profile", "person"],
    ["/logout/", "Logout", "input"]
]

ip_regex = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")

time = 30 if settings["debug"] else 10

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=time)
app.config["SECRET_KEY"] = key



from views import my_views