"""

 Created on 07-Nov-20
 @author: Kiril Zelenkovski

 patter_analysis.py

    Continuation of 'pattern_finding.py'. Main objective try to see if on of these
    price moves meet the requirements to be a certain type of harmonic pattern.

    The first harmonic pattern we are going to look at is "Gartley Pattern".
    They fit the price retracement to certain Fibonacci ratios (levels).

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
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

# Read whole close column
price = data['close'].copy()

# Error allowed (10%) setting interval for analysis
err_allowed = 0.10  # eg. (51.8, 71.8) for 61.8%

# Counter for found patterns
count_pattern_bullish = 0
count_pattern_bearish = 0


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
    Gartley Patterns: 
    1. Bullish Gartley pattern 
    UP -> DOWN -> UP -> DOWN 
    
    2.Bearish Gartley pattern 
    DOWN -> UP -> DOWN -> UP 
    
    How to check: 
     - Pattern has to be general (up-down-up-down) 
     - If it is, then define the range that the price movement needs to fall under
     - Eg. The price move AB needs to be 61.8% (~ or close to 0.618) of XA 
     - Find values for ranges using the Gartley Pattern definition 
     - Check if general pattern movements fall in their range
     - If they do then plot those patterns 
    '''
    XA = current_pattern[1] - current_pattern[0]  # XA needs to be positive (>0)
    AB = current_pattern[2] - current_pattern[1]  # AB needs to be negative (<0)
    BC = current_pattern[3] - current_pattern[2]  # BC needs to be positive (>0)
    CD = current_pattern[4] - current_pattern[3]  # CD needs to be negative (<0)



    # bullish patterns (type 1): up-down-up-down
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        # Define ranges: list where list[0]: min, list[1]: max
        AB_range = np.array([0.618 - err_allowed, 0.618 + err_allowed]) * abs(XA)
        BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.27 - err_allowed, 1.618 + err_allowed]) * abs(BC)

        # Check with absolute value function because the ranges are always positive
        if AB_range[0] < abs(AB) < AB_range[1]:
            if BC_range[0] < abs(BC) < BC_range[1]:
                if CD_range[0] < abs(CD) < CD_range[1]:
                    # Increment pattern counter
                    count_pattern_bullish += 1

                    # Plot patterns
                    plt.plot(np.arange(start, i), price.values[start:i])
                    plt.axvline(np.arange(start, i)[-1], c='g', ls='--', label='End of pattern')
                    text(1866, 1.078, "end of pattern", rotation=0, verticalalignment='center',
                         bbox=dict(facecolor='gray', alpha=0.5))
                    plt.plot(current_idx, current_pattern, c='r')
                    plt.title(label=f'{count_pattern_bullish}: Bullish Gartley Pattern; EUR/USD')
                    plt.show()

                    # Check if we were correct: Easy! See in the feature
                    plt.plot(np.arange(start, i+24), price.values[start:i+24])  # +Plot of data 24h later
                    plt.axvline(np.arange(start, i)[-1], c='g', ls='--', label='End of pattern')
                    text(1860, 1.081, "end of pattern ", rotation=0, verticalalignment='center',
                         bbox=dict(facecolor='gray', alpha=0.5))
                    plt.plot(current_idx, current_pattern, c='r')
                    plt.title(label=f'{count_pattern_bullish}: Bullish Gartley Pattern+24h; EUR/USD')
                    plt.show()


    # bearish patterns (type 2): down-up-down-up
    elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
        # Define ranges: list where list[0]: min, list[1]: max
        AB_range = np.array([0.618 - err_allowed, 0.618 + err_allowed]) * abs(XA)
        BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.27 - err_allowed, 1.618 + err_allowed]) * abs(BC)

        # Check with absolute value function because the ranges are always positive
        if AB_range[0] < abs(AB) < AB_range[1]:
            if BC_range[0] < abs(BC) < BC_range[1]:
                if CD_range[0] < abs(CD) < CD_range[1]:
                    # Increment pattern counter
                    count_pattern_bearish += 1

                    # Plot patterns
                    plt.plot(np.arange(start, i), price.values[start:i])
                    plt.axvline(np.arange(start, i)[-1], c='g', ls='--', label='End of pattern')
                    text(1866, 1.078, "end of pattern", rotation=0, verticalalignment='center',
                         bbox=dict(facecolor='gray', alpha=0.5))
                    plt.plot(current_idx, current_pattern, c='r')
                    plt.title(label=f'{count_pattern_bearish}: Bearish Gartley Pattern; EUR/USD')
                    plt.show()

                    # Check if we were correct: Easy! See in the feature
                    plt.plot(np.arange(start, i+24), price.values[start:i+24])  # +Plot of data 24h later
                    plt.axvline(np.arange(start, i)[-1], c='g', ls='--', label='End of pattern')
                    text(1860, 1.081, "end of pattern ", rotation=0, verticalalignment='center',
                         bbox=dict(facecolor='gray', alpha=0.5))
                    plt.plot(current_idx, current_pattern, c='r')
                    plt.title(label=f'{count_pattern_bearish}: Bearish Gartley Pattern+24h; EUR/USD')
                    plt.show()
