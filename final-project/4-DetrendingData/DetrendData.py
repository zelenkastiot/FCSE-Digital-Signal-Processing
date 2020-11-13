"""

 Created on 12-Nov-20
 @author: Kiril Zelenkovski

--------------------------LINEAR_DETREND----------------------------------------
Why the LINEAR-DETREND method is bad, because even tough we filtered
everything it still has the same trend (almost identical as the tick data)

The reason why this happens is because we are fitting a linear line over
the whole data series, so if we were to break it into smaller pieces
and fit a line and detrend it on that period (eg. over 5 days) then it
will work good.

--------------------------------------------------------------------------------
But, why go through so much effort when with "difference" method?
--------------------------------------------------------------------------------


--------------------DIFFERENCE_DETREND------------------------------------------

This gives use beautiful data that is completely detrended. It oscillates
around zero, that is what we want to lose the trend. Stationary time series
where we can fit Fourier or a Sine expansion curve to this data and it will
allow us higher degree od prediction pattern. This probably has the higher
prediction power than the other features.

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


method_trend = 'linear'
# method_trend = 'difference'

detrended = deTrend(prices=df, method=method_trend)

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
                    hoverinfo='none')

# Make subplots
fig = subplots.make_subplots(rows=2,
                             cols=1,
                             shared_xaxes=True,
                             vertical_spacing=0.02)


fig.append_trace(trace0, 2, 1)
fig.append_trace(trace1, 2, 1)
fig.append_trace(trace2, 1, 1)
fig.append_trace(trace3, 1, 1)

# Plot Fig 4.1
if method_trend == 'linear':
    fig.update_layout(title='Analysis_4_1: Linear Detrended data Jan-May 2017  [EUR/USD]',
                      title_x=0.5,
                      hovermode='x',
                      xaxis_range=[df.index.array[0], df.index.array[250]],
                      yaxis=dict(anchor="x",
                                 autorange=True))


    # Local offline use
    plot(fig, filename='plots/plt4_1_LinearDetrendedData.html')


# Plot Fig 4.2
elif method_trend == 'difference':
    fig.update_layout(title='Analysis_4_2: Difference Detrended data Jan-May 2017  [EUR/USD]',
                      title_x=0.5,
                      hovermode='x',
                      xaxis_range=[df.index.array[0], df.index.array[250]],
                      yaxis=dict(anchor="x",
                                 autorange=True))


    # Local offline use
    plot(fig, filename='plots/plt4_2_DifferenceDetrendedData.html')
