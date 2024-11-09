import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch stock data from Yahoo Finance
def get_stock_data(tickers, period="1y"):
    """
    Download stock data for a given list of tickers and time period.
    If any tickers fail to download, they will be skipped.
    """
    try:
        data = yf.download(tickers, period=period)
        return data['Adj Close']  # Adjusted closing price
    except Exception as e:
        print(f"Error downloading data for {tickers}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of failure

# Function to calculate performance based on percentage change
def calculate_performance(stocks):
    """
    Calculate percentage performance over the selected period.
    Handle cases where there may not be enough data.
    """
    if stocks.empty:
        return pd.Series()  # Return an empty series if there is no data
    try:
        performance = (stocks.iloc[-1] - stocks.iloc[0]) / stocks.iloc[0] * 100  # Percentage change
        return performance
    except IndexError as e:
        print(f"Error calculating performance: {e}")
        return pd.Series()  # Return an empty series in case of an error

# Function to visualize stock performance
def plot_performance(sector_name, performance):
    """
    Plot performance for a sector's stocks.
    Skip plotting if no performance data is available.
    """
    if performance.empty:
        print(f"No data to plot for {sector_name}")
        return
    performance.plot(kind='bar')
    plt.title(f"{sector_name} Sector Performance")
    plt.ylabel("Performance (%)")
    plt.show()

# Updated list of sectors and JSE stock tickers
sectors = {
    "Financials": ["ABG.JO", "FSR.JO", "NED.JO", "SBK.JO", "OMU.JO"],
    "Industrials": ["SOL.JO", "BVT.JO", "SHP.JO", "APN.JO"],
    "Resources": ["AGL.JO", "AMS.JO", "IMP.JO", "ANG.JO", "SOL.JO"],
    "Technology": ["NPN.JO", "DGH.JO"],
    "Consumer Goods": ["BTI.JO", "SAB.JO", "WHL.JO", "TRU.JO"],
    "Telecommunications": ["MTN.JO", "VOD.JO"],
    "Real Estate": ["RDF.JO", "GRT.JO", "EPP.JO"],
    "Utilities": ["CIL.JO", "PPC.JO"],
    "Energy": ["TGA.JO", "SOL.JO"],
    "Consumer Services": ["CLS.JO", "MRP.JO", "TBS.JO"]
}

# To store sector performances for comparison
sector_performances = {}

# Loop through sectors and calculate performance
for sector, tickers in sectors.items():
    print(f"Processing sector: {sector}")
    
    # Fetch stock data
    stock_data = get_stock_data(" ".join(tickers), period="6mo")
    
    # Calculate performance for each stock in the sector
    performance = calculate_performance(stock_data)
    
    # Store the average performance for the sector
    if not performance.empty:
        sector_avg_performance = performance.mean()  # Calculate average performance of the sector
        sector_performances[sector] = sector_avg_performance  # Store sector performance
        print(f"{sector} average performance: {sector_avg_performance:.2f}%")
    else:
        print(f"No performance data available for {sector}")

# Rank sectors by performance (best to worst)
sorted_sectors = sorted(sector_performances.items(), key=lambda x: x[1], reverse=True)

# Display the best and worst performing sectors
best_sector = sorted_sectors[0][0]
worst_sector = sorted_sectors[-1][0]

print(f"\nBest Performing Sector: {best_sector} with an average performance of {sorted_sectors[0][1]:.2f}%")
print(f"Worst Performing Sector: {worst_sector} with an average performance of {sorted_sectors[-1][1]:.2f}%")

# Show top 3 sectors and bottom 3 sectors
print("\nTop 3 Sectors:")
for sector, perf in sorted_sectors[:3]:
    print(f"{sector}: {perf:.2f}%")

print("\nBottom 3 Sectors:")
for sector, perf in sorted_sectors[-3:]:
    print(f"{sector}: {perf:.2f}%")

# Drill down into the best and worst-performing sectors

print(f"\nDrilling down into best performing sector: {best_sector}")
best_sector_data = get_stock_data(" ".join(sectors[best_sector]), period="6mo")
best_sector_performance = calculate_performance(best_sector_data)
print(f"{best_sector} stock performance:\n", best_sector_performance)

plot_performance(best_sector, best_sector_performance)

print(f"\nDrilling down into worst performing sector: {worst_sector}")
worst_sector_data = get_stock_data(" ".join(sectors[worst_sector]), period="6mo")
worst_sector_performance = calculate_performance(worst_sector_data)
print(f"{worst_sector} stock performance:\n", worst_sector_performance)

plot_performance(worst_sector, worst_sector_performance)




