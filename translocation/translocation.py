from os import environ as ENV
from dotenv import load_dotenv
from pymssql import connect, Connection
import pandas as pd
from boto3 import client
from datetime import date, timedelta
from os import environ


def get_con():
    """Get connection to the database"""
    load_dotenv()
    return connect(
        server=ENV["DB_HOST"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"],
        database=ENV["DB_NAME"],
        as_dict=True
    )


def get_averages_df(conn):
    with conn.cursor() as cur:
        cur.execute("""select p.plant_id, AVG(r.temperature) as 'Average Temperature', AVG(r.soil_moisture) as 'Average Soil Moisture' from beta.plant as p 
                    join beta.recording as r 
                    on r.plant_id = p.plant_id
                    GROUP BY p.plant_id;""")
        results = cur.fetchall()
    averages_df = pd.DataFrame(results)
    return averages_df


def get_last_watered_df(conn):
    with conn.cursor() as cur:
        cur.execute("""select p.plant_id, pt.plant_name, r.last_watered as 'Last Watered' from beta.plant as p 
            join beta.recording as r 
            on r.plant_id = p.plant_id
            join beta.plant_type as pt 
            on p.plant_type_id = pt.plant_type_id
            where r.recording_taken = (select max(r.recording_taken) from beta.recording as r where r.plant_id = p.plant_id);""")
        results = cur.fetchall()
    last_watered_df = pd.DataFrame(results)
    return last_watered_df


def combine_df(last_watered_df, averages_df):
    full_df = last_watered_df.merge(averages_df)
    return full_df.sort_values(by=['plant_id'])


def convert_to_csv(full_df):
    """converts dataframe into a csv file"""
    full_df.to_csv(create_file_name(), index=False)
    return create_file_name()


def upload_to_s3(client, file_name, bucket):
    try:
        client.upload_file(file_name, bucket, file_name)
    except Exception as err:
        return {'error': 'error uploading to s3 bucket'}


def get_client():
    """gets s3 client"""
    return client('s3', aws_access_key_id=environ["ACCESS_KEY"],
                  aws_secret_access_key=environ["SECRET_ACCESS_KEY"])


def create_file_name():
    today = date.today()
    yesterday = today - timedelta(days=1)
    return f"lmnh-data-summary-{yesterday}.csv"


def clear_database(conn):
    with conn.cursor() as curr:
        curr.execute("DELETE FROM beta.recording;")
        conn.commit()


def lambda_handler():
    conn = get_con()
    average_df = get_averages_df(conn)
    last_watered_df = get_last_watered_df(conn)
    full_df = combine_df(last_watered_df, average_df)
    csv = convert_to_csv(full_df)
    client = get_client()
    upload_to_s3(client, csv, "nixie-lmnh-plants-lts")
    clear_database(conn)


if __name__ == "__main__":
    lambda_handler()
