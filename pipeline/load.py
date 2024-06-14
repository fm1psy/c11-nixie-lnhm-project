"""Load pipeline script"""
from os import environ as ENV
import csv
from dotenv import load_dotenv
from pymssql import connect, Connection
TRANSFORM_DESTINATION = '/tmp/transformed_plants.csv'


def load_data(filename: str) -> list:
    """Load csv into a list of dictionary"""
    with open(filename, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)
    return rows


def get_con():
    """Get connection to the database"""
    return connect(
        server=ENV["DB_HOST"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"],
        database=ENV["DB_NAME"],
        as_dict=True
    )


def output_table(cursor: Connection.cursor, table: str) -> list[dict]:
    """Returns a specified table. """
    cursor.execute(f"""SELECT * FROM beta.{table};""")
    return cursor.fetchall()


def insert_country_code(conn: Connection, codes: list[tuple[str]]) -> list[dict]:
    """Insert country code and return the table output as a dictionary. """
    with conn.cursor() as cur:
        for code in codes:
            if code[0]:
                cur.execute(
                    """
                    SELECT *
                    FROM beta.country
                    WHERE CONVERT(VARCHAR, country_code) = (%s)
                    ;
                    """, code)
            else:
                cur.execute(
                    """
                    SELECT *
                    FROM beta.country
                    WHERE country_code IS NULL
                    ;
                    """)
            result = cur.fetchone()
            if not result:
                cur.execute("""
                        INSERT INTO beta.country (country_code)
                        VALUES (%s);
                        """,
                            code)
        result = output_table(cur, 'country')
    conn.commit()
    return result


def insert_plant_type(conn: Connection, types: list[tuple[str]]) -> list[dict]:
    """Insert plant scientific and normal name into table and return table as output. """
    with conn.cursor() as cur:
        for plant_type in types:
            cur.execute(
                """
                SELECT *
                FROM beta.plant_type
                WHERE CONVERT(VARCHAR, plant_name) = (%s)
                ;
                """, (plant_type[1]))
            result = cur.fetchone()
            if not result:
                cur.execute("""
                        INSERT INTO beta.plant_type (plant_scientific_name, plant_name)
                        VALUES (%s, %s);
                        """,
                            plant_type)
        result = output_table(cur, 'plant_type')
    conn.commit()
    return result


def insert_botanist(conn: Connection, data: list[tuple[str]]) -> list[dict]:
    """Insert botanist information into botanist table. """
    with conn.cursor() as cur:
        for info in data:
            cur.execute(
                """
                SELECT *
                FROM beta.botanist
                WHERE CONVERT(VARCHAR, botanist_full_name) = (%s)
                ;
                """, (info[0]))
            result = cur.fetchone()
            if not result:
                cur.execute("""
                        INSERT INTO beta.botanist (botanist_full_name, botanist_email, botanist_phone_no)
                        VALUES (%s, %s, %s);
                        """, info)
            elif result:
                if result['botanist_email'] != info[1]:
                    print(
                        f"Updating new email for {result['botanist_full_name']}")
                    cur.execute("""
                            UPDATE beta.botanist
                            SET botanist_email = (%s)
                            WHERE botanist_id = (%s);
                                """, (info[1], result['botanist_id']))
                if result['botanist_phone_no'] != info[2]:
                    print(
                        f"Updating new phone for {result['botanist_full_name']}")
                    cur.execute("""
                            UPDATE beta.botanist
                            SET botanist_phone_no = (%s)
                            WHERE botanist_id = (%s);
                                """, (info[2], result['botanist_id']))
        result = output_table(cur, 'botanist')
    conn.commit()
    return result


def get_country_id(conn: Connection, code: str) -> int:
    """Get the country_id from beta.country table or 
    creates it if it doesn't exists in the table and return the new id. """
    country_table = insert_country_code(conn, [(code,)])
    return [row['country_id'] for row in country_table if row['country_code'] == code][0]


def insert_location(conn: Connection, data: list[tuple[str]]) -> list[dict]:
    """Insert location details into location table. """
    with conn.cursor() as cur:
        for info in data:
            if info[0] and info[0]:
                cur.execute(
                    """
                    SELECT *
                    FROM beta.location
                    WHERE location_lon = (%s) and location_lat = (%s)
                    ;
                    """, (info[0], info[1]))
            else:
                cur.execute(
                    """
                    SELECT *
                    FROM beta.location
                    WHERE location_lon IS NULL and location_lat IS NULL
                    ;
                    """)
            result = cur.fetchone()
            if not result:
                cur.execute(
                    """
                    INSERT INTO beta.location (location_lon, location_lat, location_city, country_id, timezone)
                    VALUES (%s, %s, %s, %s, %s)
                    """, info)
        result = output_table(cur, 'location')
    conn.commit()
    return result


def get_plant_type_id(conn: Connection, plant_names: tuple[str]) -> int:
    """Get the plant_type_id using the plant_name. """
    plant_type_table = insert_plant_type(conn, [plant_names])
    return [row['plant_type_id'] for row in plant_type_table
            if row['plant_name'] == plant_names[1]][0]


def get_botanist_id(conn: Connection, info: tuple[str]) -> int:
    """Get the botanist id using the botanist full name. """
    botanist_table = insert_botanist(conn, [info])
    return [row['botanist_id'] for row in botanist_table if row['botanist_full_name'] == info[0]][0]


def get_location_id(conn: Connection, info: tuple[str]) -> int:
    """Get the location_id using the long, lat details. """
    location_table = insert_location(conn, [info])
    if info[0] and info[1]:
        return [row['location_id'] for row in location_table
                if (row['location_lon'] == float(info[0])
                    and row['location_lat'] == float(info[1]))][0]
    return [row['location_id'] for row in location_table
            if (row['location_lon'] == info[0] and row['location_lat'] == info[1])][0]


def insert_plant(conn: Connection, data: list[tuple[str]]) -> list[dict]:
    """Insert plant details into plant table. """
    with conn.cursor() as cur:
        for info in data:
            cur.execute("""
                        SELECT * FROM beta.plant
                        WHERE plant_id = (%s)
                        """, info[0])
            result = cur.fetchone()
            if not result:
                cur.execute("""
                            INSERT INTO beta.plant (plant_id, plant_type_id, location_id, botanist_id)
                            VALUES (%s, %s, %s, %s)
                            """, info)
        result = output_table(cur, 'plant')
    conn.commit()
    return result


def get_plant_id(conn: Connection, info: tuple[str]) -> int:
    """Get the plant id using the plant_id. """
    plant_table = insert_plant(conn, [info])
    return [row['plant_id'] for row in plant_table if row['plant_id'] == info[0]][0]


def insert_recording(conn: Connection, data: list[tuple[str]]) -> list[dict]:
    """Insert recording data into the recording table. """
    with conn.cursor() as cur:
        for info in data:
            cur.execute("""
                        INSERT INTO beta.recording (plant_id, recording_taken, soil_moisture, temperature, last_watered)
                        VALUES (%s, %s, %s, %s, %s)
                        """, info)
        conn.commit()
        result = output_table(cur, 'recording')
    return result


def loading_data(conn: Connection, data: list[dict]) -> list[dict]:
    """Loads csv data into the database. """
    for row in data:
        country_id = get_country_id(conn, row['country_code'])
        plant_type_id = get_plant_type_id(
            conn, (row['scientific_name'], row['name']))
        botanist_id = get_botanist_id(
            conn, (row['botanist.name'], row['botanist.email'], row['botanist.phone']))
        location_id = get_location_id(
            conn, (row['location_lon'], row['location_lat'],
                   row['location_city'], country_id, row['timezone']))
        plant_id = get_plant_id(
            conn, (row['plant_id'], plant_type_id, location_id, botanist_id))
        recording_row = (plant_id, row['recording_taken'], row['soil_moisture'],
                         row['temperature'], row['last_watered'])
        result = insert_recording(conn, [recording_row])
    return result


def format_values(data: list[dict]) -> list[dict]:
    """Sets empty values to None. Corrects data types csv changed. """
    for row in data:
        for key in row:
            if isinstance(row[key], str) and len(row[key]) == 0:
                row[key] = None
            if row[key] and key == 'plant_id':
                row[key] = int(float(row[key]))
            if row[key] and (key in ('soil_moisture', 'temperature')):
                row[key] = float(row[key])
            if row[key] and key == 'scientific_name':
                row[key] = row[key].replace(
                    "[", "").replace("]", "").replace("'", "").replace('"', '')
    return data


def loading_main():
    """Main run of functions. """
    load_dotenv()
    connection = get_con()
    data = format_values(load_data(TRANSFORM_DESTINATION))
    loading_data(connection, data)
    connection.close()


if __name__ == "__main__":
    loading_main()
