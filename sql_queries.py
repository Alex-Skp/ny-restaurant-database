import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('./credentials/dwh.cfg')

# DROP TABLES

staging_trips_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_restaurants_table_drop = "DROP TABLE IF EXISTS staging_songs;"

# CREATE TABLES

staging_tripes_table_create="""
CREATE TABNLE IF NOT EXISTS staging_trips(

    datetime        DATETIME    NOT NULL    SORTKEY,
    latitude        DECIMAL     NOT NULL,
    longitude       DECIMAL     NOT NULL,    
    base            VARCHAR         
);
"""

staging_restaurants_table_create="""
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
    phone           VARCHAR,
    categories      VARCHAR
); 
"""

