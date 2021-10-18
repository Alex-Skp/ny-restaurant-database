# Creating a New York restaurant traffic dataset 
## for Udacity's data engineering nanodegree capstone project
###  By AlexSkp
___
## Purpose of the project
In this project we will create a small database in order to allow analysts take measures of foot traffic in the city of New York, for the specific purpose of find good locations for opening new branches of our food business. We are targeting a persona that pick up ubers to move around the city.
In order to achieve this, we combined two sources of data: Restaurant data from Yelp's API, and a dataset of uber customer pick-ups. To enrich our dataset and allow for further analysis, we also engineered a new table that divides the city of New York in rectangular areas of aproximately the size of 2x2 blocks, and codified them, in order to combine and connect uber pickups with the location of restaurants. 

## Methodology
### Finding our data
* We first need to retrieve our data. We started by the uber dataset. You can download it  [here](https://www.kaggle.com/fivethirtyeight/uber-pickups-in-new-york-city?search=uber&select=uber-raw-data-aug14.csv).
We focused only in the csvs of 2014. Data spans from april to September. We wanted data that follows a continuous timeline to simulate how our ETL process would feed from data retrieved in previous steps. After downloading, we followed the steps described in [split_data.ipynb](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/split_data.ipynb)
* To make the grid table we created a table with grids that cover all our uber traffic data. Some of the restaurants happened to be in the peripheric areas of the city but we won't be interested in analyzing those. We defined a function in [functions.py](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/functions.py) to loop and calculate the grids, as well as generating an quadrant ID for each one. running [generate_coord_grid.py](https://github.com/Alex-Skp/udacity-capstone-project/blob/main/generate_coord_grid.py) would create this grid table and save it as a csv locally.
* For the NY restaurants 
* Describe the steps of the process for the project
* Describe the tools, technology and data model
	* Explain the schemas here 
### Data Model 
* ETL processes result
* Data dictionary 
* Data model is appropiate
### Next Steps
Hypothetical cases:
* Data is increased 100x
* Pipelines would be run on a daily basis 7 am every day 
* The databse needed to be accessed by 100+ people


Other: 
* PEP8, No errors 
* Two data quality checks 
* 2 Data Sources 
* 1M lines of data 
* Two types of sources 



## Cluster database diagram
!['cluster-diagram'](cluster-diagram.jpeg)


