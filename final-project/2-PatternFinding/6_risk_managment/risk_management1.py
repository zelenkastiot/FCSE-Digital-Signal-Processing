"""

 Created on 10-Nov-20
 @author: Kiril Zelenkovski

    Investigate best time to get out of trade.
    Pips - a 1000 decimal point of the data (price[end])

"""

# Import modules
from scipy.signal import argrelextrema
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm


# Peak finding function
def peak_detect(price_data, order=10):
    # Find max relative extrema, to smooth noise: change order
    max_idx = list(argrelextrema(price_data, comparator=np.greater, order=order)[0])
    # Find min relative extrema, to smooth noise: change order
    min_idx = list(argrelextrema(price_data, comparator=np.less, order=order)[0])
    # Combine lists to get all local extrema (not ordered)
    idx = max_idx + min_idx + [len(price_data) - 1]
    # Order extrema
    idx.sort()

    # Get last 5 peaks for pattern finding
    curr_dx = idx[-5:]

    # Get prices that are of interest to us
    START = min(curr_dx)
    END = max(curr_dx)

    # Find peaks for plotting
    curr_pattern = price_data[curr_dx]

    return curr_dx, curr_pattern, START, END


# 1: Classic Gartley pattern finding function
def is_gartley(price_moves, err):
    xa = price_moves[0]
    ab = price_moves[1]
    bc = price_moves[2]
    cd = price_moves[3]

    # Classic Gartley pattern ranges
    AB_range = np.array([0.618 - err, 0.618 + err]) * abs(xa)
    BC_range = np.array([0.382 - err, 0.886 + err]) * abs(ab)
    CD_range = np.array([1.27 - err, 1.618 + err]) * abs(bc)

    # Classic Gartley Bullish patterns (type 1): up-down-up-down
    if xa > 0 and ab < 0 and bc > 0 and cd < 0:
        # Check with absolute value function because the ranges are always positive
        if AB_range[0] < abs(ab) < AB_range[1] and \
                BC_range[0] < abs(bc) < BC_range[1] and \
                CD_range[0] < abs(cd) < CD_range[1]:
            return 1  # Found

        else:
            return np.NAN


    # Classic Gartley Bearish patterns (type 2): down-up-down-up
    elif xa < 0 and ab > 0 and bc < 0 and cd > 0:
        # Check with absolute value function because the ranges are always positive
        if AB_range[0] < abs(ab) < AB_range[1] and \
                BC_range[0] < abs(bc) < BC_range[1] and \
                CD_range[0] < abs(cd) < CD_range[1]:
            return -1  # Found

        else:
            return np.NAN

    else:
        return np.NAN


# 2: Butterfly Gartley pattern finding function
def is_butterfly(price_moves, err):
    xa = price_moves[0]
    ab = price_moves[1]
    bc = price_moves[2]
    cd = price_moves[3]

    # Butterfly Gartley pattern ranges
    AB_range = np.array([0.786 - err, 0.786 + err]) * abs(XA)
    BC_range = np.array([0.382 - err, 0.886 + err]) * abs(AB)
    CD_range = np.array([1.618 - err, 2.618 + err]) * abs(BC)

    # Butterfly Bullish  (type 1): up-down-up-down
    if xa > 0 and ab < 0 and bc > 0 and cd < 0:
        # Check with absolute value function because the ranges are always positive
        if AB_range[0] < abs(ab) < AB_range[1] and \
                BC_range[0] < abs(bc) < BC_range[1] and \
                CD_range[0] < abs(cd) < CD_range[1]:
            return 1  # Found

        else:
            return np.NAN


    # Butterfly Bearish (type 2): down-up-down-up
    elif xa < 0 and ab > 0 and bc < 0 and cd > 0:
        # Check with absolute value function because the ranges are always positive
        if AB_range[0] < abs(ab) < AB_range[1] and \
                BC_range[0] < abs(bc) < BC_range[1] and \
                CD_range[0] < abs(cd) < CD_range[1]:
            return -1  # Found

        else:
            return np.NAN

    else:
        return np.NAN


