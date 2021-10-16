import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('./credentials/dwh.cfg')

# DROP TABLES

staging_trips_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_restaurants_table_drop = "DROP TABLE IF EXISTS staging_songs;"
address_table_drop = "DROP TABLE IF EXISTS address;"
restaurant_table_drop = "DROP TABLE IF EXISTS restaurant;"
quadrant_table_drop = "DROP TABLE IF EXISTS quadrant;"
pickup_table_drop = "DROP TABLE IF EXISTS pickup;"
time_table_drop = "DROP TABLE IF EXISTS time;"

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
    latitude        DECIMAL     NOT NULL,
    longitude       DECIMAL     NOT NULL,
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
    address_id      INT IDENTITY(0,1)       PRIMARY KEY,
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
    quadrant_id     VARCHAR     NOT NULL,
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

drop_table_queries = [staging_trips_table_drop, staging_restaurants_table_drop, address_table_drop, restaurant_table_drop, quadrant_table_drop, time_table_drop]
create_table_queries = [staging_trips_table_create, staging_restaurants_table_create, address_table_create, restaurant_table_create, quadrant_table_create, time_table_create]