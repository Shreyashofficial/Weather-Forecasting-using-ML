##let’s start this task by importing the necessary Python libraries and the dataset we need:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

#importing data set

data = pd.read_csv('DailyDelhiClimateTest.csv')

## Let’s have a look at the descriptive statistics of this data before moving forward:
print(data.head())
print(data.describe())
print(data.info())

# The date column in this dataset is not having a datetime data type. We will change it when required.
#Let’s have a look at the mean temperature in Delhi over the years:
figure = px.line(data, x="date",
                 y="meantemp",
                 title='Mean Temperature in Delhi Over the Years')
figure.show()

#Now let’s have a look at the humidity in Delhi over the years:
figure = px.line(data, x="date",
                 y="humidity",
                 title='Humidity in Delhi Over the Years')
figure.show()

#wind speed in Delhi over the years:
figure = px.line(data, x="date",
                 y="wind_speed",
                 title='Wind Speed in Delhi Over the Years')
figure.show()

## outcome conclusion :-- Till 2015, the wind speed was higher during monsoons (August & September) and retreating monsoons (December & January). After 2015, 
#there were no anomalies in wind speed during monsoons.


#Now let’s have a look at the relationship between temperature and humidity:
figure = px.scatter(data_frame = data, x="humidity",
                    y="meantemp", size="meantemp",
                    trendline="ols",
                    title = "Relationship Between Temperature and Humidity")
figure.show()
#conclusion:--- There’s a negative correlation between temperature and humidity in Delhi. It means higher temperature results in low humidity
#and lower temperature results in high humidity.

# Now let’s analyze the temperature change in Delhi over the years. For this task, I will first convert the data type of the date column into datetime.
# Then I will add two new columns in the dataset for year and month values.

data["date"] = pd.to_datetime(data["date"], format = '%Y-%m-%d')
data['year'] = data['date'].dt.year
data["month"] = data["date"].dt.month
print(data.head())


#Now let’s have a look at the temperature change in Delhi over the years:
plt.style.use('fivethirtyeight')
plt.figure(figsize=(15, 10))
plt.title("Temperature Change in Delhi Over the Years")
sns.lineplot(data = data, x='month', y='meantemp', hue='year')
plt.show()

#The Facebook prophet model is one of the best techniques for time series forecasting.

#The prophet model accepts time data named as “ds”, and labels as “y”. So let’s convert the data into this format:

forecast_data = data.rename(columns = {"date": "ds",
                                       "meantemp": "y"})
print(forecast_data)

model = Prophet()
model.fit(forecast_data)
forecasts = model.make_future_dataframe(periods=365)
predictions = model.predict(forecasts)
plot_plotly(model, predictions)
