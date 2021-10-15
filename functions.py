import pandas as pd
import os

def generate_grid_dataframe(from_x, to_x, from_y, to_y, inc_x, inc_y, precision):

    data = pd.DataFrame(columns=['id','x_from','x_to','y_from','y_to'])

    id = []
    x_from = []
    x_to = []
    y_from = []
    y_to = []

    x,y = x_from,y_from
    a,b = 0,0
    while x < x_to:
        a += 1
        b = 0
        while y < y_to:
            b += 1
            x_from.append(x)
            y_from.append(y)
            x_to.append(x + inc_x - precision)
            y_to.append(y + inc_y - precision)
            y += inc_y
            id.append('A'+ str(a) +'B'+ str(b))
        y = y_from  
        x += inc_x

    data['id'] = id
    data['x_from'] = x_from
    data['x_to'] = x_to
    data['y_from'] = y_from
    data['y_to'] = y_to

    return data
    
    