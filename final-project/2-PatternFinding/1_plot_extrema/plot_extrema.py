"""

 Created on 07-Nov-20
 @author: Kiril Zelenkovski
 @description: Harmonic Pattern Scanning

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

# Read dataset
data = pd.read_csv('../data/EURUSD_01-05_2017.csv')

# Rename columns
data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

# Fix dates
data['date'] = pd.to_datetime(data['date'], format="%d.%m.%Y %H:%M:%S.%f")

# Set index column
data = data.set_index(data['date'])

# Clean duplicates
data = data.drop_duplicates(keep=False)

# Read close price
price = data['close'].iloc[:100]

# Get local extrema for different orders, try to catch large price movements
for i in [1, 5, 10]:
    # Find max relative extrema, to smooth noise: change order
    max_idx = list(argrelextrema(price.values, comparator=np.greater, order=i)[0])
    # Find min relative extrema, to smooth noise: change order
    min_idx = list(argrelextrema(price.values, comparator=np.less, order=i)[0])
    # Combine lists to get all local extrema (not ordered)
    idx = max_idx + min_idx
    # Order extrema
    idx.sort()
    # Find peaks for plotting
    peaks = price.values[idx]

    # Plot data
    plt.plot(price.values)
    plt.scatter(x=idx, y=peaks, c='r')
    plt.title(label=f'EUR/USD, order={i}')
    plt.show()





