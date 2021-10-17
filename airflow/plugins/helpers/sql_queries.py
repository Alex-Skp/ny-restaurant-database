class SqlQueries:
    
    address_table_insert = ("""
        SELECT DISTINCT address1 AS address1
        , address2 AS address2
        , address3 AS address3
        , city AS city
        , zip_code AS zip_code
        , country AS country
        , state AS state
        FROM staging_restaurants
    """)

    restaurant_table_insert = ("""
        SELECT DISTINCT id                          AS restaurant_id
        , name                                      AS name
        , image_url                                 AS image_url
        , yelp_url                                  AS yelp_url
        , review_count                              AS review_count 
        , latitude                                  AS latitude
        , longitude                                 AS longitude
        , price                                     AS price
        , ( SELECT at.address_id 
            FROM address_table AS at 
            WHERE sr.address1=at.address1 
            AND sr.zip_code=at.zip_code 
            ORDER BY at.address_id 
            LIMIT 1)                                AS address_id
        , phone                                     AS phone
        , ( SELECT qt.quadrant_id 
            FROM quadrant_table AS qt 
            WHERE (sr.latitude BETWEEN qt.lat_from AND qt.lat_to)
            AND (sr.longitude BETWEEN qt.lon_from AND qt.lon_to)
            ORDER BY qt.quadrant_id DESC LIMIT 1)   AS quadrant_id
        FROM staging_restaurants AS sr
    """)

    pickup_table_insert = ("""
        SELECT DISTINCT datetime                AS datetime
        , latitude                              AS latitude
        , longitude                             AS longitude
        , ( SELECT qt.quadrant_id 
            FROM quadrant_table AS qt 
            WHERE (st.latitude BETWEEN qt.lat_from AND qt.lat_to)
            AND (st.longitude BETWEEN qt.lon_from AND qt.lon_to)
            ORDER BY quadrant_id DESC LIMIT 1)  AS quadrant_id
        , station                               AS station
        FROM staging_trips AS st
    """)

    time_table_insert = ("""
        SELECT DISTINCT datetime            AS datetime
        , extract(hour from datetime)       AS hour
        , extract(day from datetime)        AS day
        , extract(week from datetime)       AS week
        , extract(month from datetime)      AS month
        , extract(year from datetime)       AS year
        , extract(dayofweek from datetime)  AS weekday
        FROM staging_trips
    """)