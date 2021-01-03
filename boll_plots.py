import pandas as pd
import requests
import matplotlib.pyplot as plt
from secrets import IEX_CLOUD_API_TOKEN_SANDBOX


def get_historical_prices(date_range, stock_symbol, api_token, sandbox=False):
    """
    Pulls historical stock prices for specified stock from IEX Cloud API
    :param date_range: timeframe for Bollinger plots (options: 3m,6m,1y,2y,5y,max; see docs for more)
    :param stock_symbol: ticker symbol for security (e.g. 'aapl' for Apple Inc.)
    :param api_token: IEX cloud API token
    :param sandbox: bool for whether IEX sandbox testing api to be used.
    :return: python list of dictionaries containing historical stock data
    """
    if sandbox:
        request_url = f'https://sandbox.iexapis.com/stable/stock/{stock_symbol}/chart/{date_range}?token={api_token}'
        return requests.get(request_url).json()
    else:
        request_url = f'https://cloud.iexapis.com/stable/stock/{stock_symbol}/chart/{date_range}?token={api_token}'
        return requests.get(request_url).json()


def hist_prices_to_df(data):
    """
    Converts passed-in data to pandas dataframe.
    NB df['date'] hard coded => reflects historical data format provided by IEX Cloud API
    :param data: python list containing stock data to be converted to dataframe
    :return: pandas dataframe of passed-in data
    """
    df = pd.DataFrame(data)
    index = pd.to_datetime(df['date'])
    df.set_index(index, inplace=True)
    return df


def add_bollinger_bands_to_df(df):
    """
    Helper function to add necessary columns to df required to plot bollinger bands.
    :param df: pandas dataframe
    :return: same dataframe passed in but which columns for bollinger bands added
    """
    df['close: 20 day mean'] = df['close'].rolling(20).mean()
    df['upper'] = df['close: 20 day mean'] + 2 * (df['close'].rolling(20).std())
    df['lower'] = df['close: 20 day mean'] - 2 * (df['close'].rolling(20).std())
    return df


def plot_bollinger_bands(df):
    """
    Helper function that actually plots the bollinger bands
    :param df: pandas dataframe
    :return: None
    """
    df[['close', 'close: 20 day mean', 'upper', 'lower']].plot(figsize=(12, 8))
    plt.xlabel('Date')
    plt.title(f'1y Bollinger Bands plot: {symbol.upper()}')
    plt.tight_layout()
    plt.show()
    return


if __name__ == '__main__':
    symbol = input('Company: ')
    historical_prices = get_historical_prices('1y', symbol, IEX_CLOUD_API_TOKEN_SANDBOX, sandbox=True)
    dataframe = hist_prices_to_df(historical_prices)
    add_bollinger_bands_to_df(dataframe)
    plot_bollinger_bands(dataframe)
