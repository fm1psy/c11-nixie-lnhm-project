from os import environ as ENV
from dotenv import load_dotenv
from pymssql import connect, Connection
import pandas as pd


def get_conn() -> Connection:
    """Connects to the database. """
    return connect(
        server=ENV["DB_HOST"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"],
        database=ENV["DB_NAME"],
        as_dict=True
    )


def get_all_recordings(conn: Connection) -> pd.DataFrame:
    """Get all recordings data from the recording table. """
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM beta.recording;")
        result = cur.fetchall()
    return pd.DataFrame(result)


def get_hour_since_last_watered(conn: Connection) -> pd.DataFrame:
    """Get the last watered value for each plant id."""
    with conn.cursor() as cur:
        # get the latest date recorded:
        cur.execute(
            """
                    WITH LatestRecording AS (
                        SELECT 
                            plant_id, 
                            last_watered,
                            ROW_NUMBER() OVER (PARTITION BY plant_id ORDER BY recording_taken DESC) AS rn
                        FROM 
                            beta.recording
                    )
                    SELECT 
                        plant_id, 
                        last_watered,
                        DATEDIFF(MINUTE, last_watered, SYSDATETIMEOFFSET()) AS hours_since_last_watered
                    FROM 
                        LatestRecording
                    WHERE 
                        rn = 1;
                    """)
        result = cur.fetchall()
    return pd.DataFrame(result)


def get_range_of_soil_moisture(conn: Connection) -> pd.DataFrame:
    """Get the range and average of soil moisture values for each plant"""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 
                plant_id,
                MIN(soil_moisture) AS lowest_soil_moisture,
                MAX(soil_moisture) AS highest_soil_moisture,
                AVG(soil_moisture) AS average_soil_moisture
            FROM
                beta.recording
            GROUP BY
                plant_id;
            """)
        result = cur.fetchall()
    return pd.DataFrame(result)


def get_range_of_temperature(conn: Connection) -> pd.DataFrame:
    """Get the range and average of soil moisture values for each plant"""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 
                plant_id,
                MIN(temperature) AS lowest_temperature,
                MAX(temperature) AS highest_temperature,
                AVG(temperature) AS average_temperature
            FROM
                beta.recording
            GROUP BY
                plant_id;
            """)
        result = cur.fetchall()
    return pd.DataFrame(result)


def get_plant_id_origin_country(conn: Connection) -> pd.DataFrame:
    """Get the origin country of the plants. """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT pt.plant_id, c.country_code
            FROM beta.plant AS pt
            JOIN beta.location as loc ON pt.location_id = loc.location_id
            JOIN beta.country as c ON c.country_id = loc.country_id;
            """)
        result = cur.fetchall()
    return pd.DataFrame(result)


if __name__ == "__main__":
    load_dotenv()
    connection = get_conn()
    df = get_plant_id_origin_country(connection)
    print(df)
    connection.close()
