#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import numpy as np
import pandas as pd
import pandas.io.data as web


def get_quote_yahoojp(code, start=None, end=None, interval='d'):
    base = 'http://info.finance.yahoo.co.jp/history/?code={0}.T&{1}&{2}&tm={3}&p={4}'
    start, end = web._sanitize_dates(start, end)
    start = 'sy={0}&sm={1}&sd={2}'.format(start.year, start.month, start.day)
    end = 'ey={0}&em={1}&ed={2}'.format(end.year, end.month, end.day)
    p = 1
    results = []

    if interval not in ['d', 'w', 'm', 'v']:
        raise ValueError("Invalid interval: valid values are 'd', 'w', 'm' and 'v'")

    while True:
        url = base.format(code, start, end, interval, p)
        tables = pd.read_html(url, header=0)
        if len(tables) < 2 or len(tables[1]) == 0:
            break
        results.append(tables[1])
        p += 1
    result = pd.concat(results, ignore_index=True)

    result.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
    result['Date'] = pd.to_datetime(result['Date'], format='%Y年%m月%d日')
    result = result.set_index('Date')
    result = result.sort_index()
    return result


def DataReader(name, data_source=None, start=None, end=None, **kwargs):
    if data_source == "yahoojp":
        return get_quote_yahoojp(symbols=name, start=start,
                                 end=end, **kwargs)
    else:
        return web.DataReader(name, data_source=data_source,
                              start=start, end=end, **kwargs)


DataReader.__doc__ = web.DataReader.__doc__


if __name__ == '__main__':
    toyota_tse = DataReader(7203, 'yahoojp', start='2014-10-01')
    print(toyota_tse.head())
