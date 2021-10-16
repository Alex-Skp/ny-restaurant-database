import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('./credentials/dwh.cfg')

# DROP TABLES

staging_trips_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_restaurants_table_drop = "DROP TABLE IF EXISTS staging_songs;"

# CREATE TABLES

staging_trips_table_create = """
CREATE TABLE IF NOT EXISTS staging_trips(
    datetime        DATETIME    NOT NULL    SORTKEY,
    latitude        DECIMAL     NOT NULL,
    longitude       DECIMAL     NOT NULL,    
    base            VARCHAR         
);
"""

staging_restaurants_table_create = """
CREATE TABLE IF NOT EXISTS staging_restaurants(
    id              VARCHAR     NOT NULL    PRIMARY KEY,
    name            VARCHAR     NOT NULL,
    image_url       VARCHAR,
    yelp_url        VARCHAR,
    review_count    INTEGER,
    latitude        DECIMAL     NOT NULL    SORTKEY,
    longitude       DECIMAL     NOT NULL    SORTKEY,
    price           VARCHAR,
    address1        VARCHAR,
    address2        VARCHAR,
    address3        VARCHAR,
    city            VARCHAR,
    zip_code        VARCHAR,
    country         VARCHAR,
    state           VARCHAR,
    phone           VARCHAR
); 
"""

address_table_create = """
CREATE TABLE IF NOT EXISTS address_table(  
    address_id      SERIAL      PRIMARY KEY SORTKEY,
    address1        VARCHAR     NOT NULL,
    address2        VARCHAR,
    address3        VARCHAR,
    city            VARCHAR     NOT NULL,
    zip_code        VARCHAR     NOT NULL,
    country         VARCHAR     NOT NULL,
    state           VARCHAR     NOT NULL
);
"""

restaurant_table_create = """
CREATE TABLE IF NOT EXISTS restaurant_table(
    restaurant_id   VARCHAR     PRIMARY KEY SORTKEY,
    name            VARCHAR     NOT NULL,
    image_url       VARCHAR,
    yelp_url        VARCHAR,
    review_count    INTEGER,
    latitude        DECIMAL     NOT NULL,
    longitude       DECIMAL     NOT NULL,
    price           VARCHAR,
    address_id      INTEGER     NOT NULL,
    phone           VARCHAR,
    quadrant_id     VARCHAR     NOT NULL
);
"""

quadrant_table_create = """
CREATE TABLE IF NOT EXISTS quadrant_table(
    quadrant_id     VARCHAR     PRIMARY KEY SORTKEY,
    lat_from        DECIMAL     NOT NULL,
    lat_to          DECIMAL     NOT NULL,
    lon_from        DECIMAL     NOT NULL,
    lon_to          DECIMAL     NOT NULL
);
"""
pickup_table_create = """
CREATE TABLE IF NOT EXISTS pickup_table_create(
    datetime        DATETIME    SORTKEY,
    latitude        DECIMAL     NOT NULL,
    longitude       DECIMAL     NOT NULL,
    quadrant_id     VARCHAR     NOT NULL
    station         VARCHAR
);
"""
time_table_create = """
CREATE TABLE IF NOT EXISTS time_table(
    datetime        DATETIME    PRIMARY KEY SORTKEY,
    hour            INTEGER     NOT NULL,
    day             INTEGER     NOT NULL,
    week            INTEGER     NOT NULL,
    month           INTEGER     NOT NULL,
    year            INTEGER     NOT NULL,
    weekday         INTEGER     NOT NULL
);
"""