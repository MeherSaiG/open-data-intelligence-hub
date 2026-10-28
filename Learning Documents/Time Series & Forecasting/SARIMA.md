# SARIMA for Beginners

## 1. What is SARIMA?

**SARIMA** is a statistical time-series forecasting model used when data has:

- Trend
- Autocorrelation
- Forecast errors
- **Seasonality**

SARIMA stands for:

```text
Seasonal
AutoRegressive
Integrated
Moving Average
```

It extends ARIMA by adding a seasonal component.

A SARIMA model is usually written as:

```text
SARIMA(p, d, q)(P, D, Q, s)
```

There are two groups of parameters:

```text
Non-seasonal part:
(p, d, q)

Seasonal part:
(P, D, Q, s)
```

---

# 2. Why Do We Need SARIMA?

ARIMA is useful when a time series has trend and autocorrelation.

But many real-world datasets also have repeating seasonal patterns.

Examples:

- Ice cream sales increase every summer
- Retail sales increase every December
- Electricity demand changes by season
- Hotel bookings rise during holiday periods
- Website traffic may change by weekday
- Taxi demand may repeat by hour or day

Example:

```text
Jan   100
Feb   110
Mar   120
...
Dec   200

Next Jan   105
Next Feb   115
Next Mar   125
```

The pattern repeats every year.

This is called:

```text
Seasonality
```

SARIMA is designed to model this kind of repeating pattern.

---

# 3. ARIMA vs SARIMA

ARIMA:

```text
ARIMA(p, d, q)
```

SARIMA:

```text
SARIMA(p, d, q)(P, D, Q, s)
```

SARIMA adds:

```text
P = Seasonal AutoRegressive order
D = Seasonal differencing order
Q = Seasonal Moving Average order
s = Seasonal period
```

Simple comparison:

| Model | Handles Trend | Handles Autocorrelation | Handles Seasonality |
|---|---|---|---|
| ARIMA | Yes | Yes | Not explicitly |
| SARIMA | Yes | Yes | Yes |

---

# 4. Understanding Seasonality

Seasonality is a repeating pattern at a fixed interval.

Example: monthly sales.

```text
Year 1:

Jan   100
Feb   120
Mar   130
...
Dec   220

Year 2:

Jan   105
Feb   125
Mar   135
...
Dec   230
```

The values are different, but the overall pattern repeats every 12 months.

Therefore:

```text
s = 12
```

because the seasonal cycle is 12 months long.

---

# 5. What Does s Mean?

`s` is the number of observations in one seasonal cycle.

Examples:

## Monthly data with yearly seasonality

```text
s = 12
```

because one year contains 12 months.

---

## Daily data with weekly seasonality

```text
s = 7
```

because one week contains 7 days.

---

## Quarterly data with yearly seasonality

```text
s = 4
```

because one year contains 4 quarters.

---

## Hourly data with daily seasonality

```text
s = 24
```

because one day contains 24 hours.

---

## Weekly data with yearly seasonality

Approximately:

```text
s = 52
```

---

# 6. SARIMA Parameters

SARIMA is written as:

```text
SARIMA(p, d, q)(P, D, Q, s)
```

Let's break it down.

---

# 7. Non-Seasonal Parameters

## p — AutoRegressive Order

`p` tells the model how many recent previous observations to use.

Example:

```text
p = 2
```

means the model may use:

```text
t-1
t-2
```

to help predict:

```text
t
```

---

## d — Differencing Order

`d` controls regular differencing.

Example:

```text
100, 120, 140, 160
```

First difference:

```text
20, 20, 20
```

If one differencing step is used:

```text
d = 1
```

---

## q — Moving Average Order

`q` tells the model how many previous forecast errors to use.

Example:

```text
q = 1
```

means:

```text
Use the previous forecast error
```

---

# 8. Seasonal Parameters

## P — Seasonal AutoRegressive Order

`P` is similar to `p`, but it looks at seasonal lags.

Suppose monthly sales have yearly seasonality:

```text
s = 12
```

Then:

```text
P = 1
```

means the model can use the value from:

```text
12 months ago
```

to help predict the current value.

Example:

```text
Jan 2025 → 100

Jan 2026 → ?
```

The previous January may help predict the next January.

---

# 9. D — Seasonal Differencing

`D` removes repeating seasonal patterns.

Regular differencing compares:

```text
Current value - Previous value
```

Seasonal differencing compares:

```text
Current value - Value one season ago
```

For monthly data with:

```text
s = 12
```

seasonal differencing is:

```text
Current month
-
Same month last year
```

Example:

```text
Jan 2025 = 100
Jan 2026 = 120
```

