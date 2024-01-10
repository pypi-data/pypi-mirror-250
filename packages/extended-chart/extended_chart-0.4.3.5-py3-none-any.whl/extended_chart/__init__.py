from extended_chart.ExtendedChart import ExtendedChart

from extended_chart.style import black_background, white_background

from extended_chart.add_trade_marker import add_trade_marker, trade_colors
from extended_chart.add_overlay import add_overlay
from extended_chart.add_marker import add_marker
from extended_chart.add_histogram import add_histogram
from extended_chart.add_trendline import add_trendline
from extended_chart.add_background_span import add_background_span
from extended_chart.add_support_lines import add_support_lines

# TODO: I need to address the symbol lookup being a parameter, I wonder if I should source this from the metadata.json file
#   The problem stems from needing start and end time for RTH and ETH

# TODO: I need to make sure that market_data always contains trading symbol in extended_algo

# TODO: Add support for histogram with multicolor and 0 center scaling issue

# TODO: There is an issue with main_chart note being able to redraw background_span on timeframe change

# TODO: Check with lightweight_chart on why main plot legend is not dropping


from extended_chart.RenderStrategyChart import RenderStrategyChart
