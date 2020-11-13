"""

 Created on 06-Nov-20
 @author: Kiril Zelenkovski

 @title: testing.py
 @description: Plot historical data using Open High Low Close plots, also plot Volume as bar plots
 @key-words: Python, Plotly & Pandas

"""
# Import modules
import pandas as pd
import plotly.graph_objs as go
from plotly import subplots
from plotly.offline import plot
from feature_functions import *

# ------------------( 1 ) Load data, create moving average ------------------------
df = pd.read_csv('Data/EURUSD_hours.csv')

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

detrended = deTrend(prices=df, method='linear')
# detrended = deTrend(prices=df, method='difference')

# -------------------(3) Plot the data ----------------------------------------------

trace0 = go.Ohlc(x=df.index,
                 open=df['open'],
                 high=df['high'],
                 low=df['low'],
                 close=df['close'],
                 name='Currency Quote (OHLC)',
                 visible=True)

trace1 = go.Scatter(x=df.index,
                    y=ma,
                    marker=dict(color='blue',
                                line=dict(width=0.1)),
                    name='Simple Moving Average(30h)',
                    visible=True)

trace2 = go.Scatter(x=df.index,
                    y=detrended,
                    name='Detrended Series')

trace3 = go.Scatter(x=df.index,
                    y=np.array([0]*len(df)),
                    marker=dict(color='gray',
                                line=dict(width=0.1)),
                    name='Zero line',
                    showlegend=False,
                    hoverinfo='none'
                    )

# Make subplots
fig = subplots.make_subplots(rows=2,
                             cols=1,
                             shared_xaxes=True,
                             vertical_spacing=0.02)


fig.append_trace(trace0, 2, 1)
fig.append_trace(trace1, 2, 1)
fig.append_trace(trace2, 1, 1)
fig.append_trace(trace3, 1, 1)


fig.update_layout(title='Analysis_4_2: Difference Detrended data Jan-May 2017  [EUR/USD]',
                  title_x=0.5,
                  hovermode='x',
                  xaxis_range=[df.index.array[0], df.index.array[250]],
                  yaxis=dict(anchor="x",
                             autorange=True))


# Local offline use
plot(fig, filename='General_plots/plt4_2_DifferenceDetrendedData.html')
