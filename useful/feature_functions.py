"""

 Created on 11-Nov-20
 @author: Kiril Zelenkovski

Functions for creating potentially useful features for machine learning
prediction on Forex hour tick data.

List of useful functions:

 - 1: Heiken Ashi Candlestick data
 - 2: Detrending data for Fourier or Sine expansion
 - 3: 1st order Fourier series expansion
 - 4: Sine series expansion
 - 5: Fourier series coefficient Calculator function
 - 6: Sine series coefficient Calculator function

"""
import pandas as pd
import numpy as np
from scipy import stats
import scipy.optimize
from scipy.optimize import OptimizeWarning
import warnings
import math
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime
import warnings

warnings.simplefilter("ignore", UserWarning)
import mplfinance as mpf


# 1: Heiken Ashi
def heikenAshi(prices, periods):
    """

    :param prices: pandas dataframe of OHlC & volume data
    :param periods: list of periods that we want to calculate the candles for
    :return: Hiken Ashi OHLC candles

    """
    results = {}

    # Dictionary for storing candles. We are going to store the candles in a dataframe in the dict
    candles_dict = {}

    # Hiken Ashi CLOSE
    HA_close = prices[['open', 'high', 'close', 'low']].sum(axis=1) / 4
    # Hiken Ashi OPEN
    HA_open = HA_close.copy()
    HA_open.iloc[0] = HA_close.iloc[0]
    # Hiken Ashi HIGH
    HA_high = HA_close.copy()
    # Hiken Ashi LOW
    HA_low = HA_close.copy()

    for i in range(1, len(prices)):
        HA_open.iloc[i] = (HA_open.iloc[i - 1] + HA_close[i - 1]) / 2

        HA_high.iloc[i] = np.array([prices['high'].iloc[i], HA_open.iloc[i], HA_close.iloc[i]]).max()

        HA_low.iloc[i] = np.array([prices['low'].iloc[i], HA_open.iloc[i], HA_close.iloc[i]]).min()

    df = pd.concat((HA_open, HA_high, HA_low, HA_close), axis=1)
    df.columns = ['open', 'high', 'low', 'close']
    candles_dict[periods[0]] = df
    results['candles'] = candles_dict
    return results


# 2: De-trending series
def deTrend(prices, method='difference'):
    """

    :param prices: pandas dataframe of OHLC currency data
    :param method: method to which to de-trend: 'linear' or 'difference'
    :return: the de-trended price series
    """

    if method == 'difference':

        de_trended = prices['close'][1:] - prices['close'][:-1].values

    elif method == 'linear':

        x = np.arange(0, len(prices))
        y = prices['close'].values

        model = LinearRegression()
        model.fit(x.reshape(-1, 1), y.reshape(-1, 1))

        trend = model.predict(x.reshape(-1, 1))

        trend = trend.reshape((len(prices),))

        de_trended = prices['close'] - trend

    else:
        print("You did not input a valid method!")

    return de_trended


# 3: 1st order Fourier series expansion
def fourier_expansion(x, a0, a1, b1, w):
    """
    Fourier Series expansion function
    :param x: the hours (independent variable)
    :param a0: first fourier coefficient
    :param a1: second fourier coefficient
    :param b1: third fourier coefficient
    :param w: fourier series frequency
    :return: the value of the fourier function
    """

    f = a0 + a1 * np.cos(w * x) + b1 * np.sin(w * x)

    return f


# 4: Sine series expansion
def sine_expansion(x, a0, b1, w):
    """
    Fourier Series expansion function
    :param x: the hours (independent variable)
    :param a0: first sine series coefficient
    :param b1: third sine series coefficient
    :param w: sine series frequency
    :return: the value of the sine series function
    """

    s = a0 + b1 * np.sin(w * x)

    return s


