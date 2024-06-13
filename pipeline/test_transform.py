import pytest
import pandas as pd
from transform import remove_errors, remove_invalid_values, set_correct_data_types, split_location_data_into_columns
from io import StringIO
import json


@pytest.fixture
def example_dataframe():
    example_data = [
        {"botanist": {"email": "gertrude.jekyll@lnhm.co.uk",
                      "name": "Gertrude Jekyll",
                      "phone": "001-481-273-3691x127"},
            "last_watered": "Mon, 10 Jun 2024 13:54:32 GMT", "name": "Venus flytrap",
            "origin_location": ["33.95015", "-118.03917", "South Whittier", "US", "America/Los_Angeles"],
            "plant_id": 1,
            "recording_taken": "2024-06-11 11:29:25",
            "soil_moisture": 23.52996228937009, "temperature": 12.033255788902762
         },

        {"botanist": {"email": "carl.linnaeus@lnhm.co.uk",
                      "name": "Carl Linnaeus",
                      "phone": "(146)994-1635x35992"},
         "last_watered": "Mon, 10 Jun 2024 14:10:54 GMT",
         "name": "Corpse flower",
         "origin_location": ["7.65649", "4.92235", "Efon-Alaaye", "NG", "Africa/Lagos"],
         "plant_id": 2,
         "recording_taken": "2024-06-11 11:30:55",
         "soil_moisture": 30.116904269335762,
         "temperature": 9.138506163148168
         },
        {"error": "plant not found", "plant_id": 7},

        {"botanist": {"email": "carl.linnaeus@lnhm.co.uk",
                      "name": "Carl Linnaeus",
                      "phone": "(146)994-1635x35992"},
         "last_watered": "Mon, 10 Jun 2024 14:10:54 GMT",
         "name": "Corpse flower",
         "origin_location": ["7.65649", "4.92235", "Efon-Alaaye", "NG", "Africa/Lagos"],
         "plant_id": 2,
         "recording_taken": "2024-06-11 11:30:55",
         "temperature": 9.138506163148168
         }
    ]
    plants_df = pd.json_normalize(example_data)
    return plants_df


def test_remove_errors(example_dataframe):
    no_error_df = remove_errors(example_dataframe)
    assert no_error_df['soil_moisture'].isnull().values.any() == False


def test_remove_invalid_values(example_dataframe):
    ...


def test_set_correct_data_types(example_dataframe):
    example_dataframe = remove_errors(example_dataframe)
    example_dataframe = split_location_data_into_columns(example_dataframe)
    changed_datatypes_df = set_correct_data_types(example_dataframe)
    assert changed_datatypes_df.dtypes['location_lon'] == 'float64'
    assert changed_datatypes_df.dtypes['location_lat'] == 'float64'


def test_split_location_data_into_columns(example_dataframe):
    """Tests whether correct columns are added when splitting location into columns"""
    example_dataframe = remove_errors(example_dataframe)
    split_dataframe = split_location_data_into_columns(example_dataframe)
    assert ['location_lon'] in split_dataframe.columns.values
    assert ['location_lat'] in split_dataframe.columns.values
    assert ['location_city'] in split_dataframe.columns.values
    assert ['country_code'] in split_dataframe.columns.values
    assert ['timezone'] in split_dataframe.columns.values
