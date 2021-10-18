# Creating a New York restaurant traffic dataset 
## for Udacity's data engineering nanodegree capstone project
###  By AlexSkp
___
## Purpose of the project
In this project we will create a small database in order to allow analysts take measures of foot traffic in the city of New York, for the specific purpose of find good locations for opening new branches of our food business. We are targeting a persona that pick up ubers to move around the city.
In order to achieve this, we combined two sources of data: Restaurant data from Yelp's API, and a dataset of uber customer pick-ups. To enrich our dataset and allow for further analysis, we also engineered a new table that divides the city of New York in rectangular areas of aproximately the size of 2x2 blocks, and codified them, in order to combine and connect uber pickups with the location of restaurants. 

## Methodology
### Finding our data
* We first need to retrieve our data. We started by the uber dataset. You can download it  [here](https://www.kaggle.com/fivethirtyeight/uber-pickups-in-new-york-city?search=uber&select=uber-raw-data-aug14.csv)
* To create the union we will create a virual grid that spans from 40,85N to 40,7N and from -74,02 to -74,73
in splits of aprox the size of 4 blocks (2x2) in lattitude/longitude: 0,0012 lat & 0,0042 lon
We will use the south end and the east end as axis so we will do lat-40,7 and then divided 0,0012, rounded to the next .1 and will generate some more rounded "coordinates" to link our data points to common grids.  
 1 example block 40.785885-40,784711 aprox 0,0012° height -73.957148-73,952920 aprox 0,0042 width 
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




https://www.kaggle.com/fivethirtyeight/uber-pickups-in-new-york-city?search=uber&select=uber-raw-data-aug14.csv