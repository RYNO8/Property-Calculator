from flask import Flask, render_template
from utility import load
import dotenv
dotenv.load_dotenv()

app = Flask(__name__, instance_relative_config=False)

with app.app_context():
    # flask stuff #

    @app.route("/")
    @app.route("/about")
    @app.route("/about/")
    def about(): return render_template("about.html", suburb=load()["suburb"])

    @app.route("/heatmap/")
    def search(): return render_template("heatmap.html", suburb=load()["suburb"])
    
    @app.route("/figHouse")
    @app.route("/figHouse/")
    def figHouse(): return render_template("figHouse.html", suburb=load()["suburb"])
    
    @app.route("/figUnit")
    @app.route("/figUnit/")
    def figUnit(): return render_template("figUnit.html", suburb=load()["suburb"])
    
    @app.errorhandler(404)
    def error(_): return render_template("404.html", suburb=load()["suburb"])

    import distMap, terrain, save

    # dash stuff #
    @app.route("/demographics")
    @app.route("/demographics/")
    def demographics_iframe(): return render_template("iframe.html", suburb=load()["suburb"], endpoint="demographics_iframe", active_page="Demographics")

    @app.route("/prices")
    @app.route("/prices/")
    def prices_iframe(): return render_template("iframe.html", suburb=load()["suburb"], endpoint="prices_iframe", active_page="Prices")
    
    
    from demographics import demographics
    app = demographics(app)
    from prices import prices
    app = prices(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