Seasonal difference:

```text
120 - 100 = 20
```

If seasonal differencing is applied once:

```text
D = 1
```

---

# 10. Q — Seasonal Moving Average Order

`Q` uses previous forecast errors at seasonal intervals.

For:

```text
Q = 1
s = 12
```

the model may use the error from:

```text
12 periods ago
```

to help improve the current forecast.

---

# 11. Full Example of SARIMA Parameters

Suppose we use:

```text
SARIMA(1,1,1)(1,1,1,12)
```

This means:

## Non-seasonal

```text
p = 1
Use 1 recent previous value

d = 1
Difference once

q = 1
Use 1 recent forecast error
```

## Seasonal

```text
P = 1
Use 1 seasonal lag

D = 1
Apply seasonal differencing once

Q = 1
Use 1 seasonal forecast error

s = 12
Season repeats every 12 observations
```

---

# 12. Visual Understanding

```text
Raw Time Series
      |
      v
Trend?
      |
      +---- Yes → Regular Differencing
      |
      v
Seasonality?
      |
      +---- Yes → Seasonal Differencing
      |
      v
Recent Lags
      |
      v
Seasonal Lags
      |
      v
Recent Forecast Errors
      |
      v
Seasonal Forecast Errors
      |
      v
SARIMA Model
      |
      v
Future Forecast
```

---

# 13. Example Dataset

Suppose monthly product demand is:

| Month | Demand |
|---|---:|
| Jan 2025 | 100 |
| Feb 2025 | 110 |
| Mar 2025 | 120 |
| Apr 2025 | 130 |
| May 2025 | 150 |
| Jun 2025 | 180 |
| Jul 2025 | 200 |
| Aug 2025 | 190 |
| Sep 2025 | 160 |
| Oct 2025 | 140 |
| Nov 2025 | 130 |
| Dec 2025 | 220 |
| Jan 2026 | 110 |
| Feb 2026 | 120 |
| Mar 2026 | 130 |

There is a clear yearly seasonal cycle.

So:

```text
s = 12
```

may be appropriate.

---

# 14. Installing Required Libraries

```bash
pip install pandas matplotlib statsmodels scikit-learn
```

Libraries:

```text
pandas
→ data handling

matplotlib
→ charts

statsmodels
→ SARIMA implementation

scikit-learn
→ evaluation metrics
```

---

# 15. SARIMA in Python

In `statsmodels`, SARIMA is commonly implemented using:

```python
SARIMAX
```

Import:

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX
```

Even if you are not using external variables, `SARIMAX` can be used to build a SARIMA model.

---

# 16. Basic SARIMA Example

```python
import pandas as pd

from statsmodels.tsa.statespace.sarimax import SARIMAX


sales = [
    100, 110, 120, 130,
    150, 180, 200, 190,
    160, 140, 130, 220,

    110, 120, 130, 140,
    160, 190, 210, 200,
    170, 150, 140, 230
]


series = pd.Series(sales)


model = SARIMAX(
    series,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12)
)


model_fit = model.fit()


forecast = model_fit.forecast(
    steps=3
)


print(forecast)
```

Here:

```text
order=(1,1,1)
```

represents:

```text
p = 1
d = 1
q = 1
```

And:

```text
seasonal_order=(1,1,1,12)
```

represents:

```text
P = 1
D = 1
Q = 1
s = 12
```

---

# 17. Plotting the Time Series

```python
import matplotlib.pyplot as plt

plt.plot(series)

plt.title("Monthly Product Demand")
plt.xlabel("Month")
plt.ylabel("Demand")

plt.show()
```

Before choosing SARIMA, visually inspect the series.

Look for:

- Trend
- Repeating patterns
- Sudden spikes
- Missing values
- Outliers
- Structural changes

---

# 18. Why Seasonal Differencing Helps

Suppose:

```text
Jan 2025 = 100
Jan 2026 = 110
Jan 2027 = 120
```

There may be a repeated January pattern plus a gradual upward trend.

Seasonal differencing:

```text
Jan 2026 - Jan 2025
= 110 - 100
= 10
```

```text
Jan 2027 - Jan 2026
= 120 - 110
= 10
```

The seasonal structure becomes easier to model.

---

# 19. Regular vs Seasonal Differencing

Regular differencing:

```text
Y(t) - Y(t-1)
```

Seasonal differencing:

```text
Y(t) - Y(t-s)
```

Example:

For monthly data:

```text
s = 12
```

Regular differencing:

```text
Feb - Jan
```

Seasonal differencing:

```text
Jan 2026 - Jan 2025
```

---

# 20. Train-Test Split

Time series should generally preserve time order.

Correct idea:

```text
Past                         Future
|--------------------------|--------|
         Training             Test
