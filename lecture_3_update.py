#################################################
#          Import Basic Libraries
#################################################
#import wrds
import os 
import sys
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
import importlib as imp
from scipy import linalg
import statsmodels.api as sm
import math
from time import sleep
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 15)    



#################################################
#         Generate quotation table
#################################################
# Import specific library

# pip install yfinance
import yfinance as yf
import pytz

# Show how the syntax works
def get_exchange_rate(base_currency, target_currency, date):
    pair = f"{base_currency}{target_currency}=X"
    data = yf.Ticker(pair)
    next_day = (pd.Timestamp(date) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
    # Setting start and end dates to the specified date to get data for that date only
    history = data.history(start=date, end=next_day)
    # Check if the data exists for the specified date
    if not history.empty:
        return history["Close"].iloc[0]
    else:
        print(f"No data available for {date}.")
        # note that there is no exchange rate for same currency, we use 1 to denote that
        return 1

# Usage
date = "2024-08-23"
base_currency = 'USD'
target_currency = 'EUR'
exchange_rate = get_exchange_rate(base_currency, target_currency, date)
print(exchange_rate)



# Generate quotation table
basic_info = [["EUR", "Euro - Used in countries such as Germany, France, Italy, Spain, etc."],\
["JPY", "Japanese Yen - Used in Japan."],\
["GBP", "British Pound - Used in the United Kingdom."],\
["CHF", "Swiss Franc - Used in Switzerland."],\
["CNY", "Chinese Yuan - Used in China."],\
["USD", "United States Dollar - Used in USA."]]


quotes = pd.DataFrame(basic_info)
quotes.columns = ["Symbol","Intro"]
for col in ["Indirect Quote", "Direct Quote"]:
    quotes[col] = math.nan


for i in range(len(quotes)):
    try:
        base_currency = 'USD'
        target_currency = quotes["Symbol"].iloc[i]
        exchange_rate = get_exchange_rate(base_currency, target_currency, date)
        quotes["Indirect Quote"].iloc[i] = "{:.4f}".format(exchange_rate)
        quotes["Direct Quote"].iloc[i] = "{:.4f}".format(1/exchange_rate)
    except:
        if base_currency == target_currency:
            quotes["Indirect Quote"].iloc[i] = 1
            quotes["Direct Quote"].iloc[i] = 1
            

# Export to csv
quotes.to_csv("Quotation Table" + ".csv", encoding = 'utf-8-sig', index = False)
#################################################
#         Triangular arbitrage
#################################################
# Import specific library
from itertools import combinations

# Generate all combinations of two currencies
all_currency_list = quotes["Symbol"].to_list()
pairs = list(combinations(all_currency_list,2))
triangular = pd.DataFrame(columns = ["Pair", "Market Quote"], index = range(len(pairs)))
for col in all_currency_list:
    triangular["via " + col] = math.nan

# note that there is no exchange rate for same currency, we use 1 to denote that
# we can ignore the errors
for i in range(len(pairs)):
    try:
        base_currency = pairs[i][0]
        target_currency = pairs[i][1]
        exchange_rate = get_exchange_rate(base_currency, target_currency, date)
        triangular["Pair"].iloc[i] = base_currency + " to " + target_currency
        triangular["Market Quote"].iloc[i] = "{:.4f}".format(exchange_rate)

        for third_currency in all_currency_list:
            first_convert_rate = get_exchange_rate(base_currency, third_currency, date)
            second_convert_rate = get_exchange_rate(third_currency, target_currency, date)
            triangular["via " + third_currency].iloc[i] = "{:.4f}".format(first_convert_rate * second_convert_rate)
        #print(i)
    except:
        None


# Export to csv
triangular.to_csv("Triangular Arbitrage" + ".csv", encoding = 'utf-8-sig', index = False)

    



