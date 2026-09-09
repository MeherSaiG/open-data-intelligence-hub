# ARIMA for Beginners

## 1. What is ARIMA?

**ARIMA** is a statistical model used for **time series forecasting**.

A time series is data collected over time, such as:

- Daily sales
- Monthly electricity usage
- Hourly website traffic
- Weekly product demand
- Yearly revenue

Example:

| Month | Sales |
|---|---:|
| Jan | 120 |
| Feb | 128 |
| Mar | 135 |
| Apr | 142 |
| May | 150 |

The goal of forecasting is to use past values to estimate future values.

For example:

```text
Past sales
120 → 128 → 135 → 142 → 150

ARIMA learns the pattern

            ↓

Forecast
157 → 164 → 170
```

ARIMA stands for:

```text
AR = AutoRegressive
I  = Integrated
MA = Moving Average
```

The model is usually written as:

```text
ARIMA(p, d, q)
```

Where:

- `p` = number of past observations used
- `d` = number of times differencing is applied
- `q` = number of past forecast errors used

---

# 2. Why Do We Need ARIMA?

Suppose a company wants to predict product demand.

Historical demand:

```text
Week 1 → 100
Week 2 → 110
Week 3 → 118
Week 4 → 125
Week 5 → 130
```

The company may want to estimate:

```text
Week 6 → ?
Week 7 → ?
Week 8 → ?
```

Forecasts can help with:

- Inventory planning
- Supply-chain decisions
- Staffing
- Budgeting
- Capacity planning
- Production planning

ARIMA is useful when future values depend strongly on the past behavior of the same time series.

---

# 3. The Three Parts of ARIMA

## AR — AutoRegressive

The **AR** part uses previous values of the time series to predict the next value.

Example:

```text
Yesterday's sales = 100
Today's sales     = 110

Tomorrow's sales may depend on:

Today's sales
Yesterday's sales
Earlier sales
```

A simple AR model may look like:

```text
Future Value =
Constant
+ coefficient × Previous Value
```

For example:

```text
Tomorrow's sales =
10 + 0.9 × Today's sales
```

If today's sales are `100`:

```text
Tomorrow =
10 + 0.9 × 100
= 100
```

---

## What Does `p` Mean?

`p` tells ARIMA how many previous observations should be considered.

### ARIMA(1, d, q)

```text
Use 1 previous value
```

### ARIMA(2, d, q)

```text
Use 2 previous values
```

Example:

```text
t-2       t-1       t
120  →    130  →    ?

p = 2
```

The model considers both `120` and `130`.

---

# 4. I — Integrated

The **I** part refers to **differencing**.

Differencing is used to make a time series more **stationary**.

Before understanding differencing, we need to understand stationarity.

---

# 5. What is Stationarity?

A stationary time series has statistical behavior that remains reasonably stable over time.

For example:

```text
10, 12, 11, 13, 12, 10, 11
```

The values move around roughly the same level.

This is relatively stationary.

But consider:

```text
100, 120, 140, 160, 180, 200
```

This series has a strong upward trend.

It is not stationary.

ARIMA generally works better when the input series is stationary.

---

# 6. What is Differencing?

Differencing calculates the change between consecutive observations.

Suppose:

```text
Original data:

100, 120, 140, 160, 180
```

First difference:

```text
120 - 100 = 20
140 - 120 = 20
160 - 140 = 20
180 - 160 = 20
```

New series:

```text
20, 20, 20, 20
```

The trend has disappeared.

This transformed series is much more stationary.

---

## What Does `d` Mean?

`d` specifies the number of times differencing is applied.

### d = 0

No differencing.

```text
Original series is already stationary
```

### d = 1

Difference once.

```text
Y'(t) = Y(t) - Y(t-1)
```

### d = 2

Difference the already-differenced series again.

Usually:

```text
d = 0, 1, or 2
```

A very large value of `d` is usually unnecessary and may damage the useful signal.

---

# 7. MA — Moving Average

The **MA** part uses previous prediction errors.

Suppose ARIMA predicted:

```text
Predicted sales = 100
Actual sales    = 110
```

Prediction error:

```text
Error = Actual - Predicted

Error = 110 - 100
      = 10
```

The MA component remembers recent forecast errors and uses them to improve future predictions.

