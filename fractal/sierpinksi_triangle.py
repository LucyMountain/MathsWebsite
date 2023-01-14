# Start at corner
# Each go pick random of the corners and go halfway there

import matplotlib.pyplot as plt
from numpy import random

corners_x = [0, 1, 1/2]
corners_y = [0, 0, (3**0.5)/2]
x_coords = corners_x
y_coords = corners_y
x = 0
y = 0

for i in range(0, 10**6):
    point = random.randint(0, 3)
    x = 0.5 * (x + corners_x[point])
    y = 0.5 * (y + corners_y[point])
    x_coords.append(x)
    y_coords.append(y)

plt.scatter(x_coords, y_coords, s = 0.1, c = 'indigo')
plt.show()