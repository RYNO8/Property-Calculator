from flask import render_template, redirect, url_for
from flask import current_app as app
from api import mapboxRequest, domainRequest
from utility import haversineDist, load

MAX_DIST = 1100

def getFacilities(searchTerm, iconName, baseLoc, numFeatures):
    output = []
    for feature in mapboxRequest(searchTerm, types=["poi"], lon=baseLoc[0], lat=baseLoc[1])[:numFeatures]:
        coord = feature["geometry"]["coordinates"]
        if coord == baseLoc: continue

        if feature["relevance"] > 0.90 or len(output) == 0:
            output.append({
                "dist": round(min(haversineDist(baseLoc, coord), MAX_DIST), 2),
                "des": feature["text"],
                "coord": coord,
                "icon": iconName
            })
    return output


def getSchools(baseLoc):
    schools = domainRequest("locations/schools", coordinate=str(baseLoc[1]) + "," + str(baseLoc[0]))
    features = []
    for school in schools:
        #print(school["name"], school["educationLevel"], school["displayYear"].replace(" ", ""))

        coord = [school["geolocation"]["lon"], school["geolocation"]["lat"]]
        features.append({
            "dist": round(min(haversineDist(baseLoc, coord), MAX_DIST), 2),
            "des": school["name"],
            "coord": coord,
            "icon": "school.png"
        })
    return features


@app.route("/suburbQuery")
def suburbQuery():
    assert "suburb" in load()
    assert "suburbId" in load()

    form = load()
    if "suburb" not in form:
        return redirect(url_for("home"))
    response = mapboxRequest(form["suburb"], types=["poi", "postcode", "locality"])[0]

    return result(
        form["suburb"],
        form["suburbId"],
        response["geometry"]["coordinates"]
    )


def result(suburb, suburbId, baseLoc):
    print(suburbId, suburb, baseLoc)
    airportLoc =  [151.1748595, -33.940917]
    features = [{
        "dist": round(min(haversineDist(baseLoc, airportLoc), MAX_DIST), 2),
        "des": "Sydney Airport",
        "coord": airportLoc,
        "icon": "airport.jpg"
    }] # manditory airport


    """#TODO: OR lightbuild.jpg
    features += getFacilities(str(baseLoc[0]) + "," + str(baseLoc[1]), "lightbulb.png", baseLoc, 10)"""
    features += getSchools(baseLoc)
    features += getFacilities(suburb + " hospital", "hospital.png", baseLoc, 2)
    features += getFacilities(suburb + " library", "library.png", baseLoc, 2)
    features += getFacilities(suburb + " shop", "shop.png", baseLoc, 6)
    features += getFacilities(suburb + " station", "station.jpg", baseLoc, 2)
    features = sorted(features, key=lambda x: x["dist"])
    print(features)

    return render_template("result.html", suburb=suburb, baseLoc=baseLoc, features=features)



