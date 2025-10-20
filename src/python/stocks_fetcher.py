import subprocess
import sys
import requests
import os
import json
import time
from dotenv import load_dotenv

#load environment variables
load_dotenv()
DELAY = 60  # seconds - increased to avoid rate limiting (5 calls/min = need 12s between calls, 3 stocks = 36s + buffer)
api_key = os.getenv("ALPHAVANTAGE_API_KEY")

API_URL = "https://www.alphavantage.co/query?" # function = GLOBAL_QUOTE & symbol = <symbol>& apikey=<api_key>
EXCHANGE_RATE_URL = "https://api.exchangerate-api.com/v4/latest/USD"
exchange_rate = requests.get(EXCHANGE_RATE_URL).json()['rates']['CAD']

#check cmd line args
if len(sys.argv) != 2:
    print("Usage: python stocks_fetcher.py <processor>")
    sys.exit(1)

analyzer = sys.argv[1]

stocks = [] #exists

if __name__ == "__main__":
    """ fetch stock prices from AlphaVantage API with rate limit handling"""
    def fetch_stocks(stocklist):
        price_data = {}
        for stock in stocklist:
            response = requests.get(f'{API_URL}function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}')
            time.sleep(13)  # Increased to 13 seconds to stay under 5 calls/minute (60s / 5 calls = 12s minimum)
            if response.status_code == 429:
                print("Rate limit exceeded. Waiting for 60 seconds before retrying...") #hard coded wait
                time.sleep(60)
                # Retry after waiting
                response = requests.get(f'{API_URL}function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}')
            
            if response.status_code != 200:
                print(f"Error fetching data for {stock} from Alpha Vantage API: {response.status_code}")
                continue  # Skip this stock instead of exiting
            
            #extract price from response
            price_str = response.json().get("Global Quote", {}).get("05. price")
            if price_str and price_str != "0":
                price_data[stock] = float(price_str)  # Convert to float
            else:
                print(f"No valid price data for {stock}")
        return price_data

    # set currency preference from user
    currency= input("Enter currency (usd/cad): ").strip().lower()
    if currency not in ['usd', 'cad']:
        print("Invalid currency. Please enter 'usd' or 'cad'.")
        sys.exit(1)

    # find stocks, check if they exist in alphavantage
    # read stock symbols, fetch initial prices
    try:
        with open('data/stocks.txt', 'r') as file:
            check_stocks = []
            for line in file:
                check_stocks.append(line.strip())

        stock_ids = ",".join(check_stocks)

        price_data_1 = fetch_stocks(check_stocks)
    except FileNotFoundError:
        print("Error: stocks.txt file not found.")
        sys.exit(1)

# validate stocks
    valid_stocks = list(price_data_1.keys())
    invalid_stocks = set(check_stocks) - set(valid_stocks)

    if len(valid_stocks)==0:
        print("No valid stocks found. Exiting.")
        sys.exit(1)

    if invalid_stocks:
        print("The following stocks are invalid and will be ignored:", ", ".join(invalid_stocks))

    print("Valid stocks:")
    print(*valid_stocks, sep=", ",end="\n")
    #print("fetched prices: ", json.dumps(price_data_1, indent=2))


# main loop
# fetches prices and analyzes with cpp processor
    price_data_2 = {}
    while (True):
        
        if not price_data_2:  # First run - fetch initial data, same as 1
            price_data_2 = price_data_1
        else:  # Subsequent runs, fetch updated prices
            price_data_2 = fetch_stocks(valid_stocks)
            
        #print("fetched prices: ", json.dumps(price_data_2, indent=2))

        #call cpp analyzer
        output_data = ""
        for stock in valid_stocks:
            if stock not in price_data_2:
                print(f"Skipping {stock} - no current price data")
                continue
                
            initial_price = float(price_data_1[stock])
            latest_price = float(price_data_2[stock])
            
            # Convert to CAD if needed
            if currency == 'cad':
                initial_price *= exchange_rate
                latest_price *= exchange_rate
            
            output_data += f"{stock} {initial_price} {latest_price}\n"


         # call cpp analyzer
        try:
            result = subprocess.run([analyzer], input=output_data, text=True, capture_output=True)
            print("Analyzed data:\n" + result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error executing analyzer:", e)
            sys.exit(1)
        
        print("-"*40)
        print(f"Waiting {DELAY} seconds before next fetch...\n")
        print("Time is:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("Press Ctrl+C to stop.")
        time.sleep(DELAY)  # wait for DELAY seconds before next fetch

        

