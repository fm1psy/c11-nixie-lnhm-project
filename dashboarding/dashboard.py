from datetime import date
from os import environ
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import altair as alt
from connection import get_conn, get_all_recordings, get_plant_id_origin_country, get_hour_since_last_watered, get_range_of_soil_moisture, get_range_of_temperature


def line_plot_soil_to_time(plant_id: int, records: pd.DataFrame) -> alt.Chart:
    """Line graph of a plant's soil moisture over time. """
    plant_records = records[records['plant_id'] == plant_id]
    plant_records['soil_moisture'] = plant_records['soil_moisture'].apply(
        lambda x: round(x, 2))
    return alt.Chart(plant_records).mark_line().encode(
        x=alt.X('recording_taken', type='temporal'),
        y=alt.Y('soil_moisture', type='nominal')
    ).properties(title=f"Soil moisture over time for plant {plant_id}")


def line_plot_temp_to_time(plant_id: int, records: pd.DataFrame) -> alt.Chart:
    """Line graph of a plant's soil moisture over time. """
    plant_records = records[records['plant_id'] == plant_id]
    plant_records['temperature'] = plant_records['temperature'].apply(
        lambda x: round(x, 2))
    return alt.Chart(plant_records).mark_line().encode(
        x=alt.X('recording_taken', type='temporal'),
        y=alt.Y('temperature')
    ).properties(title=f"Temperature over time for plant {plant_id}")


def get_unique_plant_ids(record: pd.DataFrame) -> list:
    return record['plant_id'].unique().tolist()


def get_origin_of_plant(plant_origin: pd.DataFrame, plant_id) -> str:
    origin = plant_origin[plant_origin['plant_id'] == plant_id]
    return origin['country_code'].to_string(index=False)


def get_time_since_last_water(last_watered: pd.DataFrame, plant_id) -> int:
    time = last_watered[last_watered['plant_id'] == plant_id]
    value = time['hours_since_last_watered'].to_string(index=False)
    return value if value else 0


def get_soil_range(soil_range: pd.DataFrame, plant_id) -> int:
    plant_data = soil_range[soil_range['plant_id'] == plant_id]
    lowest = plant_data['lowest_soil_moisture'].to_string(index=False)
    highest = plant_data['highest_soil_moisture'].to_string(index=False)
    avg = plant_data['average_soil_moisture'].to_string(index=False)
    return (lowest, highest, avg)


def get_temp_range(temp_range: pd.DataFrame, plant_id) -> int:
    plant_data = temp_range[temp_range['plant_id'] == plant_id]
    lowest = plant_data['lowest_temperature'].to_string(index=False)
    highest = plant_data['highest_temperature'].to_string(index=False)
    avg = plant_data['average_temperature'].to_string(index=False)
    return (lowest, highest, avg)


if __name__ == "__main__":
    load_dotenv()
    connection = get_conn()
    record_df = get_all_recordings(connection)

    st.title(
        "LMNH Plant Health Dashboard")

    plant_ids = get_unique_plant_ids(record_df)
    plants_origin_df = get_plant_id_origin_country(connection)
    plant_last_watered_df = get_hour_since_last_watered(connection)
    plant_soil_range_df = get_range_of_soil_moisture(connection)
    plant_temp_range_df = get_range_of_temperature(connection)

    connection.close()

    option = st.sidebar.selectbox("Select a plant id.", plant_ids)
    ranges = get_soil_range(plant_soil_range_df, option)
    print(ranges)

    n_col_1, n_col_2 = st.columns(2)
    with n_col_1:
        origin = get_origin_of_plant(plants_origin_df, option)
        st.metric("Plant origin", origin)
        time_past = get_time_since_last_water(plant_last_watered_df, option)
        st.metric("Minutes since last watered", time_past)

    with n_col_2:
        ranges = get_soil_range(plant_soil_range_df, option)
        sub_1, sub_2, sub_3 = st.columns(3)
        with sub_1:
            st.metric("Highest Soil Moisture", ranges[1])
        with sub_2:
            st.metric("Lowest Soil Moisture", ranges[0])
        with sub_3:
            st.metric("Average Soil Moisture", ranges[2])

        t_ranges = get_temp_range(plant_temp_range_df, option)
        tsub_1, tsub_2, tsub_3 = st.columns(3)
        with tsub_1:
            st.metric("Highest Temperature", t_ranges[1])
        with tsub_2:
            st.metric("Lowest Temperature", t_ranges[0])
        with tsub_3:
            st.metric("Average Temperature", t_ranges[2])

    col_1, col_2 = st.columns(2)
    with col_1:
        st.write(line_plot_temp_to_time(option, record_df))
    with col_2:
        st.write(line_plot_soil_to_time(option, record_df))
