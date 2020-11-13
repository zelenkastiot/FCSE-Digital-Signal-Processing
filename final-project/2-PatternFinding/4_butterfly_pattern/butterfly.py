"""

 Created on 08-Nov-20
 @author: Kiril Zelenkovski

 butterfly.py

    Continuation of 'pattern_analysis.py'.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from analysis_functions import peak_detect

# Tight layout
plt.tight_layout()

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
    # Get peaks for pattern analysis
    current_idx, current_pattern, start, end = peak_detect(price.values[:i])

    '''
    Butterfly Pattern: 
    
    - Has Bullish and Bearish same as Garltey's
    - Difference is in the price moves range, more specific in the ratios  
    
    1:bullish patterns (type 1): up-down-up-down
    2:bearish patterns (type 2): down-up-down-up
    
    '''
    # Price moves
    XA = current_pattern[1] - current_pattern[0]  # XA needs to be positive (>0)
    AB = current_pattern[2] - current_pattern[1]  # AB needs to be negative (<0)
    BC = current_pattern[3] - current_pattern[2]  # BC needs to be positive (>0)
    CD = current_pattern[4] - current_pattern[3]  # CD needs to be negative (<0)

    price_moves = [XA, AB, BC, CD]

    # bullish patterns (type 1): up-down-up-down
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        # Define ranges (BUTTERFLY): list where list[0]: min, list[1]: max
        AB_range = np.array([0.786 - err_allowed, 0.786 + err_allowed]) * abs(XA)
        BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.618 - err_allowed, 2.618 + err_allowed]) * abs(BC)

        # Check with absolute value function because the ranges are always positive
        if AB_range[0] < abs(AB) < AB_range[1]:
            if BC_range[0] < abs(BC) < BC_range[1]:
                if CD_range[0] < abs(CD) < CD_range[1]:
                    # Increment pattern counter
                    count_pattern_bullish += 1

                    # Plot patterns
                    plt.plot(np.arange(start, i), price.values[start:i])
                    plt.axvline(np.arange(start, i)[-1], c='g', ls='--', label='End of pattern')
                    text(1207, 1.06252, "end of pattern", rotation=0, verticalalignment='center',
                         bbox=dict(facecolor='gray', alpha=0.5))
                    plt.plot(current_idx, current_pattern, c='r')
                    plt.title(label=f'{count_pattern_bullish}: Butterfly Bullish  Pattern; EUR/USD')
                    plt.show()

                    # Check if we were correct: Easy! See in the feature
                    plt.plot(np.arange(start, i+24), price.values[start:i+24])  # +Plot of data 24h later
                    plt.axvline(np.arange(start, i)[-1], c='g', ls='--', label='End of pattern')
                    text(1202, 1.056, "end of pattern", rotation=0, verticalalignment='center',
                         bbox=dict(facecolor='gray', alpha=0.5))
                    plt.plot(current_idx, current_pattern, c='r')
                    plt.title(label=f'{count_pattern_bullish}: Butterfly Bullish Pattern+24h; EUR/USD')
                    plt.show()


    # bearish patterns (type 2): down-up-down-up
    elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
        # Define ranges: list where list[0]: min, list[1]: max
        AB_range = np.array([0.786 - err_allowed, 0.786 + err_allowed]) * abs(XA)
        BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.618 - err_allowed, 2.618 + err_allowed]) * abs(BC)

        # Check with absolute value function because the ranges are always positive
        if AB_range[0] < abs(AB) < AB_range[1]:
            if BC_range[0] < abs(BC) < BC_range[1]:
                if CD_range[0] < abs(CD) < CD_range[1]:
                    # Increment pattern counter
                    count_pattern_bearish += 1

                    # Plot patterns
                    plt.plot(np.arange(start, i), price.values[start:i])
                    plt.axvline(np.arange(start, i)[-1], c='g', ls='--', label='End of pattern')
                    plt.plot(current_idx, current_pattern, c='r')
                    plt.title(label=f'{count_pattern_bearish}: Butterfly Bearish Pattern; EUR/USD')
                    plt.show()

                    # Check if we were correct: Easy! See in the feature
                    plt.plot(np.arange(start, i+24), price.values[start:i+24])  # +Plot of data 24h later
                    plt.axvline(np.arange(start, i)[-1], c='g', ls='--', label='End of pattern')
                    plt.plot(current_idx, current_pattern, c='r')
                    plt.title(label=f'{count_pattern_bearish}: Butterfly Bearish Pattern+24h; EUR/USD')
                    plt.show()
