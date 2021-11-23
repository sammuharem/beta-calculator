import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from scipy import stats
from dateutil.relativedelta import relativedelta
from itertools import cycle

def downloadData(ticker):
    start, end = datetime.datetime.now() - relativedelta(years=5), datetime.datetime.now()
    data = web.DataReader(ticker, 'yahoo', start, end)
    data.reset_index(inplace=True)
    data.set_index("Date", inplace=True)
    return data

def processBeta(stockData, marketData, year, frequency, adjustment = 0):
    stockData, marketData = shortenData(stockData, marketData, year)
    stockData = stockData['Adj Close'].resample(frequency).last().pct_change()
    marketData = marketData['Adj Close'].resample(frequency).last().pct_change()
    stockData = stockData[stockData.index.isin(marketData.index)]
    marketData = marketData[marketData.index.isin(stockData.index)]        
    beta = calculateBeta(stockData, marketData)
    regressionData = stats.linregress(marketData[1:], stockData[1:])
    return adjustBeta(beta, adjustment), marketData, stockData, regressionData

def shortenData(stockData, marketData, year):
    if year == 5:
        return stockData, marketData
    array1 = stockData.index > datetime.datetime.now() - relativedelta(years=year)
    array2 = marketData.index > datetime.datetime.now() - relativedelta(years=year)
    stockData = stockData[[x for x in array1]]
    marketData = marketData[[x for x in array2]]
    return stockData, marketData

def calculateBeta(stockData, marketData):
    covariance = np.cov(stockData[1:], marketData[1:])
    variance = np.var(marketData[1:])
    return covariance[0,1] / variance
 
def adjustBeta(beta, adjustment):
    for i in range(adjustment):
        beta = 0.67 * beta + 0.33
    return beta

def subPlot(title, x1, y1, colour, rD1, i):
    plots = {1:321, 2:322, 3:323, 4:324, 5:325, 6:326}
    ax = plt.subplot(plots[i])
    ax.title.set_text(title)
    ax.scatter(x1, y1, color = colour)
    ax.plot(x1, [rD1[0] * i + rD1[1] for i in x1])
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

def beta(tickers, adjusted = 0, market = '^GSPC'):
    colours = cycle(['b','g','r','c','m','y'])
    market = downloadData(market)
    for ticker in tickers:
        stock = downloadData(ticker)
        beta1m5y, y1, x1, rD1 = processBeta(stock, market, 5, '1M', adjusted)
        beta1m3y, y2, x2, rD2 = processBeta(stock, market, 3, '1M', adjusted)
        beta1w5y, y3, x3, rD3 = processBeta(stock, market, 5, '1W', adjusted)
        beta1w3y, y4, x4, rD4 = processBeta(stock, market, 3, '1W', adjusted)
        beta1w1y, y5, x5, rD5 = processBeta(stock, market, 1, '1W', adjusted)
        beta1d1y, y6, x6, rD6 = processBeta(stock, market, 1, '1D', adjusted)
        
        fig = plt.figure()
        fig.set_size_inches(12.5, 10)
        colour = next(colours)
        subPlot('Monthly 5 Years', x1, y1, colour, rD1, 1)
        subPlot('Weekly 5 Years', x2, y2, colour, rD2, 2)
        subPlot('Weekly 5 Years', x3, y3, colour, rD3, 3)     
        subPlot('Weekly 3 Years', x4, y4, colour, rD4, 4)    
        subPlot('Weekly 1 Year', x5, y5, colour, rD5, 5)
        subPlot('Daily 1 Year', x6, y6, colour, rD6, 6)
        
        plt.suptitle(f"{ticker} Beta", y = 1.02, x = 0.52)
        plt.gcf().text(0, 0.41, 'Stock Returns (%)', fontsize=14, rotation = 'vertical')
        plt.gcf().text(0.44, 0, 'Market Returns (%)', fontsize=14)
        plt.tight_layout()
        plt.show()
        
        print(f'''{ticker} Betas:\nMonthly 5 Years {beta1m5y}\nMonthly 3 Years {beta1m3y}
Weekly  5 Years {beta1w5y}\nWeekly  3 Years {beta1w3y}\nWeekly  1 Year  {beta1w1y}
Daily   1 Year  {beta1d1y}''')
