import pandas as pd
import json


def get_dataframe_from_json():
    """creates dataframe from json extracted in extract.py"""
    with open('example.json') as file:
        plants = json.load(file)
    return pd.json_normalize(plants)


def remove_errors():
    ...


def remove_invalid_values(plants_df):
    plants_df = plants_df[plants_df['soil_moisture'] < 100]
    plants_df = plants_df[plants_df['soil_moisture'] > 0]
    plants_df = plants_df[plants_df['temperature'] < 50]
    plants_df = plants_df[plants_df['temperature'] > 0]


def split_location_data_into_columns(plants_df):
    location = pd.DataFrame(plants_df['origin_location'].to_list(), columns=[
        'location_lon', 'location_lat', 'location_city', 'country_code', 'timezone'])
    plants_df = pd.concat([plants_df, location], axis=1)
    plants_df = plants_df.drop('origin_location', axis=1)
    return plants_df


if __name__ == "__main__":
    plants_df = get_dataframe_from_json()
    plants_df = split_location_data_into_columns(plants_df)
    print(plants_df)
