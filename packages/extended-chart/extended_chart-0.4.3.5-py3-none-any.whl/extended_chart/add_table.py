import pandas as pd
import datetime as dt
from extended_chart import ExtendedChart

# TODO: This needs to be provided from chart.style so that it is consistent
color_style = {'background_style': {'background_color': '#171B26', 'border_color': '#252830', 'header_color': '#171B26'}}


def convert_number_to_excel_column(n):
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result


def row_click_event(e):
    # print(e)
    ...


# TODO: This looks like there is a duplicated function
def row_move_to_chart(row, column, chart: ExtendedChart):
    chart.set_visible_range(start_time=row.get('ENTRY TIME'), end_time=row.get('EXIT TIME'))


def row_move_to_chart_sig(row, column, chart: ExtendedChart, df):
    try:
        record = df.loc[row.get(column)]
        chart.set_visible_range(start_time=record['start_time'], end_time=record['end_time'])
    except:
        ...


# TODO: END OF DUPLICATE CODE

def _formate_value(x):
    if isinstance(x, dt.timedelta):
        x = x.components
        hours = x.days * 24 + x.hours
        minutes = x.minutes
        seconds = x.seconds

        return f'{hours}:{minutes}:{seconds}'

    return x


empty_pnl_col = [
    'net_profit', 'gross_profit', 'gross_loss', 'total_commission', 'max_drawdown', 'number_of_winning_trades',
    'number_of_losing_trades', 'total_trade_count', 'largest_winning_trade', 'largest_losing_trade', 'average_winning_trade',
    'average_losing_trade', 'average_mfe', 'average_mae', 'average_winning_percentage', 'average_losing_percentage',
    'profit_factor', 'sharpe_ratio', 'consecutive_winners', 'consecutive_losers', 'average_trade_time', 'average_winning_time',
    'average_losing_time', 'average_time_between_trades', 'max_flat_time']

empty_stats_cols = [
    'symbol', 'entry_time', 'exit_time', 'direction', 'entry_price', 'exit_price', 'quantity', 'commission', 'pnl_tick',
    'time_to_live', 'pnl_amount', 'pnl_with_commission', 'mfe', 'mfe_time', 'mae', 'mae_time', 'features']

rename_stats_col = dict(
    net_profit=dict(title='Net Profit', format='{: >10,.0f}'),
    gross_profit=dict(title='Gross Profit', format='{:,.0f}'),
    gross_loss=dict(title='Gross Loss', format='{:,.0f}'),
    total_commission=dict(title='Commission', format='{:,.0f}'),
    max_drawdown=dict(title='Drawdown', format='{:,.0f}'),
    number_of_winning_trades=dict(title='Win Count', format='{:,.0f}'),
    number_of_losing_trades=dict(title='Loss Count', format='{:,.0f}'),
    total_trade_count=dict(title='Total Trades', format='{:,.0f}'),
    largest_winning_trade=dict(title='Largest Win', format='{:,.0f}'),
    largest_losing_trade=dict(title='Largest Loss', format='{:,.0f}'),
    average_winning_trade=dict(title='Average Win', format='{:,.0f}'),
    average_losing_trade=dict(title='Average Loss', format='{:,.0f}'),
    average_mfe=dict(title='Average MFE', format='{:,.2f}'),
    average_mae=dict(title='Average MAE', format='{:,.2f}'),
    average_winning_percentage=dict(title='Win Pct.', format='{:,.3f}'),
    average_losing_percentage=dict(title='Losing Pct.', format='{:,.3f}'),
    profit_factor=dict(title='Profit Factor', format='{:,.2f}'),
    sharpe_ratio=dict(title='Sharpe Ratio', format='{:,.2f}'),
    consecutive_winners=dict(title='Consecutive Wins', format='{:,.2f}'),
    consecutive_losers=dict(title='Consecutive Losses', format='{:,.2f}'),
    average_trade_time=dict(title='Average Trade Time', format='{:}'),
    average_winning_time=dict(title='Average Winning Time', format='{:}'),
    average_losing_time=dict(title='Average Losing Time', format='{:}'),
    average_time_between_trades=dict(title='Average Flat Time', format='{:}'),
    max_flat_time=dict(title='Max Flat Time', format='{:}'),
)

columns = ['entry_time', 'exit_time', 'direction', 'entry_price', 'exit_price', 'quantity', 'pnl_with_commission', 'mfe',
           'mae', 'time_to_live']
heading = ['#', 'ENTRY TIME', 'EXIT TIME', 'DIRECTION', 'ENTRY PX', 'EXIT PX', 'QTY.', 'PNL', 'MFE', 'MAE', 'TTL']

