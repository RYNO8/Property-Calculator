import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

from api import domainRequest
from utility import load, titleToSpace


def loadData(suburbId, val):
    data = domainRequest("demographics", level="Suburb", id=suburbId)["demographics"]
    # print(data)

    # e.g. when sees "16", replace with "UniversityDegree"
    exceptions = {"18": "Occupation", "16": "UniversityDegree", "12": "AgeGroup"}

    for category in data:
        if exceptions.get(category["type"], category["type"]) == val:
            return pd.DataFrame({
                "keys": [i["label"] for i in category["items"]],
                "values": [i["value"] for i in category["items"]],
            })
    raise Exception("category not found")


def demographics(server):
    dash_app = dash.Dash(
        name="Demographics",
        server=server,
        routes_pathname_prefix="/demographics_iframe/",
        external_stylesheets=[
            "/static/css/map.css",
            "/static/css/styles.css",
            "https://fonts.googleapis.com/css?family=Inter:400,500,600,700&display=swap",
            "http://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css"
        ]
    )

    dash_app.layout = html.Div([
        html.Div([
            html.H1(children="Undefined", id="label"),
        ]),

        html.Div([
            dcc.Dropdown(
                id="dropdown",
                options=[{'label': titleToSpace(i), 'value': i} for i in [
                    'AgeGroup', 'AgeGroupOfPopulation', 'CountryOfBirth', 'DwellingStructure', 'EducationAttendance',
                    'FamilyComposition', 'HouseholdIncome', 'HousingLoanRepayment', 'LabourForceStatus',
                    'MaritalStatus', 'NatureOfOccupancy', 'Occupation', 'Religion', 'Rent', 'TransportToWork'
                ]],
                value="Religion",
                multi=False,
                clearable=False,
                style={"width": "300px"}
            ),
        ]),

        html.Div([
            dcc.Graph(id="graph", style={"padding-top": "10px", "border-radius": "10px"})
        ])
    ])

    @dash_app.callback(
        Output(component_id="graph", component_property="figure"),
        [Input(component_id="dropdown", component_property="value")]
    )
    def update_graph(val):
        suburbId = load().get("suburbId", 27512)
        output = loadData(suburbId, val)
        output.loc[output['values'] < 0.04 * sum(output["values"]), 'keys'] = "Other"  # rename key to "other" if < 4%
        # print(output)

        figure = px.pie(
            output,
            names="keys",
            values="values",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        figure.update_traces(textposition='inside')
        figure.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        return figure

    @dash_app.callback(
        Output(component_id="label", component_property="children"),
        [Input(component_id="dropdown", component_property="value")]
    )
    def update_label(val): return titleToSpace(val)

    return dash_app.server