---

## What Does `q` Mean?

`q` tells ARIMA how many previous forecast errors to consider.

For example:

```text
q = 1
```

means:

```text
Use the previous prediction error
```

And:

```text
q = 2
```

means:

```text
Use the previous two prediction errors
```

---

# 8. Putting Everything Together

An ARIMA model is written as:

```text
ARIMA(p, d, q)
```

Example:

```text
ARIMA(2, 1, 1)
```

means:

```text
p = 2
Use 2 previous observations

d = 1
Difference the data once

q = 1
Use 1 previous forecast error
```

Diagram:

```text
Raw Time Series
      |
      v
Check Stationarity
      |
      v
Apply Differencing
      |
      v
Use Previous Values
      |
      v
Use Previous Errors
      |
      v
ARIMA Model
      |
      v
Future Forecast
```

---

# 9. Simple Example

Suppose monthly demand is:

| Month | Demand |
|---|---:|
| Jan | 100 |
| Feb | 110 |
| Mar | 121 |
| Apr | 129 |
| May | 140 |
| Jun | 152 |

There is an upward trend.

First difference:

| Month | Difference |
|---|---:|
| Feb | 10 |
| Mar | 11 |
| Apr | 8 |
| May | 11 |
| Jun | 12 |

Now the values are roughly around:

```text
10, 11, 8, 11, 12
```

This is much more stable.

Therefore:

```text
d = 1
```

may be reasonable.

The model can then learn relationships between:

```text
Previous values
+
Previous forecast errors
```

to forecast future demand.

---

# 10. How Do We Choose p, d, and q?

A beginner-friendly process is:

```text
1. Plot the time series
2. Check whether it is stationary
3. Choose d using differencing
4. Use ACF to help choose q
5. Use PACF to help choose p
6. Train multiple candidate models
7. Compare their performance
```

---

# 11. ACF and PACF

## ACF

**ACF = Autocorrelation Function**

It measures how strongly the current value is related to previous values at different lags.

Example:

```text
Today's demand
   |
   +---- relation with yesterday
   |
   +---- relation with 2 days ago
   |
   +---- relation with 3 days ago
```

ACF is commonly used as one clue for choosing `q`.

---

## PACF

**PACF = Partial Autocorrelation Function**

PACF measures the relationship between a value and a particular lag after accounting for intermediate lags.

PACF is commonly used as one clue for choosing `p`.

Simple memory aid:

```text
PACF → p
ACF  → q
```

This is a useful starting rule, not a perfect law.

---

# 12. Installing the Required Libraries

Using pip:

```bash
pip install pandas matplotlib statsmodels scikit-learn
```

Libraries used:

```text
pandas        → data handling
matplotlib    → charts
statsmodels   → ARIMA
scikit-learn  → evaluation metrics
```

---

# 13. Basic ARIMA Example in Python

```python
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

sales = [
    100,
    110,
    121,
    129,
    140,
    152,
    160,
    171,
    180,
    192
]

series = pd.Series(sales)

model = ARIMA(
    series,
    order=(1, 1, 1)
)

model_fit = model.fit()

forecast = model_fit.forecast(steps=3)

print(forecast)
```

Here:

```text
order=(1, 1, 1)

p = 1
d = 1
q = 1
```

And:

```python
forecast(steps=3)
```

asks ARIMA to predict the next 3 periods.

---

# 14. Plotting the Data

```python
import pandas as pd
import matplotlib.pyplot as plt

sales = [
    100,
    110,
    121,
    129,
    140,
    152,
    160,
    171,
    180,
    192
]

series = pd.Series(sales)

plt.plot(series)

plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.show()
```

Always inspect the data visually before fitting a forecasting model.

Look for:

- Trend
- Seasonality
- Sudden spikes
- Missing values
- Outliers
- Structural changes

---

# 15. Checking Stationarity with ADF Test

One common statistical test is the:

**Augmented Dickey-Fuller Test**

Python example:

```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(series)

print("ADF Statistic:", result[0])
print("p-value:", result[1])
```

A common interpretation is:

```text
p-value <= 0.05
→ evidence suggests the series may be stationary

p-value > 0.05
→ evidence is insufficient to call it stationary
```

Do not rely only on the ADF test.