```

Example:

```python
train = series.iloc[:-4]
test = series.iloc[-4:]
```

Do not randomly shuffle time-series observations for a normal forecasting split.

---

# 21. Train SARIMA on Training Data

```python
model = SARIMAX(
    train,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12)
)

model_fit = model.fit()

predictions = model_fit.forecast(
    steps=len(test)
)
```

---

# 22. Evaluate the Forecast

Common metrics include:

- MAE
- RMSE
- MAPE

---

## MAE

**Mean Absolute Error**

Example:

```python
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(
    test,
    predictions
)

print("MAE:", mae)
```

Lower is better.

---

# 23. RMSE

**Root Mean Squared Error**

```python
from sklearn.metrics import mean_squared_error

rmse = mean_squared_error(
    test,
    predictions
) ** 0.5

print("RMSE:", rmse)
```

RMSE penalizes large errors more strongly than MAE.

---

# 24. MAPE

**Mean Absolute Percentage Error**

A simplified form is:

```text
Absolute Error
--------------
Actual Value

× 100
```

Example:

```text
Actual = 100
Predicted = 90

Error = 10

MAPE contribution = 10%
```

Be careful when actual values are zero or near zero.

---

# 25. Full Beginner Example

```python
import pandas as pd

from statsmodels.tsa.statespace.sarimax import SARIMAX

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


sales = [
    100, 110, 120, 130,
    150, 180, 200, 190,
    160, 140, 130, 220,

    110, 120, 130, 140,
    160, 190, 210, 200,
    170, 150, 140, 230,

    120, 130, 140, 150,
    170, 200, 220, 210,
    180, 160, 150, 240
]


series = pd.Series(sales)


# Keep the final 6 observations for testing
train = series.iloc[:-6]
test = series.iloc[-6:]


model = SARIMAX(
    train,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12)
)


model_fit = model.fit(
    disp=False
)


predictions = model_fit.forecast(
    steps=len(test)
)


mae = mean_absolute_error(
    test,
    predictions
)


rmse = mean_squared_error(
    test,
    predictions
) ** 0.5


print("Actual:")
print(test)

print()

print("Predictions:")
print(predictions)

print()

print("MAE:", mae)
print("RMSE:", rmse)
```

---

# 26. Forecast Future Values

After selecting the model, fit it to all available historical data.

```python
final_model = SARIMAX(
    series,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12)
)

final_fit = final_model.fit(
    disp=False
)

future = final_fit.forecast(
    steps=6
)

print(future)
```

For monthly data:

```text
steps = 6
```

means:

```text
Forecast the next 6 months
```

---

# 27. Confidence Intervals

Forecasts should include uncertainty where possible.

Instead of saying:

```text
Expected demand = 250
```

you may say:

```text
Forecast = 250

Likely range:
230 to 270
```

Python:

```python
forecast_result = model_fit.get_forecast(
    steps=6
)

predicted_mean = forecast_result.predicted_mean

confidence_interval = forecast_result.conf_int()

print(predicted_mean)
print(confidence_interval)
```

---

# 28. Choosing p, d, q, P, D, Q

A beginner-friendly process:

```text
1. Plot the data
2. Identify trend
3. Identify seasonality
4. Choose s
5. Apply regular differencing if needed
6. Apply seasonal differencing if needed
7. Inspect ACF
8. Inspect PACF
9. Try small candidate values
10. Compare models
11. Evaluate on future data
```

---

# 29. Choosing s

This is usually based on domain knowledge.

Examples:

| Data Frequency | Seasonal Pattern | s |
|---|---|---:|
| Monthly | Yearly | 12 |
| Quarterly | Yearly | 4 |
| Daily | Weekly | 7 |
| Hourly | Daily | 24 |
| Weekly | Yearly | ~52 |

Do not choose `s` randomly.

---

# 30. ACF and PACF

ACF:

```text
Autocorrelation Function
```

PACF:

```text
Partial Autocorrelation Function
```

Beginner memory aid:

```text
PACF → p
ACF  → q
```

Seasonal spikes may also provide clues for:

```text
P
Q
```

For example, a strong correlation around lag 12 in monthly data may indicate a seasonal relationship.

---

# 31. Plot ACF and PACF

```python
import matplotlib.pyplot as plt

from statsmodels.graphics.tsaplots import (
    plot_acf,
    plot_pacf
)


plot_acf(series)
plt.show()


plot_pacf(series)
plt.show()
```

For seasonal data, inspect important seasonal lags such as:

```text
12
24
36
```

for monthly yearly-seasonal data.

---

# 32. AIC for Model Comparison

**AIC = Akaike Information Criterion**

Example:

```text
SARIMA(1,1,1)(1,1,1,12)
AIC = 200

