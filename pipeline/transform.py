import pandas as pd
import json


def get_dataframe_from_json():
    """creates dataframe from json extracted in extract.py"""
    with open('extracted_plants.json') as file:
        plants = json.load(file)
    return pd.json_normalize(plants)


def remove_images_columns(plants_df):
    """removes all columns concerning images"""
    plants_df.loc[:, ~plants_df.columns.str.startswith('images')]
    return plants_df


def remove_errors(plants_df):
    """removes rows that have missing key information"""
    plants_df = plants_df.dropna(
        subset=['name', 'soil_moisture', 'temperature', 'last_watered', 'plant_id'])
    plants_df = plants_df.drop('error', axis=1)
    return plants_df


def remove_invalid_values(plants_df):
    """removes values that are not within a valid range"""
    plants_df = plants_df[plants_df['soil_moisture'] < 100]
    plants_df = plants_df[plants_df['soil_moisture'] > 0]
    plants_df = plants_df[plants_df['temperature'] < 50]
    plants_df = plants_df[plants_df['temperature'] > 0]
    plants_df = plants_df[plants_df['plant_id'] > 0]
    return plants_df


def set_correct_data_types(plants_df):
    """changes data types to the correct data type"""
    plants_df['botanist.email'] = plants_df["botanist.email"].astype(str)
    plants_df['location_lon'] = plants_df["location_lon"].astype(float)
    plants_df['location_lat'] = plants_df["location_lat"].astype(float)
    plants_df['recording_taken'] = pd.to_datetime(
        plants_df['recording_taken'], format='%Y-%m-%d %X')
    plants_df['last_watered'] = pd.to_datetime(
        plants_df['last_watered'], format='%a, %d %b %Y %X GMT')
    return plants_df


def split_location_data_into_columns(plants_df):
    """splits list with location data into separate columns for each piece of data"""
    location = pd.DataFrame(plants_df['origin_location'].to_list(), columns=[
        'location_lon', 'location_lat', 'location_city', 'country_code', 'timezone'])
    plants_df = pd.concat([plants_df, location], axis=1)
    plants_df = plants_df.drop('origin_location', axis=1)
    return plants_df


def dataframe_to_csv(plants_df):
    """converts dataframe into a csv file"""
    plants_df.to_csv('transformed_plants.csv', index=False)


def transform():
    """calls all necessary functions for cleaning and transforming the data"""
    plants_df = get_dataframe_from_json()
    plants_df = remove_images_columns(plants_df)
    plants_df = remove_errors(plants_df)
    plants_df = split_location_data_into_columns(plants_df)
    plants_df = remove_invalid_values(plants_df)
    plants_df = set_correct_data_types(plants_df)
    dataframe_to_csv(plants_df)


if __name__ == "__main__":
    transform()