Also inspect:

- The time-series chart
- Trend
- Rolling mean
- Domain behavior
- ACF/PACF

---

# 16. Performing Differencing in Python

```python
differenced = series.diff().dropna()

print(differenced)
```

Example:

```text
Original:

100
110
121
129
140
```

Difference:

```text
10
11
8
11
```

---

# 17. ACF and PACF in Python

```python
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plot_acf(differenced)
plt.show()

plot_pacf(differenced)
plt.show()
```

Use these plots as diagnostic tools rather than mechanically picking values.

---

# 18. Train-Test Split for Time Series

For normal machine learning, data may often be randomly shuffled.

For time series, random shuffling is usually inappropriate because time order matters.

Correct idea:

```text
Past                           Future
|----------------------------|---------|
         Training               Test
```

Example:

```python
train = series.iloc[:-3]
test = series.iloc[-3:]
```

Then:

```python
model = ARIMA(
    train,
    order=(1, 1, 1)
)

model_fit = model.fit()

predictions = model_fit.forecast(
    steps=len(test)
)
```

---

# 19. Evaluate the Forecast

Common forecasting metrics include:

- MAE
- RMSE
- MAPE

---

## MAE

**Mean Absolute Error**

It calculates the average absolute difference between actual and predicted values.

```text
Actual      Predicted      Error

100         105            5
120         118            2
140         135            5
```

MAE:

```text
(5 + 2 + 5) / 3

= 4
```

Smaller is better.

Python:

```python
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(
    test,
    predictions
)

print("MAE:", mae)
```

---

# 20. RMSE

**Root Mean Squared Error**

RMSE penalizes larger errors more heavily than MAE.

Python:

```python
from sklearn.metrics import mean_squared_error

rmse = mean_squared_error(
    test,
    predictions
) ** 0.5

print("RMSE:", rmse)
```

---

# 21. Complete Beginner Example

```python
import pandas as pd

from statsmodels.tsa.arima.model import ARIMA

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


sales = [
    100,
    110,
    121,
    129,
    140,
    152,
    160,
    171,
    180,
    192,
    205,
    215
]


series = pd.Series(sales)


# Keep the last 3 observations for testing
train = series.iloc[:-3]
test = series.iloc[-3:]


# ARIMA(p, d, q)
model = ARIMA(
    train,
    order=(1, 1, 1)
)


model_fit = model.fit()


# Predict the same number of periods as the test set
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

# 22. Forecast Future Values

After selecting a satisfactory model, it can be fitted using the full historical series.

```python
final_model = ARIMA(
    series,
    order=(1, 1, 1)
)

final_model_fit = final_model.fit()

future = final_model_fit.forecast(
    steps=5
)

print(future)
```

This predicts the next 5 time periods.

For monthly data:

```text
5 periods = next 5 months
```

For daily data:

```text
5 periods = next 5 days
```

The meaning of one forecast step depends on the frequency of the input data.

---

# 23. Confidence Intervals

A forecast is uncertain.

Instead of reporting only:

```text
Next month's demand = 220
```

it is better to include an uncertainty range when possible:

```text
Forecast = 220

Likely range:
205 to 235
```

Example:

```python
forecast_result = model_fit.get_forecast(
    steps=3
)

predicted_mean = forecast_result.predicted_mean

confidence_interval = forecast_result.conf_int()

print(predicted_mean)
print(confidence_interval)
```

---

# 24. ARIMA vs SARIMA

ARIMA handles:

```text
Trend
Autocorrelation
Historical errors
```

But ordinary ARIMA does not explicitly model repeating seasonal structure.

Example:

```text
Ice cream sales

Every summer → high
Every winter → low
```

For seasonal data, use:

```text
SARIMA
```

SARIMA stands for:

**Seasonal AutoRegressive Integrated Moving Average**

It is commonly written as:

```text
SARIMA(p, d, q)(P, D, Q, s)
```

where `s` is the seasonal period.

Examples:

```text
Monthly data with yearly seasonality:

s = 12
```

```text
Daily data with weekly seasonality:

