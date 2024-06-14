""" This extract file connects to an API: https://data-eng-plants-api.herokuapp.com/plants/8
and collates all of the data on the plants available. It then stores these in a single json file."""
import time
import json
from lambda_multiprocessing import Pool
import requests
BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"
EXTRACT_DESTINATION = "extracted_plants.json"
DEFAULT_RANGE = 50
DEFAULT_TIMEOUT = 10


def get_plant_response(plant_id: int, timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
    """Return a response object."""
    if not isinstance(plant_id, int):
        raise ValueError
    return requests.get(BASE_URL+f"{plant_id}", timeout=timeout)


def get_plant_data(plant_id: int = DEFAULT_RANGE) -> list[dict]:
    """Go through a range of plant ids and return a list."""
    try:
        if not isinstance(plant_id, int):
            raise ValueError
        response = get_plant_response(plant_id)
        return response.json()
    except ValueError:
        print("VALUE ERROR")
    except requests.exceptions.Timeout:
        print("TIMEOUT")
    except OSError:
        print("OSError")


def extract_data(number_of_plants: int = DEFAULT_RANGE) -> None:
    indices = list(range(number_of_plants))
    with Pool(processes=6) as pool:
        plant_data = list(pool.map(get_plant_data, indices))
    return plant_data


# def extract_data() -> list[dict]:
#     """Connect to the plants api and extract the plant data.
#     Then dump it onto a json file to be used in the transform step."""
#     return get_range_of_plants()


if __name__ == "__main__":
    extract_data()
