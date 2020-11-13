"""

 Created on 13-Nov-20
 @author: Kiril Zelenkovski

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

df = pd.read_csv("../Data/EURUSD_hours.csv")

# Rename columns
df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

# Fix dates
df['date'] = pd.to_datetime(df['date'], format="%d.%m.%Y %H:%M:%S.%f")

# Set index column
df = df.set_index(df['date'])

# Clean duplicates
df = df.drop_duplicates(keep=False)

mpf.plot(df,
         type='ohlc',
         tight_layout=False,
         axtitle='OHLC: EUR/USD, Jan-2017 : May-2017')

mpf.plot(df,
         type='ohlc',
         mav=4,
         tight_layout=False,
         axtitle='OHLC plot: MAV 4 hours EUR/USD, Jan-2017 : May-2017')

mpf.plot(df,
         type='candle',
         mav=(3, 6, 9),
         volume=True,
         tight_layout=False,
         axtitle='Candlestick plot: EUR/USD, Jan-2017 : May-2017')

mpf.plot(df,
         type='candle',
         mav=(3, 6, 9),
         volume=True,
         show_nontrading=True,
         tight_layout=False,
         axtitle='Candlestick plot: Non-trading days EUR/USD, Jan-2017 : May-2017')
