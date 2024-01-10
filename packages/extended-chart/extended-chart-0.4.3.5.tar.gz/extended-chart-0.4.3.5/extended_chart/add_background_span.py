import pandas as pd
from lightweight_charts.abstract import Line, AbstractChart
from extended_chart.utils.color_converter import hex_to_rgba

# There is an issue when the start_time and end_time falls between a bar chart
#  in these cases, the vertical span is not rendered
#  https://github.com/louisnw01/lightweight-charts-python/issues/234



def add_background_span(chart: AbstractChart | Line, data: pd.DataFrame() = None, start_time=None, end_time=None,
                        color='rgba(252, 219, 3, 0.2)', alpha=0.2):
    if isinstance(data, pd.DataFrame):
        assert {'start_time', 'end_time'}.issubset(set(data.columns)), "start_time, end_time needed to color background ranges"

        if data.empty:
            return
        if 'alpha' not in data.columns:
            data['alpha'] = alpha
        if 'color' not in data.columns:
            data['color'] = color


        data['color'] = data.apply(lambda x: hex_to_rgba(x['color'], x['alpha']), axis=1)
        data = data.sort_values('start_time',ignore_index=True)

        spans_objects = []
        for t in data.itertuples():
            span = chart.vertical_span(start_time=t.start_time, end_time=t.end_time, color=t.color)
            spans_objects.append(span)

        return spans_objects

    else:
        assert all([start_time, end_time, color]), "missing required fields: start_time, end_time, color"
        color = hex_to_rgba(color, alpha=alpha)
        spans = chart.vertical_span(start_time=start_time, end_time=end_time, color=color)
        return [spans]