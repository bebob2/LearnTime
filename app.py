import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


class Database: # created with the help of copilot
    """Lightweight helper providing a CS50-style `execute` API backed by SQLAlchemy."""

    def __init__(self, uri):
        self.engine = create_engine(uri, connect_args={"check_same_thread": False})

    def execute(self, query, *params):
        # Use a raw DBAPI connection so we can keep using '?' placeholders like cs50.SQL
        conn = self.engine.raw_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)

            # Return rows for SELECT queries
            if query.strip().lower().startswith("select"):
                columns = [col[0] for col in cursor.description] if cursor.description else []
                return [dict(zip(columns, row)) for row in cursor.fetchall()]

            # Commit for all non-SELECT statements
            conn.commit()

            # Return last inserted row ID for INSERTs, rowcount otherwise
            if query.strip().lower().startswith("insert"):
                return cursor.lastrowid

            return cursor.rowcount
        finally:
            conn.close()


# Configure database
db = Database("sqlite:///learn-time.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    # Get subjects for current user
    subjects = db.execute("SELECT * FROM subjects WHERE user_id = ?", session["user_id"])
    # Get presets for current user
    presets = db.execute("SELECT * FROM presets WHERE user_id = ? ORDER BY minutes ASC", session["user_id"])

    # Render page
    return render_template("index.html", subjects=subjects, presets=presets)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Welcome back!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Safe password as variable
        password = request.form.get("password")

        # Safe username as variable
        username = request.form.get("username")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure passwords match
        elif not request.form.get("confirmation") == password:
            return apology("passwords do not match!", 400)

        # Create password hash
        password_hash = generate_password_hash(password, method='scrypt', salt_length=16)

        # Insert user into database and ensure username doesn't already exist
        try:
            id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                            username, password_hash)
        except ValueError:
            return apology("username already exists!", 400)

        # Remember which user has logged in
        session["user_id"] = id

        # Flash a mesage to user that they've succecfully registerd
        flash("Congrats! You have REGISTERED succesfully!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/account")
@login_required
def account():
    data = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    return render_template("account.html", data=data)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    # User reached rout vie POST (as by submitting a form via POST)
    if request.method == "POST":
        # Store old_pwd in variable
        old_password = request.form.get("old_password")

        # Store new_pwd in variable
        new_password = request.form.get("new_password")

        # Store conformation in variable
        conformation = request.form.get("confirmation")

        # Ensure notice was understood
        if not request.form.get("understood"):
            return apology("You must accept notice!", 400)

        # Ensure old pwd was submitted
        if not old_password:
            return apology("must provide old password!", 400)

        # Ensure new_password was submitted
        elif not new_password:
            return apology("must provide new password!", 400)

        # Query database for id
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Ensure old_pwd is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], old_password):
            return apology("invalid old password", 403)

        # Ensure passwords match
        elif not conformation == new_password:
            return apology("passwords do not match!", 400)

        # Create password hash
        password_hash = generate_password_hash(new_password, method='scrypt', salt_length=16)

        # Insert user into database and ensure username doesn't already exist

        db.execute("UPDATE users SET hash = ? WHERE id = ?", password_hash, session["user_id"])

        # Redirect user to Homepage
        flash("Password updated successfully!")
        return redirect("/account")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_password.html")

@app.route("/subjects", methods=["GET", "POST"])
@login_required
def subjects():

    if request.method == "POST":
        subject = request.form.get("subject")
        if not subject:
            return apology("must provide subject!", 400)
        db.execute("INSERT INTO subjects (user_id, subject) VALUES (?, ?)", session["user_id"], subject)

        flash("Subject added successfully!")
        return redirect("/subjects")

    else:
        subjects = db.execute("SELECT * FROM subjects WHERE user_id = ?", session["user_id"])
        return render_template("subjects.html", subjects=subjects)


