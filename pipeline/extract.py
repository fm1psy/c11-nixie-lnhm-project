""" This extract file connects to an API: https://data-eng-plants-api.herokuapp.com/plants/8
and collates all of the data on the plants available. It then stores these in a single json file."""
import time
import requests
import json
BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"
EXTRACT_DESTINATION = "extracted_plants.json"

DEFAULT_RANGE = 50


def get_plant_response(id: int) -> requests.Response:
    """Return a response object."""
    try:
        if not isinstance(id, int):
            raise ValueError
        return requests.get(BASE_URL+f"{id}")
    except:
        return {}


def get_range_of_plants(plant_range: int = DEFAULT_RANGE) -> list[dict]:
    """Go through a range of plant ids and return a list """
    res = []
    for i in range(1, plant_range+1):
        res.append(get_plant_response(i).json())
    return res


def extract_data() -> None:
    """Connect to the plants api and extract the plant data."""
    plant_jsons = get_range_of_plants()
    with open(EXTRACT_DESTINATION, "w", encoding="utf-8") as f:
        json.dump(plant_jsons, f, indent=4)


if __name__ == "__main__":
    start = time.time()
    extract_data()
    print(time.time() - start)
