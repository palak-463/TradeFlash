from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

API_KEY = '669835009387f9.87422928'

# Top 50 stock symbols and their corresponding company names
STOCKS = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "AMZN": "Amazon.com Inc.",
    "GOOGL": "Alphabet Inc.",
    "TSLA": "Tesla Inc.",
    "FB": "Meta Platforms Inc.",
    "BRK.B": "Berkshire Hathaway Inc.",
    "NVDA": "NVIDIA Corporation",
    "JPM": "JPMorgan Chase & Co.",
    "V": "Visa Inc.",
    "PYPL": "PayPal Holdings Inc.",
    "HD": "The Home Depot Inc.",
    "DIS": "The Walt Disney Company",
    "CMCSA": "Comcast Corporation",
    "PEP": "PepsiCo Inc.",
    "NFLX": "Netflix Inc.",
    "CSCO": "Cisco Systems Inc.",
    "ADBE": "Adobe Inc.",
    "INTC": "Intel Corporation",
    "AVGO": "Broadcom Inc.",
    "COST": "Costco Wholesale Corporation",
    "TMUS": "T-Mobile US Inc.",
    "ABNB": "Airbnb Inc.",
    "SBUX": "Starbucks Corporation",
    "NKE": "Nike Inc.",
    "IBM": "International Business Machines Corporation",
    "PG": "Procter & Gamble Company",
    "CRM": "Salesforce.com Inc.",
    "MO": "Altria Group Inc.",
    "UNH": "UnitedHealth Group Incorporated",
    "MRNA": "Moderna Inc.",
    "NVAX": "Novavax Inc.",
    "BAC": "Bank of America Corporation",
    "WMT": "Walmart Inc.",
    "KO": "The Coca-Cola Company",
    "MS": "Morgan Stanley",
    "GOOG": "Alphabet Inc.",
    "GE": "General Electric Company",
    "CVX": "Chevron Corporation",
    "XOM": "Exxon Mobil Corporation",
    "BA": "The Boeing Company",
    "T": "AT&T Inc.",
}

def fetch_stock_data(stock_symbols):
    stock_data = {}
    for symbol in stock_symbols:
        try:
            url = f'https://eodhistoricaldata.com/api/real-time/{symbol}.US?api_token={API_KEY}&fmt=json'
            response = requests.get(url)
            data = response.json()
            if data:
                stock_data[symbol] = {
                    "company": STOCKS[symbol],
                    "price": float(data["close"]),
                    "change": (float(data["close"]) - float(data["open"])) / float(data["open"]) * 100
                }
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    return stock_data

@app.route("/", methods=["GET", "POST"])
def index():
    filtered_data = []

    if request.method == "POST":
        search_query = request.form.get("search").upper()
        stocks_to_display = [stock for stock in STOCKS if search_query in stock]
    else:
        stocks_to_display = STOCKS.keys()

    data = fetch_stock_data(stocks_to_display)

    if data:
        for stock in data:
            filtered_data.append({
                "name": stock,
                "company": data[stock]["company"],
                "price": data[stock]["price"],
                "change": round(data[stock]['change'], 2)
            })

    return render_template('stocks.html', stocks=filtered_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
