import subprocess
import sys
import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()
DELAY = 30  # seconds
api_key = os.getenv("COINGECKO_API_KEY")

API_URL = "https://api.coingecko.com/api/v3/simple/price?" #ids=bitcoin,dogecoin&vs_currencies=usd,cad

if len(sys.argv) != 2:
    print("Usage: python crypto_fetcher.py <processor>")
    sys.exit(1)

analyzer = sys.argv[1]

coins = [] #exists

if __name__ == "__main__":
    currency= input("Enter currency (usd/cad): ").strip().lower()
    if currency not in ['usd', 'cad']:
        print("Invalid currency. Please enter 'usd' or 'cad'.")
        sys.exit(1)
    # find coins, check if they exist in coingecko
    try:
        with open('coins.txt', 'r') as file:
            check_coins = []
            for line in file:
                check_coins.append(line.strip())

        coin_ids = ",".join(check_coins)
        response_1 = requests.get(f'{API_URL}ids={coin_ids}&vs_currencies={currency}&api_key={api_key}')

        if response_1.status_code != 200:
            print("Error fetching data from CoinGecko API:", response_1.status_code)
            sys.exit(1)

        price_data_1 = response_1.json()

    except FileNotFoundError:
        print("Error: coins.txt file not found.")
        sys.exit(1)

    valid_coins = list(price_data_1.keys())
    invalid_coins = set(check_coins) - set(valid_coins)

    if len(valid_coins)==0:
        print("No valid coins found. Exiting.")
        sys.exit(1)

    if invalid_coins:
        print("The following coins are invalid and will be ignored:", ", ".join(invalid_coins))

    print("Valid coins:")
    print(*valid_coins, sep=", ",end="\n")
    #print("fetched prices: ", json.dumps(price_data_1, indent=2))

    while (True):
    
        response_2 = requests.get(f'{API_URL}ids={",".join(valid_coins)}&vs_currencies={currency}&api_key={api_key}')
        price_data_2 = response_2.json()
        if response_2.status_code == 429:
            print("Rate limit exceeded. Waiting for 60 seconds before retrying...") #hard coded wait
            time.sleep(60)
            continue
        if response_2.status_code != 200:
            print("Error fetching data from CoinGecko API:", response_2.status_code)
            continue
        #print("fetched prices: ", json.dumps(price_data_2, indent=2))

        #call cpp analyzer

        output_data = ""
        for coin in valid_coins:
            initial_price = price_data_1[coin][currency]
            latest_price = price_data_2[coin][currency]
            output_data += f"{coin} {initial_price} {latest_price}\n"

        try:
            result = subprocess.run([analyzer], input=output_data, text=True, capture_output=True)
            print("Analyzed data:\n" + result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error executing analyzer:", e)
            sys.exit(1)
        
        print("-"*40)
        print(f"Waiting {DELAY} seconds before next fetch...\n")
        print("Time is:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        time.sleep(DELAY)  # wait for DELAY seconds before next fetch

        

    