SARIMA(2,1,1)(1,1,1,12)
AIC = 190

SARIMA(1,1,2)(1,1,1,12)
AIC = 195
```

Lower AIC is often preferred among comparable models.

However:

```text
Do not use AIC alone.
```

Also consider:

- Forecast accuracy
- Residual diagnostics
- Simplicity
- Business meaning

---

# 33. Trying Multiple Models

```python
orders = [
    (0, 1, 1),
    (1, 1, 0),
    (1, 1, 1),
    (2, 1, 1),
]

seasonal_orders = [
    (0, 1, 1, 12),
    (1, 1, 0, 12),
    (1, 1, 1, 12),
]

for order in orders:

    for seasonal_order in seasonal_orders:

        model = SARIMAX(
            train,
            order=order,
            seasonal_order=seasonal_order
        )

        fitted = model.fit(
            disp=False
        )

        print(
            order,
            seasonal_order,
            fitted.aic
        )
```

This is a simple manual search.

---

# 34. Why Small Parameter Values Are Better Initially

Beginners sometimes try:

```text
SARIMA(5,2,5)(4,2,4,12)
```

without justification.

This may lead to:

- Slow training
- Overfitting
- Unstable estimates
- Convergence warnings

Start with smaller values such as:

```text
0
1
2
```

and compare results.

---

# 35. Residuals

Residuals are:

```text
Actual - Predicted
```

Ideally, residuals should look approximately random.

Good:

```text
+2
-1
0
+3
-2
+1
```

Suspicious:

```text
+10
+12
+15
+18
+20
```

A clear residual pattern suggests the model has missed useful structure.

---

# 36. Residual Diagnostics

Statsmodels provides useful diagnostic plots:

```python
model_fit.plot_diagnostics()
```

These plots can help inspect:

- Residual distribution
- Autocorrelation
- Normality
- Remaining patterns

A good model should not leave strong systematic autocorrelation in residuals.

---

# 37. SARIMA vs SARIMAX

SARIMA models:

```text
Past target values
+
Seasonality
+
Past errors
```

SARIMAX adds:

```text
External variables
```

Example:

Demand might depend on:

```text
Past demand
+
Price
+
Promotion
+
Holiday
+
Weather
```

The external variables are called:

```text
Exogenous variables
```

---

# 38. Simple SARIMAX Example

```python
model = SARIMAX(
    y,
    exog=X,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12)
)

model_fit = model.fit()
```

Where:

```text
y
=
target time series

X
=
external variables
```

---

# 39. ARIMA vs SARIMA vs SARIMAX

| Model | Trend | Seasonality | External Variables |
|---|---|---|---|
| ARIMA | Yes | No explicit seasonal component | No |
| SARIMA | Yes | Yes | No |
| SARIMAX | Yes | Yes | Yes |

---

# 40. When SARIMA Works Well

SARIMA can work well when:

- Data is regularly spaced
- Seasonality repeats at a known interval
- Historical values are informative
- Seasonal patterns are reasonably stable
- The relationship is mostly linear
- Enough seasonal cycles are available

Example:

For monthly yearly-seasonal data, it is better to have several years of history than only one year.

---

# 41. When SARIMA May Not Be Ideal

SARIMA may struggle when:

- Seasonality changes constantly
- Relationships are highly nonlinear
- Many external variables drive the target
- There are multiple seasonal cycles
- The series has sudden structural changes
- There is very little historical data
- Seasonal patterns are irregular

Possible alternatives include:

```text
SARIMAX
Exponential Smoothing
Prophet
XGBoost
LightGBM
LSTM
Temporal Fusion Transformer
```

depending on the use case.

---

# 42. Common Beginner Mistakes

## Mistake 1 — Wrong Seasonal Period

Wrong:

```text
Monthly data with yearly seasonality

