import requests, json, os
from mapbox import Geocoder

"""import wifissid, urllib
if wifissid.showssid() == "sbhs":
    urllib.request.install_opener(urllib.request.build_opener(
        urllib.request.ProxyHandler({'http': 'http://:@proxy.intranet:8080', 'https': 'http://:@proxy.intranet:8080'})
    ))
"""

##### MAPBOX #####
#MAPBOX_TOKEN = "redacted"
geocoder = Geocoder(
    access_token=os.environ.get("MAPBOX_TOKEN")
)


def mapboxRequest(*args, **kwargs):
    """https://github.com/mapbox/mapbox-sdk-py/blob/master/docs/geocoding.md"""
    return geocoder.forward(
        *args,
        bbox=[150.56005931268874, -34.15702500964514, 151.2951926298794, -33.50604591566818],
        country=["au"],
        **kwargs
    ).geojson()["features"]


##### DOMAIN #####
DOMAIN_DOMAIN = "https://api.domain.com.au/v1"
#DOMAIN_ID = "redacted"
#DOMAIN_SECRET = "redacted"
DOMAIN_TOKEN = json.loads(requests.post(
    "https://auth.domain.com.au/v1/connect/token",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={
        "grant_type": "client_credentials",
        "scope": [" ".join([
            "api_properties_read",
            "api_demographics_read",
            "api_addresslocators_read",
            "api_suburbperformance_read",
            "api_locations_read",
        ])]
    },
    auth=(os.environ.get("DOMAIN_ID"), os.environ.get("DOMAIN_SECRET"))
).content)["access_token"]


def domainRequest(endpoint, method="GET", **kwargs):
    assert len(kwargs) > 0
    response = requests.request(
        method,
        DOMAIN_DOMAIN + "/" + endpoint + "?" + "&".join([k + "=" + str(kwargs[k]) for k in kwargs]),
        headers={'Authorization': 'Bearer ' + DOMAIN_TOKEN, 'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise Exception(response.content)

    return json.loads(response.content)


def suggest(street):
    """UNUSED"""
    response = domainRequest("properties/_suggest", terms=street, pageSize=20, channel="All")
    sorted(response, key=lambda x: x["relativeScore"])
    return response
