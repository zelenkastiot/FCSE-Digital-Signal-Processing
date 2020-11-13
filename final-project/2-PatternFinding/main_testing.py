"""

 Created on 11-Nov-20
 @author: Kiril Zelenkovski

"""
from analysis_functions import *


if __name__ == "__main__":
    # Read dataset
    data = pd.read_csv('data/EURUSD_2017-2020.csv')

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
    err_allowed = 10.0 / 100

    # # If Error allowed =5% - finds 51 patterns
    # err_allowed = 5.0 / 100

    # Total patterns
    total = 0

    # Loop dataset
    for i in tqdm(range(100, len(price))):
        # Pips
        pips = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        # Get parameters from peak detection function
        current_idx, current_pattern, start, end = peak_detect(price.values[:i])

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
            total += 1
            for j in range(0, len(harmonics)):

                if harmonics[j] == 1 or harmonics[j] == -1:
                    # Bearish / Bullish
                    sense = 'Bearish ' if harmonics[j] == -1 else 'Bullish '
                    # Classic / Butterfly / Bat / Crab
                    label = f'{total}: ' + sense + labels[j] + ' Found (+24h)'

                    plt.title(label)
                    plt.plot(np.arange(start, i + 24), price.values[start:i + 24])
                    plt.plot(current_idx, current_pattern, c='r')
                    plt.show()

                    # Long trade
                    if harmonics[j] == 1:
                        pips += 1000 * (price[end + 1:end + 25] - price[end])

                    # Short trade
                    elif harmonics[j] == -1:
                        pips += 1000 * (price[end] - price[end + 1:end + 25])

                    plt.clf()

                    label2 = label + "; Earnings (pips)"
                    plt.title(label2)
                    plt.bar(np.arange(1, 25), pips, color=(0.2, 0.4, 0.6, 0.6))
                    plt.draw()
                    plt.pause(0.09)

print(f'Total number of patterns found from EUR/USD 2017-2020 dataset: {total}')
