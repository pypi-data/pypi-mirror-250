import pandas as pd
from pathlib import Path
import time, logging
from extended_chart import ExtendedChart, black_background, add_overlay, add_marker, add_trade_marker, add_trendline, \
    add_support_lines, add_background_span, add_histogram
from extended_chart.utils.rename_columns import rename_iqfeed_cols, resample_ohlc_dict
from extended_chart.add_table import add_stats_table, add_pnl_table, add_signal_table, empty_pnl_col, empty_stats_cols
from itertools import chain, product

MAIN_CHART_HEIGHT = 0.40
SUBCHART_HEIGHT = 0.30
PNL_HEIGHT = 0.3

logger = logging.getLogger(__name__)


class RenderStrategyChart:

    def __init__(
            self, strategy_dir: (Path | str), main_indicators=[],
            main_supports=pd.DataFrame(columns=['price', 'color', 'label', 'width', 'style', 'alpha']),
            main_trendlines=pd.DataFrame(
                columns=['start_time', 'end_time', 'start_price', 'end_price', 'color', 'width', 'style', 'alpha']),
            main_spans=pd.DataFrame(columns=['start_time', 'end_time', 'color', 'alpha']),
            main_markers=pd.DataFrame(columns=['marker', 'color', 'position', 'label', 'alpha']),
            chart_one_indicators=[],
            chart_two_indicators=[],
            chart_three_indicators=[],
            chart_four_indicators=[],
            toolbar_freq=['1Min', '5Min', '30Min', '1H'],
            pnl_chunk=20,
            signal_data=pd.DataFrame(columns=['start_time', 'end_time']),
            **kwargs):
        '''
                There are two types of charts exposed by lightweights_chart: main_charts and subcharts.
                   - main_chart: the indicators, background_span, trendlines, markers can be drawn directly against the chart
                   - subcharts: these drawing objects must be drawn against an indicator-line or indicator-histogram for it to
                   register. Currently only four subchart rendering is supported due to limited screen real estate
                Style Reference:
                    - style ['solid', 'dotted', 'dashed', 'large_dashed', 'sparse_dotted']
                    - marker ['arrow_up', 'arrow_down', 'circle', 'square']
                    - position ['below', 'above', 'inside']
                Drawing Reference:
                    - x_indicators: adds indicators
                    - x_supports: adds support and resistance lines
                    - x_markers: adds markers
                    - x_trendlines: adds trendlines
                    - x_spans: adds background span
                Features Reference:
                    - Indicators can be suffixed with the following style properties ['_color','_style', 'width', 'alpha']
                    - You can also include additional features; use get_features_data() and set_features() to update
                    - You cannot override or drop original columns
                :param strategy_dir: Path to strategy that contains the strategy metadata
                :param main_indicators: List of feature columns defined in the features_data
                :param main_markers: columns=[marker(o), color(o), position(o)] index=datetime
                :param main_spans: columns=[start_time, end_time, color(o), alpha(o)] index=Any
                :param main_trendlines: [start_time, end_time, start_price, end_price, color(o), width(o), style(o), alpha(o)] index=Any
                :param signal_data: [start_time, end_time(o)]
                :param toolbar_freq: Indicators are re-drawn using their last values with chart frequency is changed
                :param pnl_chunk: Paginate the pnl table
                :param symbol_lookup: (deprecate) lookup table that defines a symbols rth_start and rth_end time
                :param show_ohlc: show ohlc-v on main chart
                :param kwargs: [disable_pnl, disable_stats, show_volume, symbol_lookup={}]
                '''

        self.strategy_dir = Path(strategy_dir) if isinstance(strategy_dir, str) else strategy_dir
        self.show_volume = kwargs.get('show_volume', False)
        self.symbol_lookup = kwargs.get('symbol_lookup', {})
        self.toolbar_freq = toolbar_freq

        self.main_overlays = main_indicators
        self.main_supports = main_supports
        self.main_markers = main_markers
        self.main_trendlines = main_trendlines
        self.main_spans = main_spans
        self.show_ohlcv = kwargs.pop("show_ohlc", False)
        self.kwargs = kwargs

        self.match_marketdata_and_featuredata_index = []
        self.pnl_chunk = pnl_chunk
        self.signal_data = signal_data

        self.subchart_names = ['chart_one', 'chart_two', 'chart_three', 'chart_four']
        self.chart_one_indicators = chart_one_indicators
        self.chart_two_indicators = chart_two_indicators
        self.chart_three_indicators = chart_three_indicators
        self.chart_four_indicators = chart_four_indicators

        self._initialize_dataset()
        self._initialize_gui(width=kwargs.pop("width", 1280), height=kwargs.pop("height", 1300),
                             debug=kwargs.pop("debug", False))

    def get_features_data(self):
        logger.info(f'Defined Features Data:\n{self.features_data}')
        return self.features_data

    def set_features_data(self, other: pd.DataFrame()):
        self.features_data = pd.concat([self.features_data, other.drop(self.features_data.columns, axis=1)], axis=1)

    def show(self):
        self._initialize_charts()
        self._refresh_plots_and_indicators()
        self._initialize_button_events()

        self.chart.show(block=True)

    def _initialize_gui(self, width, height, debug):

        self.chart = ExtendedChart(title=str(self.strategy_dir), inner_width=self.resize_width_dict['min']['main_width'],
                                   inner_height=self.resize_width_dict['min']['main_height'],
                                   width=width, height=height, debug=debug)
        self.chart = black_background(self.chart, legend=False, show_ohlc=self.show_ohlcv)

        self.marker_lines, self.marker_arrows = ([], [])
        self.indicator_type_postfix = ['supports', 'trendlines', 'markers', 'spans']

    def _initialize_dataset(self):
        self.subchart_count = sum([1 if len(x) > 0 else 0 for x in
                                   [self.chart_one_indicators, self.chart_two_indicators, self.chart_three_indicators,
                                    self.chart_four_indicators]])

        self.resize_width_dict = dict(max=dict(), min=dict())

        max_specs = self.resize_width_dict['max']
        max_specs['main_width'] = 1
        max_specs['subchart_width'] = 1
        max_specs['pnl_width'] = 0
        max_specs['stats_width'] = 0
        max_specs['signal_width'] = 0
        max_specs['pnl_height'] = 0
        max_specs['stats_height'] = 0
        max_specs['signal_height'] = 0

        max_specs['main_height'] = round(MAIN_CHART_HEIGHT / (SUBCHART_HEIGHT + MAIN_CHART_HEIGHT), 2)
        max_specs['subchart_height'] = round((
                SUBCHART_HEIGHT / (SUBCHART_HEIGHT + MAIN_CHART_HEIGHT) / max(1, self.subchart_count)), 2)

        if self.subchart_count == 0:
            max_specs['subchart_height'] = 0
            max_specs['main_height'] = 1

        min_specs = self.resize_width_dict['min']
        min_specs['main_width'] = max_specs['main_width']
        min_specs['main_height'] = MAIN_CHART_HEIGHT
        min_specs['subchart_height'] = SUBCHART_HEIGHT
        min_specs['subchart_width'] = max_specs['subchart_width']
        min_specs['pnl_width'] = 1
        min_specs['stats_width'] = 0.3
        min_specs['signal_width'] = 0.1
        min_specs['pnl_height'] = PNL_HEIGHT
        min_specs['stats_height'] = SUBCHART_HEIGHT + MAIN_CHART_HEIGHT
        min_specs['signal_height'] = SUBCHART_HEIGHT + MAIN_CHART_HEIGHT

        self.freq = self.toolbar_freq[0]
        self.show_markers = 'show_trades'
        self.rth = 'ETH'

        self.features_data = pd.read_pickle(self.strategy_dir / 'features_data.p').set_index('datetime')
        self.market_data = pd.read_pickle(self.strategy_dir / 'market_data.p')
        self.market_data = self.market_data.rename(columns=rename_iqfeed_cols)['open high low close volume'.split()]
        self.market_data.drop('volume', axis=1, errors='ignore', inplace=True) if not self.show_volume else None
        self._set_market_data()

        try:
            self.pnl_data = pd.read_pickle(self.strategy_dir / 'pnl_data.p')
            if self.kwargs.pop('disable_pnl', False):
                raise FileNotFoundError
            min_specs['subchart_height'] = round(min_specs['subchart_height'] / max(1, self.subchart_count), 2)
        except FileNotFoundError:
            self.pnl_data = pd.DataFrame(columns=empty_stats_cols)
            min_specs['main_height'] = round((MAIN_CHART_HEIGHT + PNL_HEIGHT / 2), 2)
            min_specs['subchart_height'] = round((SUBCHART_HEIGHT + PNL_HEIGHT / 2) / max(1, self.subchart_count), 2)

        if not self.subchart_count:
            min_specs['main_height'] = min_specs['main_height'] + min_specs['subchart_height']
            min_specs['subchart_height'] = 0

        try:
            self.stats_data = pd.read_pickle(self.strategy_dir / 'stats_data.p')
            if self.kwargs.pop('disable_stats', False):
                raise FileNotFoundError
            min_specs['main_width'] = min_specs['main_width'] - min_specs['stats_width']
            min_specs['subchart_width'] = min_specs['subchart_width'] - min_specs['stats_width']
        except FileNotFoundError:
            self.stats_data = pd.DataFrame(columns=empty_pnl_col)
            min_specs['stats_width'] = 0
            min_specs['stats_height'] = 0

        if self.signal_data.empty:
            min_specs['signal_width'] = 0
            min_specs['signal_height'] = 0
        else:
            min_specs['main_width'] = min_specs['main_width'] - min_specs['signal_width']
            min_specs['subchart_width'] = min_specs['subchart_width'] - min_specs['signal_width']

        try:
            self.symbol = self.market_data.symbol.min()
        except:
            self.symbol = self.pnl_data.symbol.min()

    def _initialize_button_events(self):
        self.chart.topbar.menu('switcher_freq', options=self.toolbar_freq, align='left',
                               func=lambda chart: self._change_timeframe(chart, 'switcher_freq'))
        self.chart.topbar.menu('switcher_rth', options=('ETH', 'RTH'), align='left',
                               func=lambda chart: self._change_rth(chart=chart, switcher_name='switcher_rth'))
        self.chart.topbar.menu('menu_trade_markers', options=('Trade Lines', 'Trade Markers', 'No Markers'), align='left',
                               func=lambda chart: self._show_trade_markers(chart=chart, switcher_name='menu_trade_markers'))
        self.chart.topbar.button('button_fullscreen', '🗖 Fullscreen', align='right',
                                 func=lambda chart: self._change_fullscreen(chart, 'button_fullscreen'))

        self._show_trade_markers(self.chart, 'menu_trade_markers')
        # self.chart.topbar.button('delete_overlays', '❌', align='left', func=self._delete_overlays_all)
        # self._change_fullscreen(self.chart, 'button_fullscreen')

    def _initialize_charts(self):
        time.sleep(0.1)
        small = self.resize_width_dict['min']
        self.stats_table = add_stats_table(self.chart, data=self.stats_data, width=small['stats_width'],
                                           height=small['stats_height'])
        self.signal_table = add_signal_table(self.chart, data=self.signal_data, width=small['signal_width'],
                                             height=small['signal_height'], chunks=3)

        self.chart_one = black_background(self.chart.add_subplot(height=0, width=small['subchart_width']))
        self.chart_two = black_background(self.chart.add_subplot(height=0, width=small['subchart_width']))
        self.chart_three = black_background(self.chart.add_subplot(height=0, width=small['subchart_width']))
        self.chart_four = black_background(self.chart.add_subplot(height=0, width=small['subchart_width']))

        if self.chart_one_indicators:
            self.chart_one = black_background(
                self.chart.add_subplot(height=small['subchart_height'], width=small['subchart_width']))
        if self.chart_two_indicators:
            self.chart_two = black_background(
                self.chart.add_subplot(height=small['subchart_height'], width=small['subchart_width']))
        if self.chart_three_indicators:
            self.chart_three = black_background(
                self.chart.add_subplot(height=small['subchart_height'], width=small['subchart_width']))
        if self.chart_four_indicators:
            self.chart_four = black_background(
                self.chart.add_subplot(height=small['subchart_height'], width=small['subchart_width']))

        self.pnl_table = add_pnl_table(self.chart, data=self.pnl_data, width=1, height=small['pnl_height'],
                                       pnl_chunk=self.pnl_chunk)

        for subchart in self.subchart_names:
            for overlay in self.indicator_type_postfix:
                data = self.kwargs.pop(f'{subchart}_{overlay}', None)
                setattr(self, f'{subchart}_{overlay}', data)

    def _refresh_plots_and_indicators(self):
        self.chart.set(self._set_market_data())

        cols = self.main_overlays
        cols = set(map("".join, chain((product(cols, ['_color', '_width', '_style', '_alpha'])), cols)))
        cols = list(cols.intersection(set(self.features_data.columns)))
        main_indicators = add_overlay(self.chart, self._set_features_data(columns=cols))
        setattr(self, 'main_indicator_overlay_lines', main_indicators)

        for subchart in self.subchart_names:
            chart_obj = getattr(self, subchart)
            cols = getattr(self, f'{subchart}_indicators')
            cols = set(map("".join, chain((product(cols, ['_color', '_width', '_style', '_alpha'])), cols)))
            cols = list(cols.intersection(set(self.features_data.columns)))
            data = self._set_features_data(columns=cols)
            object_line = add_overlay(chart_obj, data)
            setattr(self, f'{subchart}_indicator_overlay_lines', object_line)

        setattr(self, 'main_overlays_supports', add_support_lines(self.chart, data=self.main_supports))
        setattr(self, 'main_overlays_spans', add_background_span(self.chart, data=self.main_spans))
        setattr(self, 'main_overlays_trendlines', add_trendline(self.chart, data=self.main_trendlines))
        setattr(self, 'main_overlays_markers', add_marker(self.chart, data=self.main_markers))

        for subchart in self.subchart_names:
            line_obj = getattr(self, f'{subchart}_indicator_overlay_lines')
            chart_obj = getattr(self, subchart)

            try:
                data = getattr(self, f'{subchart}_supports')
                setattr(self, f'{subchart}_overlays_supports', add_support_lines(line_obj[0], data))
            except:
                setattr(self, f'{subchart}_overlays_supports', pd.DataFrame())
            try:
                data = getattr(self, f'{subchart}_spans')
                setattr(self, f'{subchart}_overlays_spans', add_background_span(line_obj[0], data))
            except:
                setattr(self, f'{subchart}_overlays_spans', pd.DataFrame())

            # NOTE: Verify if trendlines and markers are supported on subcharts
            data = getattr(self, f'{subchart}_trendlines')
            data = data if isinstance(data, pd.DataFrame) else pd.DataFrame()
            setattr(self, f'{subchart}_overlays_trendlines', add_trendline(chart_obj, data))

            try:
                data = getattr(self, f'{subchart}_markers')
                data = data if isinstance(data, pd.DataFrame) else pd.DataFrame()
                setattr(self, f'{subchart}_overlays_markers', add_marker(line_obj[0], data))
            except:
                setattr(self, f'{subchart}_overlays_markers', pd.DataFrame())

    def _set_market_data(self):
        df = self.market_data.copy()
        resample_ohlc_dict.pop('volume', None) if not self.show_volume else None

        df = df.groupby(pd.Grouper(freq=self.freq)).agg(resample_ohlc_dict)
        df = df.dropna()

        self.match_marketdata_and_featuredata_index = df.index

        if self.rth == 'RTH':
            symbol_detail = self.symbol_lookup.get(self.symbol)
            if symbol_detail:
                rth_start = symbol_detail.rth_start
                rth_end = symbol_detail.rth_end

                if rth_start and rth_end:
                    df = df.between_time(start_time=rth_start, end_time=rth_end, inclusive='both')

        return df

    def _set_features_data(self, columns):
        df = self.features_data.copy()
        df = df[columns]
        df = df.groupby(pd.Grouper(freq=self.freq)).last()
        df = df[df.index.isin(self.match_marketdata_and_featuredata_index)]
        df = df.fillna(method='ffill')

        if self.rth == 'RTH':
            symbol_detail = self.symbol_lookup.get(self.symbol)
            if symbol_detail:
                rth_start = symbol_detail.rth_start
                rth_end = symbol_detail.rth_end

                if rth_start and rth_end:
                    df = df.between_time(start_time=rth_start, end_time=rth_end, inclusive='both')

        return df

    def _change_rth(self, chart, switcher_name):
        if self.chart.topbar[switcher_name].value == 'ETH':
            self.rth = 'ETH'

        elif self.chart.topbar[switcher_name].value == 'RTH':
            self.rth = 'RTH'

        self._delete_overlays_all()
        self._refresh_plots_and_indicators()

    def _change_fullscreen(self, chart: ExtendedChart, button_name):
        small = self.resize_width_dict['min']
        big = self.resize_width_dict['max']

        if chart.topbar[button_name].value == '🗖 Fullscreen':
            chart.topbar[button_name].set('🗕 Minimize')

            self.stats_table.resize(width=big['stats_width'], height=big['stats_height'])
            self.pnl_table.resize(width=big['pnl_width'], height=big['pnl_height'])
            self.signal_table.resize(width=big['signal_width'], height=big['signal_height'])

            chart.resize(height=big['main_height'], width=big['main_width'])

            for chart_name in self.subchart_names:
                if getattr(self, chart_name + '_indicators'):
                    getattr(self, chart_name).resize(height=big['subchart_height'], width=big['subchart_width'])

        elif chart.topbar[button_name].value == '🗕 Minimize':
            chart.topbar[button_name].set('🗖 Fullscreen')

            chart.resize(height=small['main_height'], width=small['main_width'])

            self.stats_table.resize(width=small['stats_width'], height=small['stats_height'])
            self.pnl_table.resize(width=small['pnl_width'], height=small['pnl_height'])
            self.signal_table.resize(width=small['signal_width'], height=small['signal_height'])

            for chart_name in self.subchart_names:
                if getattr(self, chart_name + '_indicators'):
                    getattr(self, chart_name).resize(height=small['subchart_height'], width=small['subchart_width'])

    def _change_timeframe(self, chart, switcher_name):
        self.freq = chart.topbar[switcher_name].value
        self._delete_overlays_all()
        self._refresh_plots_and_indicators()

    def _show_trade_markers(self, chart, switcher_name):
        for trend_line in self.marker_lines:
            trend_line.delete()

        for marker in self.marker_arrows:
            self.chart.remove_marker(marker_id=marker)

        if chart.topbar[switcher_name].value == 'Trade Lines':
            self.show_markers = 'show_trades'
        elif chart.topbar[switcher_name].value == 'Trade Markers':
            self.show_markers = 'show_markers'
        elif chart.topbar[switcher_name].value == 'No Markers':
            self.show_markers = None

        self.marker_lines, self.marker_arrows = add_trade_marker(self.chart, self.pnl_data, marking_style=self.show_markers)

    def _delete_overlays_all(self, chart=None):
        for main_indicators_obj in getattr(self, 'main_indicator_overlay_lines'):
            main_indicators_obj.delete() if main_indicators_obj else None
        try:
            for main_markers_obj in getattr(self, 'main_overlays_markers'):
                self.chart.remove_marker(main_markers_obj) if main_markers_obj else None
        except TypeError:
            ...
        try:
            for main_trendline_obj in getattr(self, 'main_overlays_trendlines'):
                main_trendline_obj.delete() if main_trendline_obj else None
        except TypeError:
            ...
        try:
            for main_span_obj in getattr(self, 'main_overlays_spans'):
                main_span_obj.delete() if main_span_obj else None
        except TypeError:
            ...
        try:
            for main_span_obj in getattr(self, 'main_overlays_supports'):
                main_span_obj.delete() if main_span_obj else None
        except TypeError:
            ...

        for subchart in self.subchart_names:
            for subchart_lines in getattr(self, f'{subchart}_indicator_overlay_lines'):
                subchart_lines.delete() if subchart_lines else None

        for chart in self.subchart_names:
            for obj_type in self.indicator_type_postfix:
                delete_objects = getattr(self, f'{chart}_overlays_{obj_type}')

                if isinstance(delete_objects, pd.DataFrame):
                    continue
                if not delete_objects:
                    continue

                if obj_type == 'markers':
                    for obj in delete_objects:
                        getattr(self, chart).remove_marker(obj) if obj else None
                    continue

                for obj in delete_objects:
                    obj.delete() if obj else None
