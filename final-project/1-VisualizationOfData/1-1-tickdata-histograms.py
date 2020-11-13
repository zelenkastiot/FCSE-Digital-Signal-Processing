"""

 Created on 10-Nov-20
 @author: Kiril Zelenkovski

 The main point of a histogram is to visualize the distribution of our data. We don’t want our chart to have too many
 bins because that could hide the concentrations in our data; simultaneously, we don’t want a low number of classes
 because we could misinterpret the distribution.


"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import gridspec
import seaborn as sns
from scipy import stats
import plotly.graph_objs as go
from plotly.offline import plot

pd.set_option('mode.chained_assignment', None)
sns.set()

# Read dataset
data = pd.read_csv('../Data/EURUSD_Ticks_20-01-2020.csv')
data2 = pd.read_csv('../Data/USDJPY_Ticks_20-01-2017.csv')

# Rename columns
data.columns = ['date', 'ask', 'bid', 'ask_volume', 'bid_volume']
data2.columns = ['date', 'ask', 'bid', 'ask_volume', 'bid_volume']

# Fix dates
data['date'] = pd.to_datetime(data['date'], format="%d.%m.%Y %H:%M:%S.%f")
data2['date'] = pd.to_datetime(data2['date'], format="%d.%m.%Y %H:%M:%S.%f")

# Set index column
data = data.set_index(data['date'])
data2 = data2.set_index(data2['date'])

# Clean duplicates
data = data.drop_duplicates(keep=False)
data2 = data2.drop_duplicates(keep=False)

# Read whole close column
price = data['bid'].copy()
price2 = data2['bid'].copy()


# EUR/USD
f, a = plt.subplots(figsize=(8, 6))
plt.title('Bid data EUR/USD; 20.01.2017')
sns.histplot(data['bid'], stat='density', kde=True)
plt.show()

plt.clf()
f, a = plt.subplots(figsize=(8, 6))
stats.probplot(data['bid'], plot=plt)
plt.show()

# data['Bid'] = np.log1p(d['SalePrice'])

# USD/JPY
f2, a2 = plt.subplots(figsize=(8, 6))
plt.title('Bid data USD/JPY; 20.01.2017')
sns.histplot(data2['bid'], stat='density', kde=True)
plt.show()

plt.clf()
f2, a2 = plt.subplots(figsize=(8, 6))
stats.probplot(data2['bid'], plot=plt)
plt.show()



fig1 = go.Figure()
fig1.add_trace(go.Box(y=data["bid"],
                      name="Bid Price Box plot",
                      boxmean='sd',
                      boxpoints='outliers',
                      marker_color='black',
                      fillcolor='rgba(93, 164, 214, 0.5)',
                      marker_size=2,
                      line_width=0.6))

fig1.update_layout(title='EUR/USD box plot; 20.01.2017',
                   title_x=0.5,
                   width=800,
                   height=520,
                   font=dict(size=10),
                   margin=go.layout.Margin(l=50,
                                           r=50,
                                           b=60,
                                           t=35))


fig2 = go.Figure()
fig2.add_trace(go.Box(y=data2["bid"],
                      name="Bid Price Box plot",
                      boxmean='sd',
                      boxpoints='outliers',
                      marker_color='black',
                      fillcolor='rgba(93, 164, 214, 0.5)',
                      marker_size=2,
                      line_width=0.6))

fig2.update_layout(title='USD/JPY box plot; 20.01.2017',
                   title_x=0.5,
                   width=800,
                   height=520,
                   font=dict(size=10),
                   margin=go.layout.Margin(l=50,
                                           r=50,
                                           b=60,
                                           t=35))

# Local offline use
plot(fig1, filename='plots/plt1_TickData_EUR_USD.html')
plot(fig2, filename='plots/plt2_TickData_USD_JPY.html')
