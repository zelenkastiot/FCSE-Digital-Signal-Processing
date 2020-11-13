"""

 Created on 08-Nov-20
 @author: Kiril Zelenkovski

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
    AB_range = np.array([0.786 - err, 0.786 + err]) * abs(xa)
    BC_range = np.array([0.382 - err, 0.886 + err]) * abs(ab)
    CD_range = np.array([1.618 - err, 2.618 + err]) * abs(bc)

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


# 5: Walk forward check
def walk_forward(price_series, sign, slippage=4, stop=10):
    """
    :param price_series: price series that we want to wal over
    :param sign: takes on values 1 or -1.
                 sign=1 is long trade
                 sign=-1 is short trade
    :param slippage: fixed loss; accounts for the spread of market, we use it for worst case scenario
    :param stop: amount of pips for stoppage of trading
    :return:
    """

    slippage = float(slippage) / float(10000)  # dividing by 10^4 to get pips
    stop_amount = float(stop) / float(10000)  # dividing by 10^4 to get pips

    # Long trade
    if sign == 1:
        # initial stop loss is below the initial price that we entered the trade at
        initial_stop_loss = price_series[0] - stop_amount
        # this stop_los changes values
        stop_loss = initial_stop_loss

        # loop for walking trough the series
        for k in range(1, len(price_series)):
            # we move once and check if price went up or down: current price-last price
            move = price_series[k] - price_series[k - 1]

            # move is positive and the current price - the stop price is larger than initial stop loss
            if move > 0 and (price_series[k] - stop_amount) > initial_stop_loss:
                # move stop_loss up
                stop_loss = price_series[k] - stop_amount

            # if we did get stopped out, price is below the stop loss
            elif price_series[k] < stop_loss:
                # cut losses and get out: return pips:
                return stop_loss - price_series[0] - slippage

    # Shor trade; everything is opposite
    elif sign == -1:
        # initial stop loss is above the initial price that we entered the trade at
        initial_stop_loss = price_series[0] + stop_amount
        # this stop_loss changes values
        stop_loss = initial_stop_loss

        # loop for walking trough the series
        for k in range(1, len(price_series)):
            # we move once and check if price went up or down: current price-last price
            move = price_series[k] - price_series[k - 1]

            # check if move is less than 0, and price + stop is less than initial stop
            if move < 0 and (price_series[k] + stop_amount) < initial_stop_loss:
                # move stop_loss down
                stop_loss = price_series[k] + stop_amount

            # if we did get stopped out, price is above the stop loss
            elif price_series[k] > stop_loss:
                return price_series[0] - stop_loss - slippage

