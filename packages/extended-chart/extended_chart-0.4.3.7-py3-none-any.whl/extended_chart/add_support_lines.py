import logging, time, os
import pandas as pd
from lightweight_charts.abstract import Line
from extended_chart.utils.color_converter import hex_to_rgba

pd.set_option('display.width', 1000, 'display.max_columns', 1000)


# TODO: I need to check if this works on chart or line
#  if this needs to be one a line, this actually complicates things for the chart render
#  I would need to create to apply it on a arbitrary line

# TODO: I also found this API very cumbersome to use for quick renders, need to make it more streamline
#  I wonder for all my APIs if I need to go one more level of abstraction


def add_support_lines(line: Line, data: pd.DataFrame() = None, color='rgba(252, 219, 3, 0.8)',
                        width=1, style='solid', label='', alpha=1):
    '''
    Dataframe with the following properties
                price | color | width | style | label
    datetime

    Horizontal Support Lines, make sure for subcharts that the supports are applied to Line Object

    :param data dataframe of prices; or single price value
    :param color rgba(252, 219, 3, 0.8) or hex-color  #7858c4
    :param width 1
    :param style solid ['solid', 'dotted', 'dashed', 'large_dashed', 'sparse_dotted']
    :param label ""
    :param alpha 1 (optional helps set hex color transparency)
    '''
    if isinstance(data, pd.DataFrame):
        if data.empty:
            return
        assert 'price' in data.columns, 'price= values needs to be provided in the dataframe to draw horizontal lines'
        if 'width' not in data.columns:
            data['width'] = width
        if 'alpha' not in data.columns:
            data['alpha'] = alpha
        if 'color' not in data.columns:
            data['color'] = color
        if 'style' not in data.columns:
            data['style'] = 'solid'
        if 'label' not in data.columns:
            data['label'] = label

        data = data[['price', 'width', 'color', 'style', 'label', 'alpha']]
        data['alpha'] = data['alpha'].fillna(alpha)
        data['color'] = data['color'].fillna(color)
        data['style'] = data['style'].fillna(style)
        data['width'] = data['width'].fillna(width)
        data['color'] = data.apply(lambda x: hex_to_rgba(x['color'], x['alpha']), axis=1)
        data['label'] = data['label'].fillna('')

        support_lines_objects = []
        for x in data.itertuples():
            support = line.horizontal_line(price=x.price, color=x.color, width=x.width, style=x.style, text=x.label)
            support_lines_objects.append(support)

        return support_lines_objects

    elif isinstance(data, (float, int)):
        support = line.horizontal_line(price=data, color=hex_to_rgba(color, alpha=alpha), width=width, style=style, text=label)
        return [support]
