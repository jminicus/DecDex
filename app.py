import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required

# Configure application
app = Flask(__name__)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///decdex.db")


@app.route("/")
@login_required
def index():
    """Show homepage"""

    # query db for users name
    rows = db.execute("SELECT name FROM users WHERE id = :id", id=session["user_id"])
    for row in rows:
        name = row['name']

    # load page with users full name displayed
    return render_template("homepage.html", name=name)


@app.route("/newlog", methods=["GET", "POST"])
@login_required
def newlog():
    """Shows newlog page"""

    # if form submitted, enter new log into db and reload page
    if request.method == "POST":
        db.execute("INSERT INTO logs (user_id, date, events, rating, good, bad) VALUES (:user_id, :date, :events, :rating, :good, :bad)",
        user_id=session["user_id"], date=request.form.get("date"), events=request.form.get("events"), rating=request.form.get("rate"), good=request.form.get("good"), bad=request.form.get("bad"))
        return redirect("/prevlogs")

    # load page
    else:
        return render_template("newlog.html")


@app.route("/prevlogs", methods=["GET", "POST"])
@login_required
def prevlogs():
    """Shows previous logs page"""

    if request.method == "POST":

        # delete the selected log from db
        db.execute("DELETE FROM logs WHERE user_id = :user_id AND id = :id", user_id=session["user_id"], id=request.form.get('remove'))

        # query for training logs in db
        logs = db.execute("SELECT * FROM logs WHERE user_id = :user_id ORDER BY date DESC", user_id=session["user_id"])

        # load page with updated data
        return render_template("prevlogs.html", logs=logs)

    else:

        # query for training logs in db
        logs = db.execute("SELECT * FROM logs WHERE user_id = :user_id ORDER BY date DESC", user_id=session["user_id"])

        # load page with data
        return render_template("prevlogs.html", logs=logs)


@app.route("/100m", methods=["GET", "POST"])
@login_required
def sprint():
    """Shows 100m page"""

    if request.method == "POST":

        # see if user already has cues stored. if yes, update cue, if no, make new cue. If user deletes cue, delete from db
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '100m'", user_id=session["user_id"])

        if len(rows) == 1:

            if request.form.get("100mcues") == "":
                db.execute("DELETE FROM cues WHERE user_id = :user_id AND event = '100m'", user_id=session["user_id"])
                text = ""
                header = "Enter Cue List"
                button = "Submit Cue"

                return render_template("100m.html", text=text, header=header, button=button)

            else:
                db.execute("UPDATE cues SET cue = :cue WHERE user_id = :user_id AND event = '100m'", user_id=session["user_id"], cue=request.form.get("100mcues"))
                rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '100m'", user_id=session["user_id"])

                text = rows[0]['cue']
                header = "Edit Cue List"
                button = "Submit Edits"

                return render_template("100m.html", text=text, header=header, button=button)

        else:
            db.execute("INSERT INTO cues (user_id, event, cue) VALUES (:user_id, :event, :cue)", user_id=session["user_id"],
            event="100m", cue=request.form.get("100mcues"))
            rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '100m'", user_id=session["user_id"])

            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

            return render_template("100m.html", text=text, header=header, button=button)

    # query for stored cue and display it, else display nothing in text field
    else:
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '100m'", user_id=session["user_id"])
        if len(rows) == 1:
            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

        else:
            text = ""
            header = "Enter Cue List"
            button = "Submit Cue"

        return render_template("100m.html", text=text, header=header, button=button)


@app.route("/longjump", methods=["GET", "POST"])
@login_required
def longjump():
    """Shows long jump page"""

    if request.method == "POST":

        # see if user already has cues stored. if yes, update cue, if no, make new cue. If user deletes cue, delete from db
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'longjump'", user_id=session["user_id"])

        if len(rows) == 1:

            if request.form.get("longjumpcues") == "":
                db.execute("DELETE FROM cues WHERE user_id = :user_id AND event = 'longjump'", user_id=session["user_id"])
                text = ""
                header = "Enter Cue List"
                button = "Submit Cue"

                return render_template("longjump.html", text=text, header=header, button=button)

            else:
                db.execute("UPDATE cues SET cue = :cue WHERE user_id = :user_id AND event = 'longjump'", user_id=session["user_id"], cue=request.form.get("longjumpcues"))
                rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'longjump'", user_id=session["user_id"])

                text = rows[0]['cue']
                header = "Edit Cue List"
                button = "Submit Edits"

                return render_template("longjump.html", text=text, header=header, button=button)

        else:
            db.execute("INSERT INTO cues (user_id, event, cue) VALUES (:user_id, :event, :cue)", user_id=session["user_id"],
            event="longjump", cue=request.form.get("longjumpcues"))
            rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'longjump'", user_id=session["user_id"])

            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

            return render_template("longjump.html", text=text, header=header, button=button)

    # query for stored cue and display it, else display nothing in text field
    else:
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'longjump'", user_id=session["user_id"])
        if len(rows) == 1:
            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

        else:
            text = ""
            header = "Enter Cue List"
            button = "Submit Cue"

        return render_template("longjump.html", text=text, header=header, button=button)


