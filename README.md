# Stock and Index Beta Calculator #
Python script that calculates the beta (β) of a stock against the chosen index. The script retrieves the data and resamples it to provide the beta for 6 different timeframes and frequencies. The beta is calculated boy using both a formula and linear regression. 
The betas calculated are:
* Monthly 5 Years
* Weekly 5 Years
* Monthly 3 Years
* Weekly 3 Years
* Weekly 1 Year
* Daily 1 Year

## Background ##
The beta of a stock measures the volatility of its price in relation to the market or index. The return on a stock with a beta of 2.0 would generate a return twice that of the market - if the market goes up 2%, the stock price would be expected to increase by 4%. This measure of volatiltiy is also called systematic risk, undiversifiable risk or market risk.
Some major uses of beta are:
* Measuring the risk of a portfolio to the market
* Measuring the volatiltiy of an industry compared to the market
* Estimating the required return on equity of stock in the Capital Asset Pricing Model (CAPM) or Weighted-Average Cost of Captial (WACC)
* Estimating the effects of debt on a company's volatility (beta re-levering)

## Process ##
There are two methods used to calculated beta. 
1. Using the formala, β = Cov(ri, rm)/σ^2m i.e. the covariance between the returns of the stock and the market divided by the volatility of the market.   
2. Running a linear regression of the returns of the market against the returns of the stock, the slope of the regression line is the calculated beta.

The script displays the results from the first method in the console and used the second model to generate graphs.

## Usage ##
The function beta() uses the following paramaters:
Name | Symbol | Description
| :--- | :--: | :----
Stock Ticker | ['ticker1', 'ticker2', ... 'tickern'] | The tickers of the stocks beta is to be calculated for
Index/Market Symbol | market | The symbol of the index beta is to be measured against, S&P500 (^GSPC) by default  
Adjustment | adjusted | The number of times beta will be adjusted (0 by default)

The function retrieves data from yahoo finance using Pandas DataReader, index codes must match the codes on their website (linked below), major codes are listed below.
Country | Major Index | Ticker Suffix
| :--- | :--: | :----
Australia | ^AXJO for ASX200 | .AX, 'CBA.AX'
Canada | ^GSPTSE for S&P/TSX | .TO, 'RY.TO' 
Hong Kong | ^HSI for Hang Sang Index | .HK, '1299.HK'
Japan | ^N225 for Nikkei 225 | .T, '7203.T'
United Kingdom | ^FTSE for FTSE100 | .L, 'ULVR.L'
United States | ^GSPC for S&P500 | N/A, 'AAPL'

List of all indexes: https://finance.yahoo.com/world-indices

Typically beta is adjusted to better estimate the security's future beta. Typically, betas are mean-reverting and will approach to the market value of 1.0 overtime. Typically beta will be adjusted once in practice.

## Required Libraries ##
* datetime
* dateutil
* itertools
* matplotlib
* numpy
* pandas_datareader
* scipy

## Related Projects ##
Binomial Option Pricing Calculator: https://github.com/sammuhrai/binomial_option_pricing_calculator

## Disclaimer ##
Script is for educational purposes and is not to be taken as financial advice.

