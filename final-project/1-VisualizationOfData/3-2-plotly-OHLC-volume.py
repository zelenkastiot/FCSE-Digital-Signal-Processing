"""

 Created on 06-Nov-20
 @author: Kiril Zelenkovski

 @title: 3-2-plotly-OHLC-volume.py
 @description: Plot historical data using Open High Low Close plots, also plot Volume as bar plots
 @source: MachineLearningTickData
 @key-words: Python, Plotly & Pandas

"""
# Import modules
import pandas as pd
import plotly.graph_objs as go
from plotly import subplots
from plotly.offline import plot


# Read dataset
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

# Plot data; create traces
trace0 = go.Ohlc(x=df.index,
                 open=df['open'],
                 high=df['high'],
                 low=df['low'],
                 close=df['close'],
                 name='Currency Quote (OHLC)')

trace1 = go.Scatter(x=df.index,
                    y=ma,
                    marker=dict(color='blue', line=dict(width=0.1)),
                    name='Simple Moving Average(30h)')

trace2 = go.Bar(x=df.index,
                y=df['volume'],
                marker=dict(color='red'),
                name='Currency Volume')

# Make subplots
fig = subplots.make_subplots(rows=2,
                             cols=1,
                             shared_xaxes=True,
                             vertical_spacing=0.02)

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 2, 1)

fig.update_layout(title='Analysis: Hour Tick Data + Volume from Jan to May 2017  [EUR/USD]',
                  title_x=0.5,
                  hovermode='x',
                  xaxis_range=[df.index.array[0], df.index.array[1500]])

# Local offline use
plot(fig, filename='plots/plt4_HourTickDataVolume-JanMay2017.html')
