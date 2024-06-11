""" This extract file connects to an API: https://data-eng-plants-api.herokuapp.com/plants/8
and collates all of the data on the plants available. It then stores these in a single json file."""
import requests
import json
BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"
ETXTRACT_DESTINATION = "extracted_plants.json"


def get_plant_response(id: int) -> requests.Response:
    """Return a response object."""
    return requests.get(BASE_URL+"{id}")


if __name__ == "__main__":
    ...
