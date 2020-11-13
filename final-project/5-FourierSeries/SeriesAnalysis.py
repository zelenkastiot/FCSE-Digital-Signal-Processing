"""

 Created on 11-Nov-20
 @author: Kiril Zelenkovski

 Fourier series an attempt to measure the relative vibration
 parameters of a price series. Including frequency, amplitude,
 phase angle, etc ...

"""

# Import modules
import pandas as pd
import plotly.graph_objs as go
from plotly import subplots
from plotly.offline import plot
from feature_functions import *

df = pd.read_csv('../Data/EURUSD_hours.csv')

# Rename columns
df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

# Fix dates
df['date'] = pd.to_datetime(df['date'], format="%d.%m.%Y %H:%M:%S.%f")

# Set index column
df = df.set_index(df['date'])

# Clean duplicates
df = df.drop_duplicates(keep=False)


# Fourier expansion fit
f = fourier_windows(prices=df[:500],
                    periods=[10, 15],
                    method='difference',
                    plot=True)
print(f['coeffs'])
print(f['coeffs'][10])
print(f['coeffs'][15])

# Sine expansion fit
s = sine_windows(prices=df[:500],
                 periods=[10, 15],
                 method='difference',
                 plot=True)

print(s['coeffs'])
print(s['coeffs'][10])
print(s['coeffs'][15])
