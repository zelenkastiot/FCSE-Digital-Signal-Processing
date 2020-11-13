"""

 Created on 07-Nov-20
 @author: Kiril Zelenkovski

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from tqdm import tqdm

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
price = data['close'].iloc[:500]

# Find patterns
total = 0

# Loop events
for i in range(100, len(price)):
    # Find max relative extrema, to smooth noise: change order
    max_idx = list(argrelextrema(price.values[:i], comparator=np.greater, order=10)[0])
    # Find min relative extrema, to smooth noise: change order
    min_idx = list(argrelextrema(price.values[:i], comparator=np.less, order=10)[0])
    # Combine lists to get all local extrema (not ordered)
    idx = max_idx + min_idx + [len(price.values[:i]) - 1]
    # Order extrema
    idx.sort()

    # get last 5 peaks for pattern finding
    current_idx = idx[-5:]

    # Get prices that are of interest to us
    start = min(current_idx)
    end = max(current_idx)

    # Find peaks for plotting
    current_pattern = price.values[current_idx]

    '''
    Looks like Gartley Pattern: 
    UP -> DOWN -> UP -> DOWN 
    '''
    XA = current_pattern[1] - current_pattern[0]  # XA needs to be positive (>0)
    AB = current_pattern[2] - current_pattern[1]  # AB needs to be negative (<0)
    BC = current_pattern[3] - current_pattern[2]  # BC needs to be positive (>0)
    CD = current_pattern[4] - current_pattern[3]  # CD needs to be negative (<0)

    plt.ion()
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        total += 1
        plt.plot(np.arange(start, i), price.values[start:i])
        plt.plot(current_idx, current_pattern, c='r')
        plt.title(label=f'{total}: Up-Down-Up-Down pattern; EUR/USD')
        plt.show()

print(f'Total UP -> DOWN -> UP -> DOWN patterns found: {total}')
