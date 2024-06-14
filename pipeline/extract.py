""" This extract file connects to an API: https://data-eng-plants-api.herokuapp.com/plants/8
and collates all of the data on the plants available. It then stores these in a single json file."""
import time
import json
import requests
BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"
EXTRACT_DESTINATION = "/tmp/extracted_plants.json"
DEFAULT_RANGE = 50
DEFAULT_TIMEOUT = 10


def get_plant_response(plant_id: int, timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
    """Return a response object."""
    if not isinstance(plant_id, int):
        raise ValueError
    return requests.get(BASE_URL+f"{plant_id}", timeout=timeout)


def get_range_of_plants(plant_range: int = DEFAULT_RANGE) -> list[dict]:
    """Go through a range of plant ids and return a list."""
    res = []
    if not isinstance(plant_range, int):
        raise ValueError
    for i in range(0, plant_range):
        try:
            response = get_plant_response(i)
            res.append(response.json())
        except ValueError:
            print("VALUE ERROR")
        except requests.exceptions.Timeout:
            print("TIMEOUT")
        except OSError:
            print("OSError")
    return res


def extract_data() -> None:
    """Connect to the plants api and extract the plant data.
    Then dump it onto a json file to be used in the transform step."""
    plant_data = get_range_of_plants()
    with open(EXTRACT_DESTINATION, "w", encoding="utf-8") as f:
        json.dump(plant_data, f, indent=4)


if __name__ == "__main__":
    extract_data()
