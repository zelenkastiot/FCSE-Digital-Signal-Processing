"""

 Created on 06-Nov-20
 @author: Kiril Zelenkovski

 @title: 3-1-plotly-OHLC.py
 @description: get, clean and plot Historical tick data from MachineLearningTickData.
 @source: MachineLearningTickData
 @key-words: Python, Plotly & Pandas

"""
# Import modules
import pandas as pd
import plotly.graph_objs as go
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


# Plot data; create traces
fig = go.Figure()

fig.add_trace(go.Ohlc(x=df.index,
                      open=df['open'],
                      high=df['high'],
                      low=df['low'],
                      close=df['close'],
                      increasing_line_color='green',
                      decreasing_line_color='red',
                      showlegend=True,
                      name='Currency Quote'))

# Make subplots
fig.update_layout(title='Analysis: Hour Tick Data from Jan to May 2017  [EUR/USD]',
                  title_x=0.5,
                  hovermode='x',
                  xaxis_range=[df.index.array[0], df.index.array[1500]])

# Local offline use
plot(fig, filename='plots/plt3_HourTickData-JanMay2017.html')