# 5: Fourier series coefficient Calculator function
def fourier_windows(prices, periods, method='difference', plot='True'):
    """

    :param plot: True by def, False if you don't want to plot
    :param prices: OHLC dataframe
    :param periods: list of periods for which to compute coefficients [3, 5, 10, ..]
    :param method: method by which to detrend data
    :return: dict of dataframes containing coefficients for said periods
    """

    results = {}
    storage_data = {}

    # Compute the coefficients of the series
    detrended = deTrend(prices=prices, method=method)

    # Outer loop: loop the periods, for each period get coefficients (periods = windows)
    for i in range(0, len(periods)):
        # List for storing coefficients that we find
        coeffs = []

        # Inner loop: loop through the dataframe
        for j in range(periods[i], len(prices) - periods[i]):
            # We are fitting x and y, where y is the detrended data; so x is irrelevant
            x = np.arange(0, periods[i])
            y = detrended.iloc[j - periods[i]:j]  # shifter through the data

            with warnings.catch_warnings():
                warnings.simplefilter('error', OptimizeWarning)

                try:

                    res = scipy.optimize.curve_fit(fourier_expansion, x, y)

                except(RuntimeError, OptimizeWarning):
                    res = np.empty((1, 4))
                    res[0, :] = np.NAN

            if plot:
                xt = np.linspace(0, periods[i], 100)
                yt = fourier_expansion(x=xt,
                                       a0=res[0][0],
                                       a1=res[0][1],
                                       b1=res[0][2],
                                       w=res[0][3])

                plt.plot(x, y, c='g', label='Detrended series')
                plt.plot(xt, yt, c='r', ls='--', label='Fourier Expansion')
                plt.legend()
                plt.show()

            coeffs = np.append(coeffs, res[0], axis=0)
        warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

        # Reshape data to fit our way
        coeffs = np.array(coeffs).reshape((int(len(coeffs) / 4), 4))

        # Get the dataframe ready
        df = pd.DataFrame(coeffs, index=prices.iloc[periods[i]: -periods[i]])
        df.columns = ['a0', 'a1', 'b1', 'w']
        df = df.fillna(method='bfill')

        # Store in dictionary
        storage_data[periods[i]] = df

    results['coeffs'] = storage_data

    return results


# 6: Sine series coefficient Calculator function
def sine_windows(prices, periods, method='difference', plot='True'):
    """

    :param plot:
    :param prices: OHLC dataframe
    :param periods: list of periods for which to compute coefficients [3, 5, 10, ..]
    :param method: method by which to detrend data
    :return: dict of dataframes containing coefficients for said periods
    """

    results = {}
    storage_data = {}


    # Compute the coefficients of the series
    detrended = deTrend(prices=prices, method=method)

    # Outer loop: loop the periods, for each period get coefficients (periods = windows)
    for i in range(0, len(periods)):
        # List for storing coefficients that we find
        coeffs = []

        # Inner loop: loop through the dataframe
        for j in range(periods[i], len(prices) - periods[i]):
            # We are fitting x and y, where y is the detrended data; so x is irrelevant
            x = np.arange(0, periods[i])
            y = detrended.iloc[j - periods[i]:j]  # shifter through the data

            with warnings.catch_warnings():
                warnings.simplefilter('error', OptimizeWarning)

                try:

                    res = scipy.optimize.curve_fit(sine_expansion, x, y)

                except(RuntimeError, OptimizeWarning):
                    res = np.empty((1, 3))
                    res[0, :] = np.NAN

            if plot:
                xt = np.linspace(0, periods[i], 100)
                yt = sine_expansion(x=xt,
                                    a0=res[0][0],
                                    b1=res[0][1],
                                    w=res[0][2])

                plt.plot(x, y, c='g', label='Detrended series')
                plt.plot(xt, yt, c='b', ls='--', label='Sine Expansion')
                plt.legend()
                plt.show()

            coeffs = np.append(coeffs, res[0], axis=0)
        warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

        # Reshape data to fit our way
        coeffs = np.array(coeffs).reshape((int(len(coeffs) / 3), 3))

        # Get the dataframe ready
        df = pd.DataFrame(coeffs, index=prices.iloc[periods[i]: -periods[i]])
        df.columns = ['a0', 'b1', 'w']
        df = df.fillna(method='bfill')

        # Store in dictionary
        storage_data[periods[i]] = df

    results['coeffs'] = storage_data

    return results