@app.route("/shotput", methods=["GET", "POST"])
@login_required
def shotput():
    """Shows shotput page"""

    if request.method == "POST":

        # see if user already has cues stored. if yes, update cue, if no, make new cue. If user deletes cue, delete from db
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'shotput'", user_id=session["user_id"])

        if len(rows) == 1:

            if request.form.get("shotputcues") == "":
                db.execute("DELETE FROM cues WHERE user_id = :user_id AND event = 'shotput'", user_id=session["user_id"])
                text = ""
                header = "Enter Cue List"
                button = "Submit Cue"

                return render_template("shotput.html", text=text, header=header, button=button)

            else:
                db.execute("UPDATE cues SET cue = :cue WHERE user_id = :user_id AND event = 'shotput'", user_id=session["user_id"], cue=request.form.get("shotputcues"))
                rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'shotput'", user_id=session["user_id"])

                text = rows[0]['cue']
                header = "Edit Cue List"
                button = "Submit Edits"

                return render_template("shotput.html", text=text, header=header, button=button)

        else:
            db.execute("INSERT INTO cues (user_id, event, cue) VALUES (:user_id, :event, :cue)", user_id=session["user_id"],
            event="shotput", cue=request.form.get("shotputcues"))
            rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'shotput'", user_id=session["user_id"])

            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

            return render_template("shotput.html", text=text, header=header, button=button)

    # query for stored cue and display it, else display nothing in text field
    else:
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'shotput'", user_id=session["user_id"])
        if len(rows) == 1:
            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

        else:
            text = ""
            header = "Enter Cue List"
            button = "Submit Cue"

        return render_template("shotput.html", text=text, header=header, button=button)


@app.route("/highjump", methods=["GET", "POST"])
@login_required
def highjump():
    """Shows high jump page"""

    if request.method == "POST":

        # see if user already has cues stored. if yes, update cue, if no, make new cue. If user deletes cue, delete from db
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'highjump'", user_id=session["user_id"])

        if len(rows) == 1:

            if request.form.get("highjumpcues") == "":
                db.execute("DELETE FROM cues WHERE user_id = :user_id AND event = 'highjump'", user_id=session["user_id"])
                text = ""
                header = "Enter Cue List"
                button = "Submit Cue"

                return render_template("highjump.html", text=text, header=header, button=button)

            else:
                db.execute("UPDATE cues SET cue = :cue WHERE user_id = :user_id AND event = 'highjump'", user_id=session["user_id"], cue=request.form.get("highjumpcues"))
                rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'highjump'", user_id=session["user_id"])

                text = rows[0]['cue']
                header = "Edit Cue List"
                button = "Submit Edits"

                return render_template("highjump.html", text=text, header=header, button=button)

        else:
            db.execute("INSERT INTO cues (user_id, event, cue) VALUES (:user_id, :event, :cue)", user_id=session["user_id"],
            event="highjump", cue=request.form.get("highjumpcues"))
            rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'highjump'", user_id=session["user_id"])

            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

            return render_template("highjump.html", text=text, header=header, button=button)

    # query for stored cue and display it, else display nothing in text field
    else:
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'highjump'", user_id=session["user_id"])
        if len(rows) == 1:
            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

        else:
            text = ""
            header = "Enter Cue List"
            button = "Submit Cue"

        return render_template("highjump.html", text=text, header=header, button=button)


@app.route("/400m", methods=["GET", "POST"])
@login_required
def mid():
    """Shows 400m page"""

    if request.method == "POST":

        # see if user already has cues stored. if yes, update cue, if no, make new cue. If user deletes cue, delete from db
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '400m'", user_id=session["user_id"])

        if len(rows) == 1:

            if request.form.get("400mcues") == "":
                db.execute("DELETE FROM cues WHERE user_id = :user_id AND event = '400m'", user_id=session["user_id"])
                text = ""
                header = "Enter Cue List"
                button = "Submit Cue"

                return render_template("400m.html", text=text, header=header, button=button)

            else:
                db.execute("UPDATE cues SET cue = :cue WHERE user_id = :user_id AND event = '400m'", user_id=session["user_id"], cue=request.form.get("400mcues"))
                rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '400m'", user_id=session["user_id"])

                text = rows[0]['cue']
                header = "Edit Cue List"
                button = "Submit Edits"

                return render_template("400m.html", text=text, header=header, button=button)

        else:
            db.execute("INSERT INTO cues (user_id, event, cue) VALUES (:user_id, :event, :cue)", user_id=session["user_id"],
            event="400m", cue=request.form.get("400mcues"))
            rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '400m'", user_id=session["user_id"])

            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

            return render_template("400m.html", text=text, header=header, button=button)

    # query for stored cue and display it, else display nothing in text field
    else:
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '400m'", user_id=session["user_id"])
        if len(rows) == 1:
            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

        else:
            text = ""
            header = "Enter Cue List"
            button = "Submit Cue"

        return render_template("400m.html", text=text, header=header, button=button)


