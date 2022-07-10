import pandas as pd
from flask import request, redirect, url_for, session
from flask import current_app as app
df = pd.read_csv("suburb_data.csv")


def save(suburb):
    try:
        suburbId = df.loc[df["suburb"] == suburb].iloc[0]["suburbId"]
        with open("save.txt", "w") as f:
            f.write(str({
                "suburb": suburb,
                "suburbId": suburbId
            }))
    except IndexError:
        # suburb not found
        pass


@app.route("/saveSuburb", methods=["POST"])
def saveSuburb():
    assert "suburb" in request.form
    save(request.form["suburb"].title().strip())
    
    if "Referer" in request.headers:
        return redirect(request.headers["Referer"])
    else:
        return redirect(url_for(request.form.get("url", "suburbQuery")))
