from flask import render_template, request
from flask import current_app as app
from api import mapboxRequest
from utility import load


@app.route("/terrain", methods=["GET", "POST"])
def terrain():
    suburb = load()["suburb"]
    response = mapboxRequest(request.form.get("location", suburb))[0]
    return render_template("terrain.html", suburb=suburb, coord=response["geometry"]["coordinates"])