@app.route("/110mh", methods=["GET", "POST"])
@login_required
def hurdles():
    """Shows 110mh page"""

    if request.method == "POST":

        # see if user already has cues stored. if yes, update cue, if no, make new cue. If user deletes cue, delete from db
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '110mh'", user_id=session["user_id"])

        if len(rows) == 1:

            if request.form.get("110mhcues") == "":
                db.execute("DELETE FROM cues WHERE user_id = :user_id AND event = '110mh'", user_id=session["user_id"])
                text = ""
                header = "Enter Cue List"
                button = "Submit Cue"

                return render_template("110mh.html", text=text, header=header, button=button)

            else:
                db.execute("UPDATE cues SET cue = :cue WHERE user_id = :user_id AND event = '110mh'", user_id=session["user_id"], cue=request.form.get("110mhcues"))
                rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '110mh'", user_id=session["user_id"])

                text = rows[0]['cue']
                header = "Edit Cue List"
                button = "Submit Edits"

                return render_template("110mh.html", text=text, header=header, button=button)

        else:
            db.execute("INSERT INTO cues (user_id, event, cue) VALUES (:user_id, :event, :cue)", user_id=session["user_id"],
            event="110mh", cue=request.form.get("110mhcues"))
            rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '110mh'", user_id=session["user_id"])

            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

            return render_template("110mh.html", text=text, header=header, button=button)

    # query for stored cue and display it, else display nothing in text field
    else:
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '110mh'", user_id=session["user_id"])
        if len(rows) == 1:
            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

        else:
            text = ""
            header = "Enter Cue List"
            button = "Submit Cue"

        return render_template("110mh.html", text=text, header=header, button=button)


@app.route("/discus", methods=["GET", "POST"])
@login_required
def discus():
    """Shows discus page"""

    if request.method == "POST":

        # see if user already has cues stored. if yes, update cue, if no, make new cue. If user deletes cue, delete from db
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'discus'", user_id=session["user_id"])

        if len(rows) == 1:

            if request.form.get("discuscues") == "":
                db.execute("DELETE FROM cues WHERE user_id = :user_id AND event = 'discus'", user_id=session["user_id"])
                text = ""
                header = "Enter Cue List"
                button = "Submit Cue"

                return render_template("discus.html", text=text, header=header, button=button)

            else:
                db.execute("UPDATE cues SET cue = :cue WHERE user_id = :user_id AND event = 'discus'", user_id=session["user_id"], cue=request.form.get("discuscues"))
                rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'discus'", user_id=session["user_id"])

                text = rows[0]['cue']
                header = "Edit Cue List"
                button = "Submit Edits"

                return render_template("discus.html", text=text, header=header, button=button)

        else:
            db.execute("INSERT INTO cues (user_id, event, cue) VALUES (:user_id, :event, :cue)", user_id=session["user_id"],
            event="discus", cue=request.form.get("discuscues"))
            rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'discus'", user_id=session["user_id"])

            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

            return render_template("discus.html", text=text, header=header, button=button)

    # query for stored cue and display it, else display nothing in text field
    else:
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'discus'", user_id=session["user_id"])
        if len(rows) == 1:
            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

        else:
            text = ""
            header = "Enter Cue List"
            button = "Submit Cue"

        return render_template("discus.html", text=text, header=header, button=button)


@app.route("/polevault", methods=["GET", "POST"])
@login_required
def polevault():
    """Shows polevault page"""

    if request.method == "POST":

        # see if user already has cues stored. if yes, update cue, if no, make new cue. If user deletes cue, delete from db
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'polevault'", user_id=session["user_id"])

        if len(rows) == 1:

            if request.form.get("polevaultcues") == "":
                db.execute("DELETE FROM cues WHERE user_id = :user_id AND event = 'polevault'", user_id=session["user_id"])
                text = ""
                header = "Enter Cue List"
                button = "Submit Cue"

                return render_template("polevault.html", text=text, header=header, button=button)

            else:
                db.execute("UPDATE cues SET cue = :cue WHERE user_id = :user_id AND event = 'polevault'", user_id=session["user_id"], cue=request.form.get("polevaultcues"))
                rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'polevault'", user_id=session["user_id"])

                text = rows[0]['cue']
                header = "Edit Cue List"
                button = "Submit Edits"

                return render_template("polevault.html", text=text, header=header, button=button)

        else:
            db.execute("INSERT INTO cues (user_id, event, cue) VALUES (:user_id, :event, :cue)", user_id=session["user_id"],
            event="polevault", cue=request.form.get("polevaultcues"))
            rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'polevault'", user_id=session["user_id"])

            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

            return render_template("polevault.html", text=text, header=header, button=button)

    # query for stored cue and display it, else display nothing in text field
    else:
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'polevault'", user_id=session["user_id"])
        if len(rows) == 1:
            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

        else:
            text = ""
            header = "Enter Cue List"
            button = "Submit Cue"

        return render_template("polevault.html", text=text, header=header, button=button)


