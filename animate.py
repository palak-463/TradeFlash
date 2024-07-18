#This is the code for showing crypto data in candlechart without using flask

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import requests
from datetime import datetime, timedelta


# Function to fetch cryptocurrency data
def fetch_crypto_data(crypto_id):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)

    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days=1'
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching data")
        return None

    return response.json()


def plot_candlestick(data):
    data['date'] = mdates.date2num(data.index)
    new_data = data[['date', 'open', 'high', 'low', 'close']].values

    fig, ax = plt.subplots()
    candlestick_ohlc(ax, new_data, width=0.0005, colorup='#53c156', colordown='#ff1717')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.title('Candlestick chart')
    plt.xticks(rotation=45)
    plt.show()


def main():
    crypto_id = input('Enter the cryptocurrency ID (e.g., "bitcoin"): ')

    data = fetch_crypto_data(crypto_id)

    if data is not None:
        # Convert data to DataFrame
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        # Create OHLC data
        ohlc_data = df['price'].resample('1H').ohlc()

        plot_candlestick(ohlc_data)


if __name__ == "__main__":
    main()
