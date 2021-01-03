import pandas as pd
import requests
from secrets import IEX_CLOUD_API_TOKEN_SANDBOX

symbol = input('Company: ')

# requests and df operations to get revenue and net income
request_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/financials/?period=annual&last=5&token={IEX_CLOUD_API_TOKEN_SANDBOX}'

data = requests.get(request_url).json()
data['financials'].reverse()

annual_revenues = []
annual_net_incomes = []

for year in data['financials']:
    annual_revenues.append(year['revenue'])
    annual_net_incomes.append(year['netIncome'])

dates = pd.to_datetime(['2016', '2017', '2018', '2019', '2020'])

final_dataframe = pd.DataFrame(columns=dates.to_period('A'))
final_dataframe.loc['Revenue'] = annual_revenues
final_dataframe.loc['Revenue % chg. yoy'] = final_dataframe.loc['Revenue'].pct_change() * 100

final_dataframe.loc['Net Income'] = annual_net_incomes
final_dataframe.loc['Net Income % chg. yoy'] = final_dataframe.loc['Net Income'].pct_change() * 100
final_dataframe.fillna(value='n/a', inplace=True)

print(final_dataframe.head())


# add data from IEX 'advanced fundamentals' endpoint to final_dataframe
# ==> P/E ratios
request_url_fundamentals = f'https://sandbox.iexapis.com/stable/time-series/fundamentals/{symbol}/annual/?last=5&token={IEX_CLOUD_API_TOKEN_SANDBOX}'
fundamentals_data = requests.get(request_url_fundamentals).json()
fundamentals_data.reverse()

pe_multiples = []

for year in fundamentals_data:
    pe_multiples.append(year['pricePerEarnings'])

final_dataframe.loc['P/E'] = pe_multiples

print(final_dataframe.head())


# stock summary df
request_url_adv_stats = f'https://sandbox.iexapis.com/stable/stock/{symbol}/advanced-stats/annual/?token={IEX_CLOUD_API_TOKEN_SANDBOX}'
adv_stats_data = requests.get(request_url_adv_stats).json()

stock_summary_df = pd.DataFrame([adv_stats_data['marketcap'], adv_stats_data['totalRevenue'],
                                 adv_stats_data['week52high'], adv_stats_data['week52highDate'],
                                 adv_stats_data['week52low'], adv_stats_data['week52lowDate'],
                                 pe_multiples[-1], adv_stats_data['priceToBook'],
                                 adv_stats_data['dividendYield'], adv_stats_data['year1ChangePercent']*100
                                ],
                                columns=[f'{symbol.upper()} Summary'],
                                index=['Market cap (USD)', 'Revenue (USD)', '52-week high', '52-week high date',
                                      '52-week low', '52-week low date', 'P/E', 'P/B', 'Dividend yield %', '1-year price change %'])



print(stock_summary_df)