rename_pnl_col = dict(
    entry_time=dict(title='ENTRY TIME', format='{:}'),
    exit_time=dict(title='EXIT TIME', format='{:}'),
    direction=dict(title='DIRECTION', format='{:}'),
    entry_price=dict(title='ENTRY PX', format='{:,.2f}'),
    exit_price=dict(title='EXIT PX', format='{:,.2f}'),
    quantity=dict(title='QTY.', format='{:,.0f}'),
    pnl_with_commission=dict(title='PNL', format='{:,.2f}'),
    mfe=dict(title='MFE', format='{:,.2f}'),
    mae=dict(title='MAE', format='{:,.2f}'),
    time_to_live=dict(title='TTL', format='{:}'),
)


def add_signal_table(chart, data, height=1, width=0.1, position='right', color_style=color_style, chunks=3,
                     default_offset=pd.offsets.Hour(1)):
    data = data.reset_index(drop=True)
    if 'end_time' not in data.columns:
        data['end_time'] = data['start_time'] + default_offset

    data = data[['start_time', 'end_time']]
    data.index = data.index + 1

    headings = [convert_number_to_excel_column(x + 1) for x in range(chunks)]
    alignments = ('center' for _ in range(chunks))
    heading_color = (color_style.get('background_style').get('header_color') for _ in range(chunks))

    signal_table = chart.create_table(width=width, height=height, return_clicked_cells=True, headings=headings,
                                   heading_background_colors=heading_color, alignments=alignments, position=position,
                                   func=lambda row, column: row_move_to_chart_sig(row, column, chart=chart, df=data))
    list_df = [data[i:i + chunks] for i in range(0, data.shape[0], chunks)]

    for i, x in enumerate(list_df, 1):
        row = signal_table.new_row(*list(x.index.values))

        for heading in headings:
            row.background_color(column=heading, color=color_style.get('background_style').get('background_color'))

    return signal_table


def move_stats_table(table, footer_index, page_number, total_page_count, list_of_stats):
    footer = {0: 'previous', 1: 'page', 2: 'next'}.get(footer_index)

    table.footer[0] = '<< Previous'
    table.footer[2] = 'Next >>'

    if footer == 'previous':
        if page_number[0] > 1:
            page_number[0] = page_number[0] - 1
        else:
            table.footer[0] = ''
    elif footer == 'next':
        if page_number[0] < total_page_count:
            page_number[0] = page_number[0] + 1
        else:
            table.footer[2] = ''

    _table = list_of_stats[page_number[0] - 1]
    table.clear()

    for x in _table.itertuples():
        _stat = rename_stats_col.get(x.index, {'title': x.index, 'format': '{:}'})

        _stat_both = _stat.get('format').format(_formate_value(x.BOTH)) if not (pd.isna(x.BOTH) or x.BOTH == 0) else '-'
        _stat_long = _stat.get('format').format(_formate_value(x.LONG)) if not (pd.isna(x.LONG) or x.LONG == 0) else '-'
        _stat_short = _stat.get('format').format(_formate_value(x.SHORT)) if not (pd.isna(x.SHORT) or x.SHORT == 0) else '-'

        row = table.new_row(x.Index, _stat.get('title'), _stat_both, _stat_long, _stat_short)

        row.background_color(column='#', color=color_style.get('background_style').get('background_color'))
        row.background_color(column='STAT', color=color_style.get('background_style').get('background_color'))
        row.background_color(column='BOTH', color=color_style.get('background_style').get('background_color'))
        row.background_color(column='LONG', color=color_style.get('background_style').get('background_color'))
        row.background_color(column='SHORT', color=color_style.get('background_style').get('background_color'))

    table.footer[1] = f'{page_number[0]} / {total_page_count}'


