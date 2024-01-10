import pandas as pd
import warnings, logging
from extended_chart.utils.color_converter import color_wheel, hex_to_rgba

warnings.simplefilter('ignore')

def add_overlay(chart, data: pd.DataFrame(), width=1, style='solid', alpha=1, color=None):
    if not isinstance(data, pd.DataFrame | pd.Series):
        return []

    try:
        data = data.to_frame()
    except AttributeError:
        ...

    indicators = [item for item in data.columns if
                  '_color' not in item and '_width' not in item and '_style' not in item and '_alpha' not in item]
    indicators = [item for item in indicators if not item.strip().startswith('_') and not item.strip().endswith('_')]
    indicator_colors = color_wheel(indicators)

    overlay_objects = []
    for i, line in enumerate(indicators, 0):
        _df = data[[x for x in data.columns if line in x]]
        if f'{line}_color' not in _df.columns:
            _df[f'{line}_color'] = indicator_colors[i] if not color else color
        if f'{line}_width' not in _df.columns:
            _df[f'{line}_width'] = width
        if f'{line}_style' not in _df.columns:
            _df[f'{line}_style'] = style
        if f'{line}_alpha' not in _df.columns:
            _df[f'{line}_alpha'] = alpha

        _df[f'{line}_style'] = _df[f'{line}_style'].fillna(style)
        _df[f'{line}_alpha'] = _df[f'{line}_alpha'].fillna(alpha)
        _df[f'{line}_width'] = _df[f'{line}_width'].fillna(width)
        _df[f'{line}_color'] = _df.apply(lambda x: hex_to_rgba(x[f'{line}_color'], x[f'{line}_alpha']), axis=1)

        _df = _df.rename(columns={
            f'{line}_color': 'color',
            f'{line}_width': 'width',
            f'{line}_style': 'style',
        })

        _data = _df[[line, 'color']]
        _df = _df[['width', 'style']]
        _df = _df.drop_duplicates(keep='first').head(1)

        for x in _df.itertuples():
            overlay = chart.create_line(name=line, style=x.style, width=x.width, price_line=False, price_label=False)
            overlay_objects.append(overlay)
            overlay.set(_data)

    return overlay_objects
