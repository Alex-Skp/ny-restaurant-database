# Creating a New York restaurant traffic database 
## *for Udacity's data engineering nanodegree capstone project*
### By AlexSkp

## Purpose of the project
___
In this project we will create a small database in order to allow analysts take measures of foot traffic in the city of New York, for the specific purpose of find good locations for opening new branches of our food business. We are targeting a persona that pick up ubers to move around the city.
In order to achieve this, we combined two sources of data: Restaurant data from Yelp's API, and a dataset of uber customer pick-ups. To enrich our dataset and allow for further analysis, we also engineered a new table that divides the city of New York in rectangular areas of aproximately the size of 2x2 blocks, and codified them, in order to combine and connect uber pickups with the location of restaurants. 

## Methodology
___
### Finding our data
* We first need to retrieve our data. We started by the uber dataset. You can download it  [here](https://www.kaggle.com/fivethirtyeight/uber-pickups-in-new-york-city?search=uber&select=uber-raw-data-aug14.csv).
We focused only in the csvs of 2014, as they were already 4M+ lines of pickup data. Data spans from april to September. We wanted data that follows a continuous timeline to simulate how our ETL process would feed from data retrieved in previous steps. After downloading, we followed the steps described in [split_data.ipynb](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/split_data.ipynb), as we wanted the data structured in folders by year, month and day, as well as in small enough chunks for fast data transfers using COPY commands in redshift. The data is stored in csv files
* To make the grid table we created a table with grids that cover all our uber traffic data. Some of the restaurants happened to be in the peripheric areas of the city but we won't be interested in analyzing those. We defined a function in [functions.py](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/functions.py) to loop and calculate the grids, as well as generating an quadrant ID for each one. running [generate_coord_grid.py](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/generate_coord_grid.py) would create this grid table and save it as a csv locally.
* For the NY restaurants we had to ask for an educational API key from [Yelp](https://www.yelp.com/developers) and then i took inspiration from a great repository i found from rspiro9 who makes a great EDA of NYC food ratings [here](https://github.com/rspiro9/NYC-Restaurant-Yelp-and-Inspection-Analysis/blob/main/1.%20Exploratory%20Data%20Analysis.ipynb). The steps I took for the retrieval can be found in [scraping_data.ipynb](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/scraping_data.ipynb) and dump them locally. We saved json files that we modified to JSONLine format in order to feed it to redshift. To tell redshift where the columns are in our json files, we created this [JSONpath](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/NYrestaurants-jsonpath%20copy.json) file.
* After gathering all data, I uploaded it in a public S3 bucket from my AWS console and went directly to build the pipeline.

### Building the pipeline 
Our pipeline would look like this:
1. Retrieve our data, process it locally and upload it to a S3 bucket. Uber data had
2. Set up a cluster in Amanzon Redshift to copy the data to, by creating the tables in the cluster first, running [create_tables.py](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/create_tables.py). The queries executed are stored in [sql_queries.py](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/sql_queries.py). There you will find queries that create staging queries, as well as the end tables where the transformed data will be. After this we created a cluster programatically in [create_cluster.ipynb](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/create_cluster.ipynb). To run our code here, we had an active AWS account, and we stored all keys in a local config file. 
3. Create a scheduled pipeline in Airflow that will stage our data, make some data quality tests, then transform it and load it in the final tables, making a second data quality test in the end. The pipeline would run daily at 7 am, as we set this time as the start runtime of our DAG, and it's scheduled to run daily. 
4. The data would be ready for our users to query against. 

![pipeline_chart](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/images/AWS%20schema%20project%20.png?raw=true)

### Airflow DAG process. 
In the folder [airflow](https://github.com/Alex-Skp/udacity-capstone-project/tree/main/airflow) you will find all the files ran in the airflow instance. In the following image you can see the different operators we set up to make all the data transfers, as well as the data test. We made sure there were no empty tables after the transfers happened. 
1. First we initialized the DAG with a dummy operator, then staged the full restaurant data and the trip data of that day run, and we upload the coordinates table, as it is artificially generated by us. 
2. We transformed and load the data into the final tables. There was a dependency as we wanted to separate the address data from the restaurant data, so we had to load the addresses first, then connect them tot he restaurant table.
3. Check that the data arrived properly to the destination tables to our business analysts to query. 

![DAG](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/images/Capture2.PNG?raw=true)

In this diagram you can see the tree view of the DAG running 

![tree_view](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/images/treeview.PNG?raw=true)

## The final data model. 
___
We wanted to create a schema that would allow our analysts to join the data coming from uber and the restaurant data. and have address information separated in a different table as it might be relevant for detailed analysis but not for the aggregations we wanted to run.
![data_model](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/images/cluster-diagram.jpeg?raw=true)


## Next Steps
___
After this project I think I would like to incorporate new sources of data, like for example actual food traffic, or food delivery pickups and link them to the restaurants and/or the grids to get a better insight of the local restaurant scene and take our food business to success
Hypothetical cases:
* If the data increased 100x: we would take in consideration first that we might incur a big increase in storage and processing costs, might need faster cpus in our redshift cluster and we might also need to process part of the data in a multi-node instance using Spark 
* Pipelines would be run on a daily basis 7 am every day: They technically already do, if we were actually in 2014. I think we would need to implement an extra step at the beginning of our pipeline and automate the retrieval of this uber through their api and straight into our bucket. 
* The databse needed to be accessed by 100+ people: We would definitely increase the size of our clusters, or create separate clusters depending of the need of each department, and probably hire a team of data engineers! 