@app.route("/delete_subject", methods=["POST"]) # this function created by copilot
@login_required
def delete_subject():
    subject_id = request.form.get("subject_id")
    if not subject_id:
        return apology("must provide subject id!", 400)
    deletedAmount = db.execute("DELETE FROM subjects WHERE id = ? AND user_id = ?", subject_id, session["user_id"])
    db.execute("DELETE FROM tracker WHERE subject_id = ? AND user_id = ?", subject_id, session["user_id"])
    if deletedAmount == 0:
        return apology("subject not found!", 404)

    flash("Subject deleted successfully!")
    return redirect("/subjects")

@app.route("/edit_subject", methods=["POST", "GET"]) # this function created by copilot
@login_required
def edit_subject():
    # Accept subject_id from either GET (query string) or POST (form data)
    subject_id = request.values.get("subject_id")
    if not subject_id:
        return apology("must provide subject id!", 400)

    subject = db.execute("SELECT * FROM subjects WHERE id = ? AND user_id = ?", subject_id, session["user_id"])
    if len(subject) != 1:
        return apology("subject not found!", 404)

    if request.method == "POST":
        # The edit form field is named "subject"
        new_subject = request.form.get("subject")
        if not new_subject:
            return apology("must provide new subject name!", 400)
        db.execute("UPDATE subjects SET subject = ? WHERE id = ? AND user_id = ?", new_subject, subject_id, session["user_id"])

        flash("Subject updated successfully!")
        return redirect("/subjects")

    else:
        return render_template("edit-subject.html", subject=subject[0])

@app.route("/store_learned_time", methods=["POST"])
@login_required
def store_learned_time():
    data = request.get_json()
    subject_id = data.get("subject_id")
    learned_time = data.get("learned_time")

    # Accept 0 as a valid learned_time
    if subject_id is None or learned_time is None:
        return apology("must provide subject id and learned time!", 400)

    db.execute("INSERT INTO tracker (user_id, subject_id, minutes) VALUES (?, ?, ?)", session["user_id"], subject_id, learned_time)

    # Return JSON for AJAX callers
    return jsonify({"success": True})

@app.route("/stats")
@login_required
def stats(): # created with copilot to save time
    data = db.execute("""
        SELECT subjects.subject, SUM(tracker.minutes) AS total_minutes
        FROM tracker
        JOIN subjects ON tracker.subject_id = subjects.id
        WHERE tracker.user_id = ?
        GROUP BY subjects.subject
    """, session["user_id"])

    return render_template("stats.html", data=data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/history") # created with the help of copilot to save time
@login_required
def history():
    data = db.execute("""
        SELECT subjects.subject, tracker.minutes
        FROM tracker
        JOIN subjects ON tracker.subject_id = subjects.id
        WHERE tracker.user_id = ?
    """, session["user_id"])

    return render_template("history.html", data=data)

@app.route("/presets", methods=["GET", "POST"]) # created with the help of copilot to save time
@login_required
def presets():
    presets = db.execute("SELECT * FROM presets WHERE user_id = ?", session["user_id"])
    if request.method == "POST":
        minutes = request.form.get("minutes")

        if not minutes:
            return apology("must provide minutes!", 400)
        try:
            int(minutes)
        except ValueError:
            return apology("must provide valid minutes!", 400)

        if not int(minutes) >= 0 and not int(minutes) <= 1440:
            return apology("must provide minutes between 0 and 1440!", 400)

        if len(presets) >= 4:
            flash("Error: ")
            return redirect("/presets")
        else:
            db.execute("INSERT INTO presets (user_id, minutes) VALUES (?, ?)", session["user_id"], int(minutes))
            flash("Preset added successfully!")
            return redirect("/presets")
    else:
        if len(presets) >= 4:
            flash("You have reached the maximum number of presets (4). Please delete an existing preset to add a new one.")
        return render_template("presets.html", presets=presets)

@app.route("/delete_preset", methods=["POST"])
@login_required
def delete_preset():
    preset_id = request.form.get("preset_id")
    if not preset_id:
        return apology("must provide preset id!", 400)
    deletedAmount = db.execute("DELETE FROM presets WHERE id = ? AND user_id = ?", preset_id, session["user_id"])
    if deletedAmount == 0:
        return apology("preset not found!", 404)

    flash("Preset deleted successfully!")
    return redirect("/presets")
