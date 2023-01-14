# Start at corner
# Each go pick random of the corners and go halfway there
import base64
from io import BytesIO
from matplotlib import pyplot
from numpy import random


def get_graph():
    buffer = BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_triangle():
    corners_x = [0, 1, 1/2]
    corners_y = [0, 0, (3**0.5)/2]
    x_coords = corners_x
    y_coords = corners_y
    x = 0
    y = 0

    for i in range(0, 10**4):
        point = random.randint(0, 3)
        x = 0.5 * (x + corners_x[point])
        y = 0.5 * (y + corners_y[point])
        x_coords.append(x)
        y_coords.append(y)

    pyplot.scatter(x_coords, y_coords, s = 0.1, c = 'indigo')
    pyplot.tight_layout()
    chart = get_graph()
    return chart
