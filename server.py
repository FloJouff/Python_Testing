import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
date = datetime.now()


@app.route('/')
def index():
    return render_template("index.html", clubs=clubs, date=date)


@app.route("/showSummary", methods=["POST", "GET"])
def showSummary():
    if request.method == "POST":
        email = request.form["email"]
    else:
        email = request.args.get("email")
    club = next((club for club in clubs if club["email"] == email), None)
    if club is None:
        flash("Email not found. Please try again.")
        return redirect(url_for("index"))
    else:
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c["name"] == club), None)
    foundCompetition = next((c for c in competitions if c["name"] == competition), None)

    if not foundClub or not foundCompetition:
        flash("Something went wrong-please try again")
        return redirect(url_for("index"))

    comp_date = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S")
    if comp_date >= datetime.now():
        return render_template("booking.html", club=foundClub, competition=foundCompetition)
    else:
        flash("You can't book past competition")
        return redirect(url_for("showSummary", email=foundClub["email"]))


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = next((c for c in competitions if c["name"] == request.form["competition"]), None)
    club = next((c for c in clubs if c["name"] == request.form["club"]), None)
    placesRequired = int(request.form['places'])
    if placesRequired < 0:
        flash("The number of places can't be negative.")
        return redirect(url_for("book", competition=request.form["competition"], club=request.form["club"]))
    if competition and club:
        if "reservations" not in competition:
            competition["reservations"] = {}

        if club["name"] not in competition["reservations"]:
            competition["reservations"][club["name"]] = 0

        total_reserved = competition["reservations"][club["name"]] + placesRequired

        if total_reserved > 12:
            flash("You cannot book more than 12 places in total for a competition.")

        elif placesRequired <= int(competition["numberOfPlaces"]) and placesRequired <= int(club["points"]):
            competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
            club["points"] = int(club["points"]) - placesRequired
            competition["reservations"][club["name"]] += placesRequired
            flash("Great-booking complete!")
        else:
            flash("Not enought points or places available.")
    else:
        flash("Something went wrong-please try again")
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route("/pointsBoard/")
def pointsBoard():
    return render_template("points_board.html", clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
