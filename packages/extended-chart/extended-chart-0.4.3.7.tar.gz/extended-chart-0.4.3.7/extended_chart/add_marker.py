import numpy as np
import pandas as pd
from lightweight_charts import Chart
from lightweight_charts.util import MARKER_SHAPE, MARKER_POSITION
from datetime import datetime
from extended_chart.utils.color_converter import hex_to_rgba


# TODO: I need to revisit if this whole nested if/else case is necessary
#   I think I want to keep it simple and only allow for dataframe
#   This will break my test suite so I will revist when I get some time


def add_marker(chart: Chart, data: list[datetime], marker: MARKER_SHAPE = 'circle', color='#7858c4', label='',
               position: list[MARKER_POSITION] = 'below', alpha=1):
    '''
    Dataframe with the following properties
                marker | color | position | label
    datetime

    Adds a Markers on the Chart
    :param data dataframe of markers or list of datetime
    :param color rgba(252, 219, 3, 0.8)  or hex-color  #7858c4
    :param marker circle ['arrow_up', 'arrow_down', 'circle', 'square']
    :param position below ['below','above','inside']
    :param label ""
    :param alpha 1 (optional helps set hex color transparency)
    '''

    if isinstance(data, pd.DataFrame):
        if data.empty:
            return
        if 'position' not in data.columns:
            data['position'] = position
        if 'color' not in data.columns:
            data['color'] = color
        if 'label' not in data.columns:
            data['label'] = label
        if 'marker' not in data.columns:
            data['marker'] = marker
        if 'alpha' not in data.columns:
            data['alpha'] = alpha

        data['alpha'] = data['alpha'].fillna(alpha)
        data['color'] = data['color'].fillna(color)
        data['color'] = data.apply(lambda x: hex_to_rgba(x['color'], x['alpha']), axis=1)

        data = data[['position', 'marker', 'color', 'label']]
        data = data.fillna('')

        marker_objects = []
        for m in data.itertuples():
            marker = chart.marker(time=m.Index, position=m.position, shape=m.marker, color=m.color, text=m.label)
            marker_objects.append(marker)

        return marker_objects


    if isinstance(data, datetime):
        data = [data]
    if isinstance(data, np.ndarray):
        data = [x.astype(datetime) for x in data]
    if isinstance(position, str):
        default_position = position
        position = [position]
    if isinstance(label, str):
        label = [label for _ in data]
    if isinstance(color, str):
        color = [hex_to_rgba(color, alpha=alpha) for _ in data]

    label = [label[i] if i < len(label) else '' for i, _ in enumerate(data)]
    color = [color[i] if i < len(color) else '' for i, _ in enumerate(data)]
    position = [position[i] if i < len(position) else default_position for i, _ in enumerate(data)]

    data = sorted(data)

    marker_objects = []
    for i, m in enumerate(data, 0):
        chart.marker(time=m, position=position[i], shape=marker, color=color[i], text=label[i])
        marker_objects.append(marker)

    return marker_objects
