import time
from base64 import b64encode
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from plotter.database.dbo import PointDBO


# Use non interactive backend
matplotlib.use('agg')


def create_plot_from_points(points: list[PointDBO]) -> str:
    x_dots = np.fromiter(map(lambda point: point.x_value, points), dtype=np.int32)
    y_dots = np.fromiter(map(lambda point: point.y_value, points), dtype=np.int32)

    fig, ax = plt.subplots()

    ax.plot(x_dots, y_dots, 'o-')
    ax.set_ylabel("Y Axis")
    ax.set_xlabel("X Axis")

    buffer = BytesIO()
    fig.savefig(buffer, format="png")

    return f'data:image/png;base64,{b64encode(buffer.getvalue()).decode("ascii")}'
