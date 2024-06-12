""" This extract file connects to an API: https://data-eng-plants-api.herokuapp.com/plants/8
and collates all of the data on the plants available. It then stores these in a single json file."""
import time
import json
import requests
BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"
EXTRACT_DESTINATION = "extracted_plants.json"
DEFAULT_RANGE = 50


def get_plant_response(plant_id: int) -> requests.Response:
    """Return a response object."""
    if not isinstance(plant_id, int):
        raise ValueError
    return requests.get(BASE_URL+f"{plant_id}", timeout=10)


def get_range_of_plants(plant_range: int = DEFAULT_RANGE) -> list[dict]:
    """Go through a range of plant ids and return a list."""
    res = []
    for i in range(1, plant_range+1):
        try:
            res.append(get_plant_response(i).json())
        except ValueError:
            pass
    return res


def extract_data() -> None:
    """Connect to the plants api and extract the plant data.
    Then dump it onto a json file to be used in the transform step."""
    plant_data = get_range_of_plants()
    with open(EXTRACT_DESTINATION, "w", encoding="utf-8") as f:
        json.dump(plant_data, f, indent=4)


if __name__ == "__main__":
    extract_data()