@app.route("/javelin", methods=["GET", "POST"])
@login_required
def javelin():
    """Shows javelin page"""

    if request.method == "POST":

        # see if user already has cues stored. if yes, update cue, if no, make new cue. If user deletes cue, delete from db
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'javelin'", user_id=session["user_id"])

        if len(rows) == 1:

            if request.form.get("javelincues") == "":
                db.execute("DELETE FROM cues WHERE user_id = :user_id AND event = 'javelin'", user_id=session["user_id"])
                text = ""
                header = "Enter Cue List"
                button = "Submit Cue"

                return render_template("javelin.html", text=text, header=header, button=button)

            else:
                db.execute("UPDATE cues SET cue = :cue WHERE user_id = :user_id AND event = 'javelin'", user_id=session["user_id"], cue=request.form.get("javelincues"))
                rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'javelin'", user_id=session["user_id"])

                text = rows[0]['cue']
                header = "Edit Cue List"
                button = "Submit Edits"

                return render_template("javelin.html", text=text, header=header, button=button)

        else:
            db.execute("INSERT INTO cues (user_id, event, cue) VALUES (:user_id, :event, :cue)", user_id=session["user_id"],
            event="javelin", cue=request.form.get("javelincues"))
            rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'javelin'", user_id=session["user_id"])

            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

            return render_template("javelin.html", text=text, header=header, button=button)

    # query for stored cue and display it, else display nothing in text field
    else:
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = 'javelin'", user_id=session["user_id"])
        if len(rows) == 1:
            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

        else:
            text = ""
            header = "Enter Cue List"
            button = "Submit Cue"

        return render_template("javelin.html", text=text, header=header, button=button)


@app.route("/1500m", methods=["GET", "POST"])
@login_required
def distance():
    """Shows 1500m page"""

    if request.method == "POST":

        # see if user already has cues stored. if yes, update cue, if no, make new cue. If user deletes cue, delete from db
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '1500m'", user_id=session["user_id"])

        if len(rows) == 1:

            if request.form.get("1500mcues") == "":
                db.execute("DELETE FROM cues WHERE user_id = :user_id AND event = '1500m'", user_id=session["user_id"])
                text = ""
                header = "Enter Cue List"
                button = "Submit Cue"

                return render_template("1500m.html", text=text, header=header, button=button)

            else:
                db.execute("UPDATE cues SET cue = :cue WHERE user_id = :user_id AND event = '1500m'", user_id=session["user_id"], cue=request.form.get("1500mcues"))
                rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '1500m'", user_id=session["user_id"])

                text = rows[0]['cue']
                header = "Edit Cue List"
                button = "Submit Edits"

                return render_template("1500m.html", text=text, header=header, button=button)

        else:
            db.execute("INSERT INTO cues (user_id, event, cue) VALUES (:user_id, :event, :cue)", user_id=session["user_id"],
            event="1500m", cue=request.form.get("1500mcues"))
            rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '1500m'", user_id=session["user_id"])

            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

            return render_template("1500m.html", text=text, header=header, button=button)

    # query for stored cue and display it, else display nothing in text field
    else:
        rows = db.execute("SELECT * FROM cues WHERE user_id = :user_id AND event = '1500m'", user_id=session["user_id"])
        if len(rows) == 1:
            text = rows[0]['cue']
            header = "Edit Cue List"
            button = "Submit Edits"

        else:
            text = ""
            header = "Enter Cue List"
            button = "Submit Cue"

        return render_template("1500m.html", text=text, header=header, button=button)


@app.route("/about")
@login_required
def about():
    """Shows about page"""

    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and / or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registers a new user"""

    if request.method == "POST":

        # query for usernames with inputted username in db, apologize if one exists
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(rows) != 0:
            return apology("Username already taken", 403)

        # insert new user into db
        else:
            db.execute("INSERT INTO users (username, hash, name) VALUES (:username, :password, :name)",
                        username=request.form.get("username"),
                        password=generate_password_hash(request.form.get("password")), name=request.form.get("name"))

        # log the user into the new account
        rows = db.execute("SELECT id FROM users WHERE username = :username",
                                        username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    # user reached route via GET
    elif request.method == "GET":
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""

    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
