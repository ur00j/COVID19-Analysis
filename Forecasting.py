import pandas as pd

# Sample DataFrame
data = {
    'DATE': pd.date_range(start='2022-01-01', periods=100),
    'CASES': [100 + i*5 for i in range(100)]  
}

df = pd.DataFrame(data)
df.set_index('DATE', inplace=True)
print(df.head())

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['CASES'], label='Daily Cases')
plt.xlabel('Date')
plt.ylabel('Number of Cases')
plt.title('Daily Infection Rates')
plt.legend()
plt.show()

from statsmodels.tsa.seasonal import seasonal_decompose

result = seasonal_decompose(df['CASES'], model='additive', period=7)  
result.plot()
plt.show()

from fbprophet import Prophet

# Prepare data for Prophet
prophet_df = df.reset_index()
prophet_df.columns = ['ds', 'y']

# Initialize and fit the model
model = Prophet(daily_seasonality=True)
model.fit(prophet_df)

# Make future predictions
future = model.make_future_dataframe(periods=30)  # Forecasting 30 days into the future
forecast = model.predict(future)

# Plot the results
fig = model.plot(forecast)
plt.show()

from statsmodels.tsa.arima.model import ARIMA

# Fit the ARIMA model
model = ARIMA(df['CASES'], order=(5, 1, 0))  # Adjust the order based on ACF/PACF plots
model_fit = model.fit()

# Forecast future values
forecast = model_fit.forecast(steps=30)
forecast_index = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=30)

forecast_df = pd.DataFrame(forecast, index=forecast_index, columns=['Forecast'])

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['CASES'], label='Historical Data')
plt.plot(forecast_df.index, forecast_df['Forecast'], color='red', linestyle='--', label='Forecast')
plt.xlabel('Date')
plt.ylabel('Number of Cases')
plt.title('Infection Rate Forecast')
plt.legend()
plt.show()

from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Actual values (assuming you have actual future data for evaluation)
actual_values = [100 + i*6 for i in range(30)]  # Example future data
predicted_values = forecast

mae = mean_absolute_error(actual_values, predicted_values)
mse = mean_squared_error(actual_values, predicted_values)
rmse = np.sqrt(mse)

print(f'MAE: {mae}')
print(f'MSE: {mse}')
print(f'RMSE: {rmse}')
