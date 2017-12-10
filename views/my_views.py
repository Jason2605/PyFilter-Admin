from flask import render_template, jsonify, request, session, redirect, url_for
from pyfilter_admin import app, header_array, database, ip_regex, login_db, settings
from datetime import datetime, timedelta
from passlib.hash import bcrypt
from functools import wraps
import time


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        return redirect(url_for("index"))
    return decorated_function


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login/", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if not (username and password):
        redirect(url_for("index"))

    cur = login_db.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    password_hash = cur.fetchone()

    if not password_hash:
        return redirect(url_for("index"))

    if bcrypt.verify(password, password_hash[0]):
        session["logged_in"] = True
        session["username"] = username
        return redirect(url_for("home"))
    return redirect(url_for("index"))


@app.route("/logout/")
@login_required
def logout():
    del session["logged_in"]
    return redirect(url_for("index"))


@app.route("/profile/")
@login_required
def profile():
    return render_template("profile.html", header_array=header_array)


@app.route("/profile/password/", methods=["POST"])
@login_required
def change_password():
    password = request.form["password"]
    password_confirm = request.form["password-confirm"]

    if not (password and password_confirm):
        return jsonify(status=401, error="Please enter all fields!")

    if password != password_confirm:
        return jsonify(status=401, error="Passwords do not match!")

    password_hash = bcrypt.hash(password)

    cur = login_db.cursor()
    cur.execute("UPDATE users SET password = ? WHERE username = ?", (password_hash, session["username"]))
    cur.close()
    login_db.commit()

    return jsonify(status=200, message="Password changed!")


@app.route("/home/")
@login_required
def home():
    is_redis = database[0] == "redis"
    if is_redis:
        bans = [x.split() for x in database[1].lrange("latest_10_keys", 0, 9)]
        amount, total_bans = scan(database[1])
        # amount = 6
        # total = 61
    else:
        sql = "SELECT ip, server_name, time_banned FROM banned_ip" \
              " WHERE time_banned > {} ORDER BY id DESC".format(time.time() - 864000)
        cur = database[1].cursor()
        cur.execute(sql)
        bans_last_10 = cur.fetchall()

        sql_amount = "SELECT COUNT(id) FROM banned_ip"
        cur.execute(sql_amount)
        total_bans = cur.fetchone()[0]

        bans = bans_last_10[-10:]
        amount = len(bans_last_10)

    return render_template("home.html",
                           header_array=header_array,
                           bans=bans,
                           amount=amount,
                           total=total_bans,
                           is_redis=is_redis)


@app.route("/info/", methods=["POST"])
@login_required
def info():

    ip = request.form["ip"]
    server = request.form["name"]
    if database[0] == "redis":
        reason = database[1].hget(ip, "reason")
        time_banned = database[1].hget(ip, server)
    else:
        sql = "SELECT time_banned, server_name, log_msg FROM banned_ip WHERE ip = ?"
        cur = database[1].cursor()
        cur.execute(sql, (ip,))
        time_banned, server, reason = cur.fetchone()
        cur.close()

    return jsonify(status=200, ip=ip, server=server, time_banned=time_banned, reason=reason)


@app.route("/ban/add/", methods=["POST"])
@login_required
def add_ban():
    ip = request.form["ip"]
    reason = request.form["reason"]

    if database[0] != "redis":
        return jsonify(status=501, error="Adding bans is currently only supported for Redis!")

    if not (ip and reason):
        return jsonify(status=400, error="Please input both a reason and an IP address!")

    if not ip_regex.match(ip):
        return jsonify(status=400, error="Please enter a valid IP address!")

    if ip in settings["ignored_ips"]:
        return jsonify(status=400, error="This IP cannot be banned!")

    if database[1].hkeys(ip):
        return jsonify(status=400, error="IP address already banned!")

    time_banned = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = "PyFilter-Admin"

    database[1].lpush("latest_10_keys", "{} {}".format(ip, name))
    database[1].ltrim("latest_10_keys", 0, 9)

    database[1].hmset(ip, {
        name: time_banned,
        "reason": reason,
        "banned_server": name
    })

    return jsonify(status=200, message="IP {} has been banned!".format(ip))


def scan(redis_connection):
    amount = 0
    total = 0
    time_now = datetime.now()

    for result in redis_connection.scan_iter():
        if redis_connection.type(result) != "hash":
            continue

        total += 1

        server = redis_connection.hget(result, "banned_server")
        time_banned = redis_connection.hget(result, server)

        if time_banned is None:
            continue

        try:
            time_banned = datetime.strptime(time_banned, "%Y-%m-%d %H:%M:%S")  # "2017-12-02 17:31:38"
        except ValueError:
            continue

        if time_banned - time_now >= timedelta(days=10):
            print(time_banned - time_now)
            continue

        amount += 1

    return amount, total
