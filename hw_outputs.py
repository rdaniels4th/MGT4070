import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Fetch historical monthly data for the USD/EUR exchange rate for the past 5 years
def get_historical_exchange_rates(base_currency, target_currency, period='5y'):
    pair = f"{base_currency}{target_currency}=X"
    ticker = yf.Ticker(pair)
    data = ticker.history(period=period, interval='1mo')  # Fetch monthly data
    return data['Close']

# (1) Get the historical monthly spot rates
base_currency = 'USD'
target_currency = 'EUR'
spot_rates = get_historical_exchange_rates(base_currency, target_currency)

# Plot the historical spot rates
plt.figure(figsize=(10, 6))
plt.plot(spot_rates.index, spot_rates.values, marker='o', linestyle='-')
plt.title(f"Historical Monthly Spot Rates for {base_currency}/{target_currency} (Past 5 Years)")
plt.xlabel("Date")
plt.ylabel("Spot Rate (USD/EUR)")
plt.grid(True)
plt.show()

# (2) Compute the rate of return for the spot rate series
# Percentage return = (current rate - previous rate) / previous rate
rate_of_return = spot_rates.pct_change().dropna()

# Plot the rate of return
plt.figure(figsize=(10, 6))
plt.plot(rate_of_return.index, rate_of_return.values, marker='o', linestyle='-', color='green')
plt.title(f"Rate of Return for {base_currency}/{target_currency} Spot Rates (Past 5 Years)")
plt.xlabel("Date")
plt.ylabel("Rate of Return")
plt.grid(True)
plt.show()
