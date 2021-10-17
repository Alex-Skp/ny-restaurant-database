"""
This script will run to create a coordinates table with the grid placed in new york, and
will save it in data/ret_grid as a csv file 
"""

import pandas as pd
from functions import generate_grid_dataframe

data = generate_grid_dataframe(40.7, 40.85, -74.73, -74.02, 0.0012, 0.0042, 0.0001)
data.to_csv('./data/quadrant_table.csv', index=False)
