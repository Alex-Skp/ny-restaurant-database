import pandas as pd
import os


def generate_grid_dataframe(from_x,
                            to_x,
                            from_y,
                            to_y,
                            inc_x,
                            inc_y,
                            precision):
    """
    This function will generate a grid that would cover the coordinates passed
    as arguments.
    Returns a pandas dataframe.
    -------
    from_x: coordinate to start the grid in the x axis
    to_x: coordinate where to stop generating grid cells in the x axis
    from_y: coordinate to start the grid in the y axis
    to_y: coordinate where to stop generating grid cells, in the y axis
    inc_x: size of the grid cell in the x axis
    inc_y: size of the grid cell in the y axis
    precision: state the precision in which the measures are entered.
               for example, 0,001
    """

    data = pd.DataFrame(columns=['id', 'x_from', 'x_to', 'y_from', 'y_to'])

    id = []
    x_from = []
    x_to = []
    y_from = []
    y_to = []

    x, y = from_x, from_y
    a, b = 0, 0
    while x < to_x:
        a += 1
        b = 0
        while y < to_y:
            b += 1
            x_from.append(x)
            y_from.append(y)
            x_to.append(x + inc_x - precision)
            y_to.append(y + inc_y - precision)
            y += inc_y
            id.append('A' + str(a) + 'B' + str(b))
        y = from_y
        x += inc_x

    data['id'] = id
    data['x_from'] = x_from
    data['x_to'] = x_to
    data['y_from'] = y_from
    data['y_to'] = y_to

    return data
