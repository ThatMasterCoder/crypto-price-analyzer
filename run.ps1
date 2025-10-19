# Compile C++ analyzer
Write-Host "Compiling C++ analyzer..." -ForegroundColor Cyan
g++ -Wall -Wextra -g3 -o output\analyzer.exe .\src\cpp\analyzer.cpp

if ($LASTEXITCODE -ne 0) {
    Write-Host "Compilation failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Compilation successful!" -ForegroundColor Green
Write-Host ""

# Prompt user to choose fetcher
Write-Host "Select a data fetcher:" -ForegroundColor Yellow
Write-Host "1. Crypto Fetcher"
Write-Host "2. Stocks Fetcher"
Write-Host ""

$choice = Read-Host "Enter your choice (1 or 2)"

switch ($choice) {
    "1" {
        Write-Host "`nRunning Crypto Fetcher..." -ForegroundColor Green
        python src\python\crypto_fetcher.py .\output\analyzer.exe
    }
    "2" {
        Write-Host "`nRunning Stocks Fetcher..." -ForegroundColor Green
        python src\python\stocks_fetcher.py .\output\analyzer.exe
    }
    default {
        Write-Host "`nInvalid choice! Please run the script again and select 1 or 2." -ForegroundColor Red
        exit 1
    }
}