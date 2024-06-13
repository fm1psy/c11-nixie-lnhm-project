DROP TABLE IF EXISTS beta.recording;
DROP TABLE IF EXISTS beta.plant;
DROP TABLE IF EXISTS beta.location;
DROP TABLE IF EXISTS beta.botanist;
DROP TABLE IF EXISTS beta.country;
DROP TABLE IF EXISTS beta.plant_type;

CREATE TABLE beta.plant_type (
    plant_type_id INT IDENTITY(1, 1),
    plant_scientific_name TEXT,
    plant_name TEXT NOT NULL,
    PRIMARY KEY (plant_type_id)
)

CREATE TABlE beta.country (
    country_id INT IDENTITY(1, 1),
    country_code TEXT,
    PRIMARY KEY (country_id)
)

-- INSERT INTO beta.country (country_code)
-- VALUES 
-- ("BR"), 
-- ("US"), 
-- ("NG"), 
-- ("SV"), 
-- ("IN"), 
-- ("CA"), 
-- ("CI"), 
-- ("DE"), 
-- ("HR"), 
-- ("TN"), 
-- ("ID"), 
-- ("BW"), 
-- ("ES"), 
-- ("JP"), 
-- ("SD"), 
-- ("DZ"), 
-- ("UA"), 
-- ("LY"), 
-- ("CN"), 
-- ("CL"), 
-- ("TZ"), 
-- ("FR"),
-- ("BG"),
-- ("MX"), 
-- ("MW"), 
-- ("IT"), 
-- ("PH")
-- ;

CREATE TABLE beta.botanist (
    botanist_id INT IDENTITY(1, 1),
    botanist_full_name TEXT NOT NULL,
    botanist_email TEXT,
    botanist_phone_no TEXT,
    PRIMARY KEY (botanist_id)
)

CREATE TABLE beta.location (
    location_id INT IDENTITY(1, 1),
    location_lon FLOAT,
    location_lat FLOAT,
    location_city TEXT,
    country_id INT NOT NULL,
    timezone TEXT,
    PRIMARY KEY (location_id),
    FOREIGN KEY (country_id) REFERENCES beta.country(country_id)
)

CREATE TABLE beta.plant (
    plant_id INT NOT NULL,
    plant_type_id INT NOT NULL,
    location_id INT NOT NULL,
    botanist_id INT NOT NULL,
    PRIMARY KEY (plant_id),
    FOREIGN KEY (plant_type_id) REFERENCES beta.plant_type(plant_type_id),
    FOREIGN KEY (location_id) REFERENCES beta.location(location_id),
    FOREIGN KEY (botanist_id) REFERENCES beta.botanist(botanist_id)
)

CREATE TABLE beta.recording (
    recording_id BIGINT IDENTITY(1, 1) NOT NULL,
    plant_id INT NOT NULL,
    recording_taken DATETIME NOT NULL,
    soil_moisture DECIMAL(17,15) NOT NULL,
    temperature DECIMAL(17,15) NOT NULL,
    last_watered DATETIMEOFFSET NOT NULL,
    PRIMARY KEY (recording_id),
    FOREIGN KEY (plant_id) REFERENCES beta.plant(plant_id)
)

