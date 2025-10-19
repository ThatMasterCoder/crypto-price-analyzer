# Crypto & Stock Price Analyzer

A cross-language price monitoring system that fetches cryptocurrency and stock prices using Python and analyzes price changes using C++.

## Features

- **Real-time price monitoring** for cryptocurrencies and stocks
- **Multi-currency support** (USD/CAD)
- **C++ analysis engine** for fast price change calculations
- **Rate limiting** to respect API constraints
- **Interactive CLI** to choose between crypto or stock tracking

## Project Structure

```
crypto-price-analyzer/
├── src/
│   ├── cpp/
│   │   └── analyzer.cpp       # C++ price analysis engine
│   └── python/
│       ├── crypto_fetcher.py  # Cryptocurrency data fetcher (CoinGecko API)
│       └── stocks_fetcher.py  # Stock data fetcher (Alpha Vantage API)
├── data/
│   ├── coins.txt              # List of cryptocurrencies to track
│   └── stocks.txt             # List of stock symbols to track
├── output/                    # Compiled executables
├── run.ps1                    # Main execution script (PowerShell)
├── requirements.txt           # Python dependencies
└── .env                       # API keys (create this yourself)
```

## Prerequisites

### Required Software
- **Python 3.8+** 
- **C++ Compiler** (g++ / MinGW for Windows)
- **PowerShell** (Windows only - currently no Linux/macOS support)

### API Keys
You'll need free API keys from:
- **CoinGecko** (for crypto): https://www.coingecko.com/en/api
- **Alpha Vantage** (for stocks): https://www.alphavantage.co/support/#api-key

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ThatMasterCoder/crypto-price-analyzer.git
cd crypto-price-analyzer
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
COINGECKO_API_KEY=your-coingecko-api-key-here
ALPHAVANTAGE_API_KEY=your-alphavantage-api-key-here
```

### 4. Configure Your Watchlist

**For Cryptocurrencies** - Edit `data/coins.txt`:
```
bitcoin
ethereum
dogecoin
```

**For Stocks** - Edit `data/stocks.txt`:
```
AAPL
NVDA
GOOGL
```

## Usage

### Windows (PowerShell)
```powershell
.\run.ps1
```

> **Note**: This project currently only supports Windows. Linux/macOS support coming soon!

The script will:
1. Compile the C++ analyzer
2. Prompt you to choose between crypto or stock tracking
3. Ask for your preferred currency (USD/CAD)
4. Start monitoring prices in real-time

### Sample Output
```
Select a data fetcher:
1. Crypto Fetcher
2. Stocks Fetcher

Enter your choice (1 or 2): 2
Enter currency (usd/cad): usd

Valid stocks: AAPL, NVDA, GOOGL

Analyzed data:
Name: AAPL, Last Price: $353.21, Latest Price: $354.15, Change: $0.94, Change (%): 0.266%
Name: NVDA, Last Price: $256.51, Latest Price: $257.30, Change: $0.79, Change (%): 0.308%
Name: GOOGL, Last Price: $354.62, Latest Price: $355.10, Change: $0.48, Change (%): 0.135%

----------------------------------------
Waiting 60 seconds before next fetch...
```

## Rate Limiting

### CoinGecko (Crypto)
- **Free tier**: 30 calls/minute
- Script delay: 30 seconds between fetch cycles

### Alpha Vantage (Stocks)
- **Free tier**: 5 calls/minute, 100 calls/day
- Script delay: 13 seconds between individual requests, 60 seconds between cycles
- **Note**: With 3 stocks, you'll use ~65 API calls per hour

**Tip**: The stock market is only open Monday-Friday, 9:30 AM - 4:00 PM EST. Prices won't change outside these hours!

## Troubleshooting

### "Rate limit exceeded"
- **Crypto**: Increase `DELAY` in `crypto_fetcher.py`
- **Stocks**: Increase `DELAY` or reduce the number of stocks in `stocks.txt`

### "No valid price data"
- Check your API keys in `.env`
- Verify coin/stock symbols are correct
- Check if you've hit daily API limits

### Compilation errors
```bash
# Verify g++ is installed
g++ --version

# Manual compilation
g++ -Wall -Wextra -g3 -o output/analyzer.exe src/cpp/analyzer.cpp
```

## Technologies Used

- **Python 3.12** - API data fetching
- **C++17** - Price analysis and calculations
- **PowerShell** - Build automation and orchestration
- **APIs**: CoinGecko, Alpha Vantage, ExchangeRate-API

## Dependencies

See `requirements.txt`:
- `requests` - HTTP requests for API calls
- `python-dotenv` - Environment variable management
- `yfinance` - Yahoo Finance data (backup for stocks)

## Future Improvements

- [ ] Add JSON parsing library (nlohmann/json) for C++
- [ ] Implement price alerts/notifications
- [ ] Add historical data tracking and charts
- [ ] Support more exchanges and data sources
- [ ] Create a web dashboard for visualization
- [ ] Add automated testing

## License

This project is licensed under the APACHE License - see the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Author

**ThatMasterCoder**
- GitHub: [@ThatMasterCoder](https://github.com/ThatMasterCoder)

---
