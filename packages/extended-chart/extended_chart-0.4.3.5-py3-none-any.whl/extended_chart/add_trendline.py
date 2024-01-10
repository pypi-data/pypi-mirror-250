import pandas as pd
from lightweight_charts import Chart
from extended_chart.utils.color_converter import hex_to_rgba


def add_trendline(chart: Chart, data: pd.DataFrame(), color='#76b5c5', width=1, style='solid', alpha=1):
    '''
    Dataframe with the following properties
                entry_time | end_time | entry_price | end_price | style | color | width | alpha
    Index

    Draw trendlines between two points

    :param data dataframe of above points
    :param color rgba(252, 219, 3, 0.8) or hex-color #76b5c5
    :param width 1
    :param style solid ['solid', 'dotted', 'dashed', 'large_dashed', 'sparse_dotted']
    :param alpha 1 (optional helps set hex color transparency)
    '''

    if data.empty:
        return

    assert set(['start_time', 'end_time', 'start_price', 'end_price']).issubset(
        data.columns), 'To draw trendlines [start_time, end_time, start_price, end_price] columns are required'

    data = data.sort_values('start_time', ascending=True, ignore_index=True)

    if 'width' not in data.columns:
        data['width'] = width
    if 'alpha' not in data.columns:
        data['alpha'] = alpha
    if 'color' not in data.columns:
        data['color'] = color
    if 'style' not in data.columns:
        data['style'] = style

    data = data[['start_time', 'start_price', 'end_time', 'end_price', 'width', 'color', 'style', 'alpha']]
    data['alpha'] = data['alpha'].fillna(alpha)
    data['color'] = data['color'].fillna(color)
    data['style'] = data['style'].fillna(style)
    data['width'] = data['width'].fillna(width)
    data['color'] = data.apply(lambda x: hex_to_rgba(x['color'], x['alpha']), axis=1)

    lines = []
    for x in data.itertuples():
        l = chart.trend_line(start_time=x.start_time, start_value=x.start_price, end_time=x.end_time, end_value=x.end_price,
                             color=x.color, style=x.style, width=x.width, round=True)
        lines.append(l)

    return lines
