"""

 Created on 11-Nov-20
 @author: Kiril Zelenkovski

 Accuracy calculator

"""


# Import modules
from scipy.signal import argrelextrema
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from analysis_functions import *
from tqdm import tqdm

if __name__ == "__main__":
    # Read dataset
    data = pd.read_csv('../data/EURUSD_2017-2020.csv')

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

    # Error allowed (5%) setting interval for analysis
    err_allowed = 5.0 / 100

    # Dynamic plot
    plt.ion()

    pnl = []  # Profit and Lost list
    trade_dates = []  # Trade dates
    correct_pats = 0
    total = 0

    # Loop dataset
    for i in tqdm(range(100, len(price.values))):

        # Get parameters from peak detection function
        current_idx, current_pattern, start, end = peak_detect(price.values[:i], order=5)

        # Calculate price moves: XA, AB, BC, CD
        XA = current_pattern[1] - current_pattern[0]
        AB = current_pattern[2] - current_pattern[1]
        BC = current_pattern[3] - current_pattern[2]
        CD = current_pattern[4] - current_pattern[3]

        # Organize moves
        moves = [XA, AB, BC, CD]

        # Use local functions to search for pattern findings
        gartleys = is_gartley(price_moves=moves, err=err_allowed)
        butterflies = is_butterfly(price_moves=moves, err=err_allowed)
        bats = is_bat(price_moves=price, err=err_allowed)
        crabs = is_crab(price_moves=moves, err=err_allowed)

        # Organizing found patterns
        harmonics = np.array([gartleys, butterflies, bats, crabs])
        labels = ['Gartley pattern',
                  'Butterfly pattern',
                  'Bat pattern',
                  'Crab pattern']

        # Goes inside loop if and only if he finds any pattern
        if np.any(harmonics == 1) or np.any(harmonics == -1):
            total += 1
            for j in range(0, len(harmonics)):

                if harmonics[j] == 1 or harmonics[j] == -1:
                    # Bearish / Bullish
                    sense = 'Bearish ' if harmonics[j] == -1 else 'Bullish '
                    # Classic / Butterfly / Bat / Crab
                    label = f'{total}: ' + sense + labels[j] + ' Traded'

                    # Get start, end in order to create date of pattern
                    start = np.array(current_idx).min()
                    end = np.array(current_idx).max()

                    # Hypothetically we are entering the trade at the end of te pattern
                    date = data.iloc[end].name
                    trade_dates = np.append(trade_dates, date)

                    # Get pips from the end of pattern: till the end of series
                    pips = walk_forward(price_series=price.values[end:],
                                        sign=harmonics[j],
                                        slippage=10,
                                        stop=6)

                    pnl = np.append(pnl, pips)
                    cumulative_pips = pnl.cumsum()

                    if pips > 0:
                        correct_pats += 1

                    lbl = 'Accuracy ' + str(100 * float(correct_pats)/float(total)) + ' %'

                    plt.clf()
                    plt.title(label + "; " + str(date))
                    plt.plot(cumulative_pips, label=lbl, linestyle='dashed', color="r")
                    plt.legend()
                    plt.pause(0.05)