# 3: Bat Gartley pattern finding function
def is_bat(price_moves, err):
    xa = price_moves[0]
    ab = price_moves[1]
    bc = price_moves[2]
    cd = price_moves[3]

    # Bat Gartley pattern ranges
    AB_range = np.array([0.382 - err, 0.5 + err]) * abs(xa)
    BC_range = np.array([0.382 - err, 0.886 + err]) * abs(ab)
    CD_range = np.array([1.618 - err, 2.618 + err]) * abs(bc)

    # Bat Bullish (type 1): up-down-up-down
    if xa > 0 and ab < 0 and bc > 0 and cd < 0:

        if AB_range[0] < abs(ab) < AB_range[1] and \
                BC_range[0] < abs(bc) < BC_range[1] and \
                CD_range[0] < abs(cd) < CD_range[1]:
            return 1  # Found

        else:
            return np.NAN

    # Bat Bearish (type 2): down-up-down-up
    elif xa < 0 and ab > 0 and bc < 0 and cd > 0:
        if xa > 0 and ab < 0 and bc > 0 and cd < 0:

            if AB_range[0] < abs(ab) < AB_range[1] and \
                    BC_range[0] < abs(bc) < BC_range[1] and \
                    CD_range[0] < abs(cd) < \
                    CD_range[1]:
                return -1  # Found

            else:
                return np.NAN


# 4: Crab Gartley pattern finding function
def is_crab(price_moves, err):
    xa = price_moves[0]
    ab = price_moves[1]
    bc = price_moves[2]
    cd = price_moves[3]

    # Crab Gartley pattern ranges
    AB_range = np.array([0.382 - err, 0.618 + err]) * abs(xa)
    BC_range = np.array([0.382 - err, 0.886 + err]) * abs(ab)
    CD_range = np.array([2.24 - err, 3.618 + err]) * abs(bc)

    # Crab Bullish (type 1): up-down-up-down
    if xa > 0 and ab < 0 and bc > 0 and cd < 0:

        if AB_range[0] < abs(ab) < AB_range[1] and \
                BC_range[0] < abs(bc) < BC_range[1] and \
                CD_range[0] < abs(cd) < CD_range[1]:
            return 1  # Found

        else:
            return np.NAN

    # Crab Bearish (type 2): down-up-down-up
    elif xa < 0 and ab > 0 and bc < 0 and cd > 0:
        if xa > 0 and ab < 0 and bc > 0 and cd < 0:

            if AB_range[0] < abs(ab) < AB_range[1] and \
                    BC_range[0] < abs(bc) < BC_range[1] and \
                    CD_range[0] < abs(cd) < \
                    CD_range[1]:
                return -1  # Found

            else:
                return np.NAN


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

    # Error allowed (10%) setting interval for analysis
    err_allowed = 0.10  # eg. (51.8, 71.8) for 61.8%

    # Dynamic plot
    plt.ion()

    # Count patterns found
    total_pat_found = 0

    # Loop dataset
    for i in tqdm(range(100, len(price))):
        # Captured pips (15h): If we get in one of those 15 hours after, how much pips we would have collected
        pips = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

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

        if np.any(harmonics == 1) or np.any(harmonics == -1):
            total_pat_found += 1
            for j in range(0, len(harmonics)):

                if harmonics[j] == 1 or harmonics[j] == -1:
                    # Bearish / Bullish
                    sense = 'Bearish ' if harmonics[j] == -1 else 'Bullish '
                    # Classic / Butterfly / Bat / Crab
                    label = f'{total_pat_found} :' + sense + labels[j] + ' Found (+15h)'

                    # Plot found pattern
                    plt.title(label)
                    plt.plot(np.arange(start, i + 15), price.values[start:i + 15])
                    plt.plot(current_idx, current_pattern, c='r')
                    plt.show()

                    # Long trade
                    if harmonics[j] == 1:
                        pips += 1000 * (price[end + 1:end + 16] - price[end])

                    # Short trade
                    elif harmonics[j] == -1:
                        pips += 1000 * (price[end] - price[end + 1:end + 16])

                    plt.clf()

                    # Plot trade earnings
                    label2 = label + "; Trade Earnings (pips)"
                    plt.title(label2)
                    plt.bar(np.arange(1, 16), pips, color=(0.2, 0.4, 0.6, 0.6))
                    plt.draw()
                    plt.pause(0.05)

print(f"Total number of patterns found is: {total_pat_found}")
