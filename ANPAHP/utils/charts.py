"""Module offering methods for generating graphs using matplotlib."""

import matplotlib.pyplot as plt
import numpy as np

import base64
from io import BytesIO

def get_graph():
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
        new_order = sorted([(point, label) for point, label in zip(points, labels)], reverse=False)
        points = [point[0] for point in new_order]
        labels = [point[1] for point in new_order]
    
    plt.switch_backend('AGG')
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
    return get_graph()
