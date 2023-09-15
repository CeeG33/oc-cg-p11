import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for

MAXIMUM_BOOKINGS = 12
CURRENT_DATE = datetime.now().replace(microsecond=0)


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.template_filter("str_to_date")
def _convert_str_to_date(date_str, format="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(date_str, format)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except IndexError:
        flash("Email not found. Please try a valid email.")
        return render_template("index.html")

    return render_template(
        "welcome.html", club=club, competitions=competitions, today=CURRENT_DATE
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    club_points = int(foundClub["points"])
    found_competition_date = datetime.strptime(
        foundCompetition["date"], "%Y-%m-%d %H:%M:%S"
    )
    places_allowed = MAXIMUM_BOOKINGS

    if club_points == 0:
        flash("You do not have enough points to book places.")
        return render_template(
            "welcome.html",
            club=foundClub,
            competitions=competitions,
            today=CURRENT_DATE,
        )

    if found_competition_date < CURRENT_DATE:
        flash("Booking in a past competition is impossible.")
        return render_template(
            "welcome.html",
            club=foundClub,
            competitions=competitions,
            today=CURRENT_DATE,
        )

    if club_points < places_allowed:
        places_allowed = club_points
        return render_template(
            "booking.html",
            club=foundClub,
            competition=foundCompetition,
            limit=places_allowed,
            today=CURRENT_DATE,
        )

    if foundClub and foundCompetition:
        return render_template(
            "booking.html",
            club=foundClub,
            competition=foundCompetition,
            limit=places_allowed,
            today=CURRENT_DATE,
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", club=club, competitions=competitions, today=CURRENT_DATE
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    """This docstrings is show that the issue with club points update
    was already handled and tested in this fonction during the resolution of bug nr 2.
    """
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    club_points = int(club["points"])
    competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    placesRequired = int(request.form["places"])
    places_allowed = MAXIMUM_BOOKINGS

    if club_points < places_allowed:
        places_allowed = club_points

    elif placesRequired > club_points or placesRequired > places_allowed:
        flash("You are not allowed to book this quantity. Please try again.")
        return render_template(
            "welcome.html", club=club, competitions=competitions, today=CURRENT_DATE
        )

    elif placesRequired <= 0:
        flash("This is not a correct value. Please try again.")
        return render_template(
            "welcome.html", club=club, competitions=competitions, today=CURRENT_DATE
        )

    if competition_date < CURRENT_DATE:
        flash("Booking in a past competition is impossible.")
        return render_template(
            "welcome.html", club=club, competitions=competitions, today=CURRENT_DATE
        )

    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired

    club["points"] = int(club["points"]) - placesRequired

    places_allowed = places_allowed - placesRequired

    flash("Great-booking complete!")

    return render_template(
        "welcome.html", club=club, competitions=competitions, today=CURRENT_DATE
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