s = 7
```

Better:

```text
s = 12
```

---

## Mistake 2 — Assuming Every Dataset Is Seasonal

Do not use SARIMA only because it is more advanced.

If there is no meaningful seasonality, ARIMA may be sufficient.

---

## Mistake 3 — Using Too Little Historical Data

If:

```text
s = 12
```

but you only have 12 observations, the model has seen only one seasonal cycle.

More cycles are usually better.

---

## Mistake 4 — Over-Differencing

Using too much:

```text
d
D
```

can remove useful information.

Start small.

---

## Mistake 5 — Random Train-Test Split

Time order matters.

Use:

```text
Past → Train
Future → Test
```

---

## Mistake 6 — Ignoring Residuals

A low MAE is useful, but residuals should also be checked for systematic patterns.

---

## Mistake 7 — Ignoring External Drivers

If demand is mostly controlled by:

```text
Price
Promotion
Weather
Holiday
```

ordinary SARIMA may be insufficient.

Consider:

```text
SARIMAX
```

---

# 43. Supply-Chain Example

Suppose monthly demand for a product is:

```text
January     Low
February    Low
March       Medium
April       Medium
May         High
June        High
July        High
August      High
September   Medium
October     Medium
November    High
December    Very High
```

This pattern repeats yearly.

A possible model could be:

```text
SARIMA(1,1,1)(1,1,1,12)
```

The model uses:

```text
Recent demand
+
Recent changes
+
Recent forecast errors
+
Demand from previous years
+
Seasonal differences
+
Seasonal forecast errors
```

to estimate future demand.

---

# 44. Role of Data Engineers

In a production forecasting system:

```text
Source Systems
      |
      v
Data Ingestion
      |
      v
Cleaning
      |
      v
Timestamp Validation
      |
      v
Aggregation
      |
      v
Seasonal Time-Series Dataset
      |
      v
SARIMA / Forecasting Model
      |
      v
Forecast Output
      |
      v
API / Dashboard / Planning System
```

Data engineers may help with:

- Data ingestion
- Correct timestamps
- Handling missing dates
- Aggregating data
- Data-quality validation
- Storing model inputs
- Scheduling forecast jobs
- Delivering outputs
- Monitoring pipelines

---

# 45. Complete SARIMA Workflow

```text
Collect Time-Series Data
          |
          v
Clean Data
          |
          v
Set Correct Time Frequency
          |
          v
Plot the Series
          |
          v
Identify Trend
          |
          v
Identify Seasonality
          |
          v
Choose Seasonal Period s
          |
          v
Check Stationarity
          |
          v
Apply Regular Differencing
          |
          v
Apply Seasonal Differencing
          |
          v
Inspect ACF / PACF
          |
          v
Choose Candidate Parameters
          |
          v
Split Train / Test by Time
          |
          v
Train SARIMA
          |
          v
Forecast Test Period
          |
          v
Evaluate MAE / RMSE / MAPE
          |
          v
Check Residuals
          |
          v
Compare Candidate Models
          |
          v
Train Final Model
          |
          v
Forecast Future Values
```

---

# 46. Easy Way to Remember SARIMA

Remember:

```text
ARIMA
+
Seasonality
=
SARIMA
```

ARIMA:

```text
(p, d, q)
```

Seasonal part:

```text
(P, D, Q, s)
```

Easy memory:

```text
p → recent past values

d → regular differencing

q → recent past errors


P → seasonal past values

D → seasonal differencing

Q → seasonal past errors

s → length of seasonal cycle
```

---

# 47. Quick Cheat Sheet

```text
SARIMA
Seasonal AutoRegressive Integrated Moving Average
```

Model form:

```text
SARIMA(p,d,q)(P,D,Q,s)
```

Meaning:

```text
p = non-seasonal AR order
d = non-seasonal differencing
q = non-seasonal MA order

P = seasonal AR order
D = seasonal differencing
Q = seasonal MA order

s = seasonal period
```

Typical examples:

```text
Monthly + yearly seasonality
s = 12

Daily + weekly seasonality
s = 7

Hourly + daily seasonality
s = 24
```

Python:

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX
```

Model:

```python
model = SARIMAX(
    train,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12)
)
```

Train:

```python
model_fit = model.fit(
    disp=False
)
```

Forecast:

```python
forecast = model_fit.forecast(
    steps=6
)
```

---

# 48. Final Summary

SARIMA is an extension of ARIMA designed for seasonal time series.

It combines:

```text
Recent past values
+
Regular differencing
+
Recent forecast errors
+
Seasonal past values
+
Seasonal differencing
+
Seasonal forecast errors
```

The model is written as:

```text
SARIMA(p, d, q)(P, D, Q, s)
```

The most important beginner concept is:

```text
ARIMA
models regular time-series behavior.

SARIMA
models regular behavior
+
repeating seasonal behavior.
```

A practical process is:

```text
Understand the data
        ↓
Find the seasonal cycle
        ↓
Choose s
        ↓
Check trend and stationarity
        ↓
Difference if required
        ↓
Try small SARIMA models
        ↓
Evaluate on future data
        ↓
Inspect residuals
        ↓
Choose the best reasonable model
        ↓
Forecast future periods
```

For beginners, focus first on understanding:

> SARIMA learns both recent time-series behavior and patterns that repeat after a fixed seasonal interval.
