import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for

MAXIMUM_BOOKINGS = 12
CURRENT_DATE = datetime.now().replace(microsecond=0)


def load_data(json_file, key_to_load):
    with open(json_file) as database:
        data = json.load(database)[key_to_load]
        return data


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_data("competitions.json", "competitions")
clubs = load_data("clubs.json", "clubs")


def helper_get_club_via_email():
    for club in clubs:
        if club["email"] == request.form["email"]:
            return club


def helper_get_club_via_name():
    for club in clubs:
        if club["name"] == request.form["name"]:
            return club


def helper_get_competition_via_name():
    for competition in competitions:
        if competition["name"] == request.form["name"]:
            return competition


@app.template_filter("str_to_date")
def _convert_str_to_date(date_str, format="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(date_str, format)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary():
    club = helper_get_club_via_email()

    if club is None:
        flash("Email not found. Please try a valid email.")
        return render_template("index.html")

    else:
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
            today=CURRENT_DATE,
        )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = helper_get_club_via_name()
    found_competition = helper_get_competition_via_name()

    if not found_club or not found_competition:
        flash(
            "You can't book if the competition or the account is invalid. Please try again."
        )
        return render_template("index.html")

    else:
        club_points = int(found_club["points"])
        found_competition_date = datetime.strptime(
            found_competition["date"], "%Y-%m-%d %H:%M:%S"
        )
        places_allowed = MAXIMUM_BOOKINGS

        if club_points == 0:
            flash("You do not have enough points to book places.")
            return render_template(
                "welcome.html",
                club=found_club,
                competitions=competitions,
                today=CURRENT_DATE,
            )

        if found_competition_date < CURRENT_DATE:
            flash("Booking in a past competition is impossible.")
            return render_template(
                "welcome.html",
                club=found_club,
                competitions=competitions,
                today=CURRENT_DATE,
            )

        if club_points < places_allowed:
            places_allowed = club_points
            return render_template(
                "booking.html",
                club=found_club,
                competition=found_competition,
                limit=places_allowed,
                today=CURRENT_DATE,
            )

        return render_template(
            "booking.html",
            club=found_club,
            competition=found_competition,
            limit=places_allowed,
            today=CURRENT_DATE,
        )


@app.route("/purchase_places", methods=["POST"])
def purchase_places():
    """This docstrings is show that the issue with club points update
    was already handled and tested in this fonction during the resolution of bug nr 2.
    """
    competition = helper_get_competition_via_name()
    club = helper_get_club_via_name()
    club_points = int(club["points"])
    competition_date = datetime.strptime(
        competition["date"], "%Y-%m-%d %H:%M:%S"
    )
    places_required = int(request.form["places"])
    places_allowed = MAXIMUM_BOOKINGS

    if club_points < places_allowed:
        places_allowed = club_points

    elif places_required > club_points or places_required > places_allowed:
        flash("You are not allowed to book this quantity. Please try again.")
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
            today=CURRENT_DATE,
        )

    elif places_required <= 0:
        flash("This is not a correct value. Please try again.")
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
            today=CURRENT_DATE,
        )

    if competition_date < CURRENT_DATE:
        flash("Booking in a past competition is impossible.")
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
            today=CURRENT_DATE,
        )

    competition["numberOfPlaces"] = (
        int(competition["numberOfPlaces"]) - places_required
    )

    club["points"] = int(club["points"]) - places_required

    places_allowed = places_allowed - places_required

    flash("Great-booking complete!")

    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions,
        today=CURRENT_DATE,
    )


@app.route("/points")
def points():
    if clubs:
        return render_template("points.html", clubs=clubs)
    else:
        flash("Page unavailable.")
        return render_template("index.html")


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
