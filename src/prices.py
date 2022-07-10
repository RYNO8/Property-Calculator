import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

from utility import load, titleToSpace

df = pd.read_csv("suburb_data.csv")


def prices(server):
    dash_app = dash.Dash(
        name="Prices",
        server=server,
        routes_pathname_prefix="/prices_iframe/",
        external_stylesheets=[
            "/static/css/map.css",
            "/static/css/styles.css",
            "https://fonts.googleapis.com/css?family=Inter:400,500,600,700&display=swap",
            "http://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css"
        ]
    )
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")  # e.g. 1/05/2009
    
    dash_app.layout = html.Div([
        html.H1(children="Undefined", id="label"),
        html.Div([
            dcc.Dropdown(
                id="dropdownType",
                options=[{"label": i, "value": i} for i in ["House", "Unit", "House vs Unit"]],
                value="House",
                clearable=False,
                multi=False,
                style={"width": "300px"},
            ),

            dcc.Dropdown(
                id="dropdownCat",
                options=[{"label": titleToSpace(i), "value": i} for i in [
                    "medianSoldPrice", "numberSold", "highestSoldPrice", "lowestSoldPrice", "5thPercentileSoldPrice",
                    "25thPercentileSoldPrice", "75thPercentileSoldPrice", "95thPercentileSoldPrice",
                    "medianSaleListingPrice", "numberSaleListing", "highestSaleListingPrice", "lowestSaleListingPrice",
                    "auctionNumberAuctioned", "auctionNumberSold", "auctionNumberWithdrawn", "daysOnMarket",
                    "medianRentListingPrice", "numberRentListing", "highestRentListingPrice", "lowestRentListingPrice"]
                ],
                value="medianSoldPrice",
                clearable=False,
                multi=False,
                style={"flex-grow": "1", "width": "300px"},
            )
        ], style={"display": "flex"}),

        html.Div([
            dcc.Graph(id="graph", style={"padding-top": "10px", "border-radius": "10px"}
        )]),
    ])

    @dash_app.callback(
        Output(component_id="graph", component_property="figure"),
        [
            Input(component_id="dropdownType", component_property="value"),
            Input(component_id="dropdownCat", component_property="value"),
        ]
    )
    def update_graph(propType, category):
        if propType == "House vs Unit":
            toDisplay = df.loc[(df["suburbId"] == load()["suburbId"]), [category, "date", "propertyType"]]
            x = toDisplay["date"]
            y1 = toDisplay.loc[toDisplay["propertyType"] == "house"][category]
            y2 = toDisplay.loc[toDisplay["propertyType"] == "unit"][category]
            #print(x, y1, y2)
            fig = go.Figure(data=[
                go.Bar(name="unit", x=x, y=y1),
                go.Bar(name="house", x=x, y=y2)
            ])
            fig.update_layout(barmode='group')
            return fig

        else:
            return px.line(
                df.loc[(df["suburbId"] == load()["suburbId"]) & (df["propertyType"] == propType.lower())],
                x="date",
                y=category,
                line_shape="spline",
                render_mode="svg",
            )

    @dash_app.callback(
        Output(component_id="label", component_property="children"),
        [
            Input(component_id="dropdownType", component_property="value"),
            Input(component_id="dropdownCat", component_property="value"),
        ]
    )
    def update_label(propertyType, category):
        return titleToSpace(category) + " for " + propertyType + "s in " + load()["suburb"]

    return dash_app.server
