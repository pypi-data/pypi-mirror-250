from lightweight_charts import Chart
from lightweight_charts.util import LINE_STYLE
from pandas import DataFrame
from extended_chart.add_overlay import add_overlay
from extended_chart.add_marker import add_marker
from extended_chart.add_trade_marker import add_trade_marker
from extended_chart.add_histogram import add_histogram
from extended_chart.add_background_span import add_background_span
from extended_chart.add_table import add_stats_table, add_pnl_table, add_signal_table
from extended_chart.add_support_lines import add_support_lines
from lightweight_charts.table import Table
from pandas import offsets


# TODO: Need the ability to remove indicators easily ("Sicking for now because not important for strategy discovery)
# TODO: Streamline the style, so that it is applied at top-level and you don't need to keep re-applying it
# TODO: I think I need to abstract this ExtendChart one for level...because this Abstract Chart error is a bit annoying


# This is not extendable, seems like an issue with
class ExtendedChart(Chart):
    def __init__(self, *args, **kwargs):
        super(ExtendedChart, self).__init__(*args, **kwargs)

    def add_overlay(self, data: DataFrame(), color: str = None, width=1, style='solid', alpha=1):
        return add_overlay(self, data=data, color=color, alpha=alpha, style=style, width=width)

    def add_subplot(self, height, sync=True, position='bottom', width=1, *args, **kwargs) -> 'ExtendedChart':
        chart = self.create_subchart(position=position, height=height, width=width, sync=sync, *args,
                                     **kwargs)
        return chart

    def add_support_lines(self, data: DataFrame = None, color='rgba(252, 219, 3, 0.8)',
                          width=1, style='solid', label='', alpha=1):
        return add_support_lines(self, data=data, color=color, width=width, style=style, label=label, alpha=alpha)

    def add_marker(self, data, marker='circle', color='#7858c4', label='', position='below', alpha=1):
        return add_marker(self, data=data, marker=marker, color=color, label=label, position=position, alpha=alpha)

    def add_trade_marker(self, data, label=''):
        return add_trade_marker(self, data=data, label=label)

    def add_histogram(self, data: DataFrame(), label: str | None | list = None, color: str | list[str] | None = None,
                      price_line: bool = False, price_label: bool = False, ):
        return add_histogram(self, data=data, label=label, color=color, price_line=price_line, price_label=price_label)

    def add_background_span(self, data: DataFrame = None, start_time=None, end_time=None, color='rgba(252, 219, 3, 0.1)',
                            **kwargs):
        return add_background_span(self, data=data, start_time=start_time, end_time=end_time, color=color, **kwargs)

    def add_stats_table(self, data: DataFrame(), height=1, width=1) -> Table:
        return add_stats_table(self, data=data, height=height, width=width, position='top', return_clicked_cells=False)

    def add_pnl_table(self, data: DataFrame(), height, width=1, pnl_chunk=100_000_000_000) -> Table:
        return add_pnl_table(self, data=data, height=height, width=width, return_clicked_cells=True, pnl_chunk=pnl_chunk)

    def add_signal_table(self, data: DataFrame(), height, width, chucks=3, default_offset=offsets.Hour(1)):
        return add_signal_table(self, data=data, height=height, width=width, chunks=chucks, default_offset=default_offset)
