# AI/ML Interview Questions: Regression

## 1. What is regression in machine learning, and when is it used?
Regression is a supervised learning algorithm used to predict continuous numerical values such as house prices, salaries, and temperatures.

## 2. What is the difference between simple linear regression and multiple linear regression?
Simple linear regression uses one independent variable, while multiple linear regression uses two or more independent variables to predict the target.

## 3. What assumptions are made by linear regression?
- Linear relationship
- Independent observations
- Constant variance of errors
- Normally distributed errors
- No multicollinearity

## 4. What is the difference between a dependent variable and an independent variable?
The dependent variable is the output to be predicted, while independent variables are the input features used for prediction.

## 5. What do the slope and intercept represent in a linear regression model?
The slope shows how much the dependent variable changes for one unit increase in the independent variable. The intercept is the predicted value when the independent variable is zero.

## 6. What is the purpose of the cost function in regression?
The cost function measures the prediction error and helps the model find the best-fit parameters by minimizing that error.

## 7. What is Mean Squared Error (MSE), and why is it commonly used?
MSE is the average of squared differences between actual and predicted values. It is widely used because it penalizes large errors more heavily.

## 8. What is the difference between MAE, MSE, and RMSE?
- MAE: Average absolute error.
- MSE: Average squared error.
- RMSE: Square root of MSE and is in the same unit as the target variable.

## 9. What is the R-squared score, and how should it be interpreted?
R-squared measures how well the model explains the variation in the target variable. A value closer to 1 indicates better performance.

## 10. What is adjusted R-squared, and why is it useful?
Adjusted R-squared considers both model accuracy and the number of features, preventing unnecessary variables from improving the score.

## 11. What is overfitting in a regression model?
Overfitting occurs when the model learns the training data too well, including noise, resulting in poor performance on new data.

## 12. What is underfitting in a regression model?
Underfitting occurs when the model is too simple to capture the data pattern, leading to poor performance.

## 13. What is multicollinearity, and how does it affect regression?
Multicollinearity occurs when independent variables are highly correlated. It makes coefficient estimates unstable and difficult to interpret.

## 14. How can multicollinearity be detected?
It can be detected using a Correlation Matrix or Variance Inflation Factor (VIF).

## 15. What is regularization, and why is it used?
Regularization adds a penalty to the model to reduce overfitting and improve generalization.

## 16. What is the difference between Ridge, Lasso, and Elastic Net regression?
- Ridge uses L2 regularization.
- Lasso uses L1 regularization and performs feature selection.
- Elastic Net combines both L1 and L2 regularization.

## 17. How does Lasso regression perform feature selection?
Lasso sets the coefficients of less important features to zero, effectively removing them from the model.

## 18. What is polynomial regression?
Polynomial regression models nonlinear relationships by adding polynomial terms such as x² and x³.

## 19. How do outliers affect a regression model?
Outliers can significantly influence the regression line, reducing model accuracy and increasing prediction error.

## 20. How would you evaluate the performance of a regression model?
Regression models are evaluated using MAE, MSE, RMSE, R-squared, Adjusted R-squared, and residual analysis.
