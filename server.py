import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for

MAXIMUM_BOOKINGS = 12
CURRENT_DATE = datetime.now().replace(microsecond=0)


def load_data(json_file, key_to_load):
    """Load data from a JSON file.

    Args:
        json_file (str): The path to the JSON file.
        key_to_load (str): The key in the JSON file to load.

    Returns:
        dict: The loaded data.
    """
    with open(json_file) as database:
        data = json.load(database)[key_to_load]
        return data


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_data("competitions.json", "competitions")
clubs = load_data("clubs.json", "clubs")


def helper_get_club_via_email(email):
    """Retrieves a club based on an email address.

    Args:
        email (str): The email address to search for.

    Returns:
        dict or None: The club information if found, else None.
    """
    for club in clubs:
        if club["email"] == email:
            return club


def helper_get_club_via_name(name):
    """Retrieves a club based on its name.

    Args:
        name (str): The name of the club to search for.

    Returns:
        dict or None: The club information if found, else None.
    """
    for club in clubs:
        if club["name"] == name:
            return club


def helper_get_competition_via_name(name):
    """Retrieves a competition based on its name.

    Args:
        name (str): The name of the competition to search for.

    Returns:
        dict or None: The competition information if found, else None.
    """
    for competition in competitions:
        if competition["name"] == name:
            return competition


@app.template_filter("str_to_date")
def _convert_str_to_date(date_str, format="%Y-%m-%d %H:%M:%S"):
    """Convert a string to a datetime object.

    Args:
        date_str (str): The date string to convert.
        format (str): The format of the date string (default is "%Y-%m-%d %H:%M:%S").

    Returns:
        datetime: The datetime object representing the parsed date.
    """
    return datetime.strptime(date_str, format)


@app.route("/")
def index():
    """Renders the index page."""
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary():
    """Renders the summary page for a club.
    An error message is raised if the club is not found.
    """
    club = helper_get_club_via_email(request.form["email"])

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
    """This function is responsible for rendering the booking page
    for a given competition and club.
    The following conditions are handled:
    -Booking is made against valid competition/club.
    -Booking is not possible for a past competition.
    -Booking is not possible for a club that has no points.
    -Clubs would be able to book places between the lower of clubs' points
    or the MAXIMUM_BOOKINGS value.

    Args:
        competition (str): The name of the competition to book against.
        club (str): The name of the club making the booking.
    """
    found_club = helper_get_club_via_name(club)
    found_competition = helper_get_competition_via_name(competition)

    if not found_club or not found_competition:
        flash(
            "You can't book if the competition or the account is invalid. Please try again."
        )
        return render_template("index.html")

    club_points = int(found_club["points"])
    found_competition_date = datetime.strptime(
        found_competition["date"], "%Y-%m-%d %H:%M:%S"
    )
    places_allowed = MAXIMUM_BOOKINGS

    if found_competition_date < CURRENT_DATE:
        flash("Booking in a past competition is impossible.")
        return render_template(
            "welcome.html",
            club=found_club,
            competitions=competitions,
            today=CURRENT_DATE,
        )

    if club_points == 0:
        flash("You do not have enough points to book places.")
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
    """Handles the purchase of competition places.
    The following conditions are handled:
    -Booking is made against valid competition/club.
    -Booking is not possible for a past competition.
    -Booking is not possible for a club that has no points.
    -Clubs would be able to book places between the lower of clubs' points
    or the MAXIMUM_BOOKINGS value.
    -Places booked shall be higher to zero.
    Places booked are then deducted from:
    -The club's points
    -The competitions availables places
    """
    competition = helper_get_competition_via_name(request.form["competition"])
    club = helper_get_club_via_name(request.form["club"])

    if not club or not competition:
        flash(
            "You can't book if the competition or the account is invalid. Please try again."
        )
        return render_template("index.html")

    club_points = int(club["points"])
    competition_date = datetime.strptime(
        competition["date"], "%Y-%m-%d %H:%M:%S"
    )
    places_required = int(request.form["places"])
    places_allowed = MAXIMUM_BOOKINGS

    if club_points == 0:
        flash("You do not have enough points to book places.")
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
            today=CURRENT_DATE,
        )

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

    flash("Great, booking complete !")

    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions,
        today=CURRENT_DATE,
    )


@app.route("/points")
def points():
    """Renders the points page which includes a table
    with the current points of each club.
    """
    if clubs:
        return render_template("points.html", clubs=clubs)
    else:
        flash("Page unavailable.")
        return render_template("index.html")


@app.route("/logout")
def logout():
    """Logs out the user by redirecting him to the index page."""
    return redirect(url_for("index"))
