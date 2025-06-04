"""Module offering methods for generating graphs using matplotlib."""

import matplotlib.pyplot as plt
import numpy as np

import base64
from io import BytesIO


# -----------------------------------------------------------------------------
# Private utilities:


def __get_graph():
    """Gets the current graph from matplotlib as a str usable in HTML using:
    `<img src="data:image/png;base64, {{graph|safe}}">.`
    """
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


# -----------------------------------------------------------------------------
# Chart functions:


def make_radar_chart(points, labels, title, backend="AGG", figsize=5, reorder=True):
    """Creates a radar chart of the provided points.
    
    Args:
        points (list[float]): The points to plot.
        labels (list[str]): The labels associated to points.
        title (str): The title of your graph (e.g. 'Financial Perspective').
        backend (str): The backend to use (default to "AGG"), for more information on this,
            refer to: https://matplotlib.org/stable/users/explain/figure/backends.html#the-builtin-backends
        figsize (float): The size of the figure in inches. The figure will be a square.
        reorder (bool): Used to reorder the values so larger values are set together in nice manner
            to make the graph look better. (Defaults to `True`)
        
    Returns:
        str - A string ready to be used in HTML using `<img src="data:image/png;base64, {{chart|safe}}">`.
    """
    if reorder:
        new_order = sorted([(point, label) for point, label in zip(points, labels)])
        points = [point[0] for point in new_order]
        labels = [point[1] for point in new_order]
    
    plt.switch_backend(backend)
    fig = plt.figure(figsize = (figsize*1.2, figsize))
    
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, points, 'o-', linewidth=2)
    ax.fill(angles, points, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, labels)
    
    y_ticks = [round(i/6 * max(points), 2) for i in range(6)]
    plt.yticks(y_ticks)
    ax.tick_params(labelsize = 8)
    
    ax.set_title(title)
    ax.grid(True)
    return __get_graph()


def make_pie_chart(points, labels, title, backend="AGG", figsize=5, 
                   compress_small_ones=True, threshold=0.01,
                   rounding_error=0.01, percentage_decimals=2):
    """Creates a pie chart of the provided points.
    
    Args:
        points (list[float]): The points to plot (either as percentages, or as proportions summing to 1).
        labels (list[str]): The labels associated to points.
        title (str): The title of your graph (e.g. 'Financial Perspective').
        backend (str): The backend to use (default to "AGG"), for more information on this,
            refer to: https://matplotlib.org/stable/users/explain/figure/backends.html#the-builtin-backends
        figsize (float): The size of the figure in inches. The figure will be a rectangle (1.5 figsize * figsize).
        compress_small_ones (bool): If set to `True`, will compress all the values lower than
            `threshold` into a single "Others" category. (Defaults to `True`)
        threshold (float): The threshold used for value compression into a single "Others" category.
            (Defaults to 0.01)
        rounding_error (float): The possible rounding error for the sum of the values. If you pass
            percentages, you should set it to 1. (Defaults to 0.01)
        percentage_decimals (int): The number of decimals to keep in the percentages. (Defaults to 2)
        
    Returns:
        str - A string ready to be used in HTML using `<img src="data:image/png;base64, {{chart|safe}}">`.
    """
    # Reorder the values (required for a pie chart to be readable):
    new_order = sorted([(point, label) for point, label in zip(points, labels)])
    points = [point[0] for point in new_order]
    labels = [point[1] for point in new_order]
    
    # Get rid of 0s since they are not relevant in a pie chart:
    nb_0s = len([x for x in points if x == 0])
    points = points[nb_0s:]
    labels = labels[nb_0s:]
    
    # Compress values if required:
    if compress_small_ones:
        nb_compressed = 0
        compressed_value = 0
        for value in points:
            if value < threshold:
                nb_compressed += 1
                compressed_value += value
        if nb_compressed:
            points = [compressed_value] + points[nb_compressed:]
            labels = ["Others"] + labels[nb_compressed:]
        
    # Make sure we have percentages:
    total = sum(points)
    if 1 - rounding_error <= total <= 1 + rounding_error:
        points = [x * 100 for x in points]
        
    # Create the pie chart:
    plt.switch_backend(backend)
    fig = plt.figure(figsize = (figsize*1.5, figsize))
    ax = fig.add_subplot()
    ax.pie(points, labels=labels, autopct=f'%1.{percentage_decimals}f%%')
    ax.set_title(title)
    return __get_graph()
    
    