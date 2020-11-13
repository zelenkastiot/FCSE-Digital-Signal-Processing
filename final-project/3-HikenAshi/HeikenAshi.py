"""

 Created on 11-Nov-20
 @author: Kiril Zelenkovski
 @description: Feature Creation |
    Heiken Ashi Candlestick: Candlestick data that capture the
                             market momentum better.
"""

# Import modules
import pandas as pd
import plotly.graph_objs as go
from plotly import subplots
from plotly.offline import plot
from feature_functions import *

# ------------------( 1 ) Load data, create moving average ------------------------
df = pd.read_csv('../Data/EURUSD_hours.csv')

# Rename columns
df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

# Fix dates
df['date'] = pd.to_datetime(df['date'], format="%d.%m.%Y %H:%M:%S.%f")

# Set index column
df = df.set_index(df['date'])

# Clean duplicates
df = df.drop_duplicates(keep=False)

# SMA (Simple Moving Average 30 hours)
ma = df['close'].rolling(center=False, window=30).mean()

# ------------------( 2 ) Get function data from selected function ------------------

periods_list = [1]
HA_results = heikenAshi(prices=df, periods=periods_list)
HA = HA_results['candles'][1]

# -------------------(3) Plot the data ----------------------------------------------
trace0 = go.Ohlc(x=df.index,
                 open=df['open'],
                 high=df['high'],
                 low=df['low'],
                 close=df['close'],
                 name='Currency Quote (OHLC)',
                 visible='legendonly')

trace1 = go.Scatter(x=df.index,
                    y=ma,
                    marker=dict(color='blue', line=dict(width=0.1)),
                    name='Simple Moving Average(30h)',
                    visible="legendonly")

trace2 = go.Candlestick(x=HA.index,
                        open=HA['open'],
                        high=HA['high'],
                        low=HA['low'],
                        close=HA['close'],
                        name='Hiken Ashi Candlestick data (OHLC)',
                        increasing_line_color='cyan',
                        decreasing_line_color='gray')

fig = go.Figure()
fig.add_trace(trace0)
fig.add_trace(trace1)
fig.add_trace(trace2)

fig.update_layout(title='Analysis_3: Heiken Ashi Candlestick Jan-May 2017  [EUR/USD]',
                  title_x=0.5,
                  hovermode='x',
                  xaxis_range=[df.index.array[0], df.index.array[1500]],
                  yaxis=dict(anchor="x",
                             autorange=True))

# Local offline use
plot(fig, filename='plots/plt3_HikenAshi.html')