s = 7
```

---

# 25. ARIMA vs Other Forecasting Models

| Model | Good For |
|---|---|
| Naive Forecast | Baseline comparison |
| Moving Average | Simple smoothing |
| Exponential Smoothing | Trend and seasonality |
| ARIMA | Non-seasonal time-series relationships |
| SARIMA | Seasonal time series |
| Prophet | Business-oriented trend/seasonal forecasting |
| LSTM | Complex nonlinear sequential patterns |
| XGBoost | Forecasting with engineered features and external variables |

Do not automatically choose the most complex model.

Always compare against a simple baseline.

---

# 26. When ARIMA Works Well

ARIMA can work well when:

- Data is collected regularly
- Historical values are informative
- The series can be made stationary
- The relationship is mostly linear
- There is sufficient historical data
- There are no extremely complicated seasonal patterns
- External variables are not the main drivers

---

# 27. When ARIMA May Not Be Ideal

ARIMA may be less suitable when:

- The data has strong seasonality not modeled explicitly
- Many external variables influence the result
- Relationships are highly nonlinear
- The series changes behavior suddenly
- There is very little historical data
- There are many missing observations
- Multiple interacting time series must be modeled together

Possible alternatives include:

```text
SARIMA
SARIMAX
Exponential Smoothing
Prophet
XGBoost
LSTM
Temporal Fusion Transformer
```

depending on the problem.

---

# 28. ARIMA vs SARIMAX

**SARIMAX** extends SARIMA and can include external variables.

Example:

Product demand may depend on:

```text
Past demand
+
Price
+
Discount
+
Holiday
+
Temperature
```

Ordinary ARIMA mainly uses the history of the target series.

SARIMAX can incorporate additional explanatory features.

---

# 29. Common Beginner Mistakes

## Mistake 1 — Ignoring Stationarity

Training ARIMA directly on a strongly trending series without investigating stationarity can lead to poor modeling.

---

## Mistake 2 — Randomly Splitting the Data

Wrong:

```text
Random train-test split
```

Better:

```text
Earlier periods → training
Later periods   → testing
```

---

## Mistake 3 — Choosing p, d, q Randomly

Use:

- Data visualization
- Stationarity checks
- Differencing
- ACF
- PACF
- AIC/BIC
- Validation performance

---

## Mistake 4 — Over-Differencing

Too much differencing may remove useful information.

Try small values such as:

```text
d = 0
d = 1
d = 2
```

and validate the result.

---

## Mistake 5 — Ignoring Seasonality

If sales increase every December, ordinary ARIMA may not fully represent that pattern.

Consider:

```text
SARIMA
```

---

## Mistake 6 — Evaluating Only Training Accuracy

A model must forecast unseen future periods well.

Always keep a test period or use time-series cross-validation.

---

# 30. What is AIC?

**AIC = Akaike Information Criterion**

It helps compare candidate statistical models.

Example:

```text
ARIMA(1,1,1) → AIC = 210

ARIMA(2,1,1) → AIC = 198

ARIMA(3,1,2) → AIC = 201
```

Lower AIC is usually preferred among comparable models.

However:

```text
Do not select a model using AIC alone.
```

Also consider:

- Forecast accuracy
- Residual behavior
- Simplicity
- Domain knowledge

---

# 31. Trying Multiple ARIMA Models

Example:

```python
orders = [
    (0, 1, 1),
    (1, 1, 0),
    (1, 1, 1),
    (2, 1, 1),
    (2, 1, 2),
]

for order in orders:

    model = ARIMA(
        train,
        order=order
    )

    fitted_model = model.fit()

    print(
        order,
        fitted_model.aic
    )
```

This can help compare several candidate models.

---

# 32. Residuals

Residuals are:

```text
Actual Value - Predicted Value
```

A good forecasting model should leave residuals that look approximately random.

Example of a healthy residual sequence:

```text
+2
-1
+1
-3
+2
0
-1
```

A suspicious residual pattern:

```text
+10
+11
+12
+13
+14
```

The second pattern suggests the model is consistently missing something.

---

# 33. Full ARIMA Workflow

```text
Collect Time-Series Data
          |
          v
Clean Missing / Invalid Data
          |
          v
Plot the Series
          |
          v
Check Trend and Seasonality
          |
          v
Check Stationarity
          |
          v
Difference if Required
          |
          v
Inspect ACF and PACF
          |
          v
Choose Candidate p, d, q
          |
          v
Split Data by Time
          |
          v
