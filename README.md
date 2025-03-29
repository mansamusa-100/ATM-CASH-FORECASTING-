# ATM-CASH-FORECASTING-

### This project focuses on forecasting the cash demand for ATMs using machine learning techniques. The goal is to predict the optimal cash withdrawal amounts for multiple ATM locations, ensuring efficient cash management and reducing cash shortages or excess reserves.

## Data collection and Processing 
### The dataset contains historical ATM withdrawal transactions with the following features:

date: Date of transaction

atm_location: Specific ATM branch/location

withdrawal_amount: Cash withdrawn on a given day

day, month, year, week_of_year, day_of_week: Time-based features for pattern recognition

## Data Preprocessing 

### Handled missing values by forward-filling missing transactions.

Converted date fields into structured time features.

Encoded categorical variables (ATM locations).

## Machine Learning Model 

### The XGBoost Regressor was chosen due to its efficiency in time-series forecasting. It handles non-linearity well and performs better than traditional models like linear regression.

## Conclusion 

###  This project successfully predicts ATM cash demand using machine learning. It helps banks efficiently manage cash distribution, reducing both shortages and excess reserves.