def add_stats_table(chart, data, height=1, width=0.4, position='right', color_style=color_style, return_clicked_cells=False):
    try:
        stat_chucks = sorted(data.index.get_level_values('chunk').unique())
    except KeyError:
        stat_chucks = [0]

    list_of_stats = []

    try:
        for x in stat_chucks:
            _df = data[data.index.get_level_values('chunk') == x]
            _df = _df.droplevel(level='chunk')
            _df = _df.T.reset_index()
            _df.index = _df.index + 1
            list_of_stats.append(_df)

        consolidated_df = list_of_stats[0]
        list_of_stats = list_of_stats[1:]
        list_of_stats.append(consolidated_df)
    except KeyError:
        list_of_stats.append(pd.DataFrame(columns=['index', 'BOTH', 'LONG', 'SHORT']))

    alignments = ('center', 'left', 'right', 'right', 'right')
    heading_color = (color_style.get('background_style').get('header_color') for _ in range(len(alignments)))

    table = chart.create_table(position=position, height=height, width=width, headings=['#', 'STAT', 'BOTH', 'LONG', 'SHORT'],
                               func=row_click_event, return_clicked_cells=return_clicked_cells,
                               alignments=alignments, heading_background_colors=heading_color,
                               background_color=color_style.get('background_style').get('background_color'),
                               border_color=color_style.get('background_style').get('border_color'))

    for x in list_of_stats[-1].itertuples():
        _stat = rename_stats_col.get(x.index, {'title': x.index, 'format': '{:}'})

        _stat_both = _stat.get('format').format(_formate_value(x.BOTH)) if not (pd.isna(x.BOTH) or x.BOTH == 0) else '-'
        _stat_long = _stat.get('format').format(_formate_value(x.LONG)) if not (pd.isna(x.LONG) or x.LONG == 0) else '-'
        _stat_short = _stat.get('format').format(_formate_value(x.SHORT)) if not (pd.isna(x.SHORT) or x.SHORT == 0) else '-'

        row = table.new_row(x.Index, _stat.get('title'), _stat_both, _stat_long, _stat_short)

        row.background_color(column='#', color=color_style.get('background_style').get('background_color'))
        row.background_color(column='STAT', color=color_style.get('background_style').get('background_color'))
        row.background_color(column='BOTH', color=color_style.get('background_style').get('background_color'))
        row.background_color(column='LONG', color=color_style.get('background_style').get('background_color'))
        row.background_color(column='SHORT', color=color_style.get('background_style').get('background_color'))

    if len(list_of_stats) > 1:
        page_number = [len(stat_chucks)]
        table.footer(3, func=lambda x, y: move_stats_table(x, y, page_number=page_number, total_page_count=len(stat_chucks),
                                                           list_of_stats=list_of_stats))
        table.footer[0] = '<< Previous'
        table.footer[1] = f'{page_number[0]} / {len(stat_chucks)}'
        table.footer[2] = ''

    return table


def move_pnl_table(table, footer_index, page_number, total_page_count, list_of_pnls):
    footer = {0: 'previous', 1: 'page', 2: 'next'}.get(footer_index)

    table.footer[0] = '<< Previous'
    table.footer[2] = 'Next >>'

    if footer == 'previous':
        if page_number[0] > 1:
            page_number[0] = page_number[0] - 1
        else:
            table.footer[0] = ''
    elif footer == 'next':
        if page_number[0] < total_page_count:
            page_number[0] = page_number[0] + 1
        else:
            table.footer[2] = ''

    _table = list_of_pnls[page_number[0] - 1]
    table.clear()

    for x in _table.itertuples():
        row = table.new_row(x.Index, x.entry_time, x.exit_time, x.direction, x.entry_price, x.exit_price, x.quantity,
                            x.pnl_with_commission, x.mfe, x.mae, x.time_to_live)

        for column in heading:
            row.background_color(column=column, color=color_style.get('background_style').get('background_color'))

    table.footer[1] = f'{page_number[0]} / {total_page_count}'


def add_pnl_table(chart, data, height, width=1, position='bottom', color_style=color_style,
                  return_clicked_cells=True, pnl_chunk=100_000_000_000):
    data = data.reset_index(drop=True)

    data.index = data.index + 1
    list_of_pnls = [data[i:i + pnl_chunk] for i in range(0, data.shape[0], pnl_chunk)]
    data.index = data.index + 1

    columns = ['entry_time', 'exit_time', 'direction', 'entry_price', 'exit_price', 'quantity', 'pnl_with_commission', 'mfe',
               'mae', 'time_to_live']

    alignments = ('center', 'center', 'center', 'center', 'right', 'right', 'center', 'right', 'right', 'right', 'right')
    heading_color = (color_style.get('background_style').get('header_color') for _ in range(len(alignments)))

    data = data[columns]
    for col in data:
        data[col] = data[col].apply(lambda x: rename_pnl_col.get(col).get('format').format(x))

    heading = [rename_pnl_col.get(col).get('title') for col in data.columns]

    table = chart.create_table(position=position, height=height, width=width, headings=['#'] + heading,
                               return_clicked_cells=return_clicked_cells,
                               func=lambda row, column: row_move_to_chart(row, column, chart=chart),
                               alignments=alignments, heading_background_colors=heading_color,
                               background_color=color_style.get('background_style').get('background_color'),
                               border_color=color_style.get('background_style').get('border_color'))

    if len(list_of_pnls) >= 1:
        # hack to restrict page_numer int mutable and limit scope
        page_number = [len(list_of_pnls)]
        table.footer(3, func=lambda x, y: move_pnl_table(x, y, page_number=page_number, total_page_count=len(list_of_pnls),
                                                         list_of_pnls=list_of_pnls))
        table.footer[0] = '<< Previous'
        table.footer[1] = f'{page_number[0]} / {len(list_of_pnls)}'
        table.footer[2] = ''

        try:
            for x in list_of_pnls[-1].itertuples():
                row = table.new_row(x.Index, x.entry_time, x.exit_time, x.direction, x.entry_price, x.exit_price, x.quantity,
                                    x.pnl_with_commission, x.mfe, x.mae, x.time_to_live)

                for column in heading:
                    row.background_color(column=column, color=color_style.get('background_style').get('background_color'))
        except IndexError:
            ...

    return table