Train ARIMA
          |
          v
Forecast Test Period
          |
          v
Evaluate MAE / RMSE / MAPE
          |
          v
Inspect Residuals
          |
          v
Compare Candidate Models
          |
          v
Train Final Model
          |
          v
Forecast Future Values
          |
          v
Monitor Forecast Accuracy
```

---

# 34. Supply-Chain Example

Imagine a warehouse has weekly demand:

```text
Week 1   520
Week 2   540
Week 3   550
Week 4   570
Week 5   590
Week 6   610
```

The data engineer may:

```text
1. Collect historical demand
2. Clean missing records
3. Aggregate transactions weekly
4. Store the time series
5. Check data quality
6. Train candidate ARIMA models
7. Evaluate them
8. Produce future demand forecasts
9. Send forecasts to planning systems
```

The business team can use these predictions to decide:

- How much inventory to order
- How much warehouse capacity is needed
- How many trucks may be required
- Whether stock shortages are likely

---

# 35. Role of a Data Engineer in Forecasting

A data engineer does not always build the final forecasting algorithm.

However, data engineers are critical because forecasting depends on good data.

Typical responsibilities include:

```text
Source Systems
      |
      v
Data Ingestion
      |
      v
Data Cleaning
      |
      v
Time-Series Aggregation
      |
      v
Data Quality Checks
      |
      v
Feature / Forecast Dataset
      |
      v
ML / Forecasting Pipeline
      |
      v
Forecast Output
      |
      v
Dashboard / API / Planning System
```

The data engineer may be responsible for:

- Reliable data pipelines
- Correct timestamps
- Missing data handling
- Duplicate prevention
- Data aggregation
- Feature pipelines
- Scheduling
- Data storage
- Monitoring
- Forecast output delivery

---

# 36. Important Time-Series Terms

| Term | Meaning |
|---|---|
| Time Series | Data ordered by time |
| Observation | One recorded value |
| Lag | Previous time step |
| Trend | Long-term upward or downward movement |
| Seasonality | Repeating pattern |
| Stationarity | Stable statistical behavior over time |
| Differencing | Subtracting consecutive values |
| Forecast | Prediction of future values |
| Residual | Difference between actual and predicted |
| ACF | Correlation with previous lags |
| PACF | Direct correlation with a lag |
| MAE | Mean Absolute Error |
| RMSE | Root Mean Squared Error |
| AIC | Model-comparison criterion |

---

# 37. Easy Way to Remember ARIMA

Remember:

```text
ARIMA = Past Values + Differencing + Past Errors
```

Or:

```text
AR
Look at previous values

I
Remove trend using differencing

MA
Look at previous forecast errors
```

And:

```text
ARIMA(p, d, q)

p → Past observations
d → Differencing
q → Past errors
```

---

# 38. Quick Cheat Sheet

```text
ARIMA
AutoRegressive Integrated Moving Average

ARIMA(p,d,q)

p = AR order
d = number of differences
q = MA order
```

Common workflow:

```text
Plot
↓
Check stationarity
↓
Difference
↓
ACF/PACF
↓
Choose p,d,q
↓
Train
↓
Forecast
↓
Evaluate
```

Useful Python class:

```python
from statsmodels.tsa.arima.model import ARIMA
```

Train:

```python
model = ARIMA(
    train,
    order=(1, 1, 1)
)

model_fit = model.fit()
```

Forecast:

```python
forecast = model_fit.forecast(
    steps=3
)
```

---

# 39. Final Summary

ARIMA is one of the classic time-series forecasting models.

It combines three ideas:

```text
AR → learn from previous observations

I  → make the series more stationary using differencing

MA → learn from previous prediction errors
```

The model is represented as:

```text
ARIMA(p, d, q)
```

A practical modeling process is:

```text
Understand the data
        ↓
Check stationarity
        ↓
Apply differencing
        ↓
Use ACF/PACF
        ↓
Train candidate models
        ↓
Evaluate on future periods
        ↓
Inspect residuals
        ↓
Select the best reasonable model
        ↓
Forecast future values
```

For beginners, the most important idea is not memorizing equations.

The important idea is understanding:

> ARIMA studies patterns in past values and past forecasting errors after making the time series sufficiently stable for modeling.
