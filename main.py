import requests

API_URL = "https://api.kraken.com"

# Fetch all tradable asset pairs using Kraken's REST API
def get_tradable_pairs():
    response = requests.get(f"{API_URL}/0/public/AssetPairs")
    result = response.json()
    if 'error' in result and result['error']:
        print(f"Error fetching pairs: {result['error']}")
        return []
    return list(result['result'].keys())

# Fetch order book for a specific trading pair (best bid and ask) using REST API
def get_order_book(pair):
    response = requests.get(f"{API_URL}/0/public/Depth?pair={pair}&count=1")
    result = response.json()
    if 'error' in result and result['error']:
        print(f"Error fetching order book for {pair}: {result['error']}")
        return None
    return result['result'].get(pair, {})

# Calculate the spread percentage: (ask - bid) / midpoint * 100
def calculate_spread_percentage(ask, bid):
    midpoint = (ask + bid) / 2
    if midpoint == 0:  # Avoid division by zero
        return 0
    return ((ask - bid) / midpoint) * 100

# Rank pairs by spread using the REST API
def rank_pairs_by_spread():
    pairs = get_tradable_pairs()
    spread_results = []

    # Iterate through all pairs and calculate their spread
    for pair in pairs:
        try:
            order_book = get_order_book(pair)
            if not order_book or 'asks' not in order_book or 'bids' not in order_book:
                continue
            ask_price = float(order_book['asks'][0][0])
            bid_price = float(order_book['bids'][0][0])
            spread_percentage = calculate_spread_percentage(ask_price, bid_price)
            
            # Verbosely print the spread for each pair as it's calculated
            print(f"Pair: {pair} | Bid: {bid_price:.20f}, Ask: {ask_price:.20f} | Spread: {spread_percentage:.2f}%")
            
            spread_results.append((pair, spread_percentage))
        except Exception as e:
            print(f"Error processing {pair}: {e}")

    # Sort pairs by the largest spread percentage
    sorted_spreads = sorted(spread_results, key=lambda x: x[1], reverse=True)

    # Display the final ranking
    print("\nTop Trading Pairs by Largest Spread:")
    for pair, spread in sorted_spreads[:1000]:
        print(f"{pair}: {spread:.20f}%")

# Run the function to rank pairs by spread
rank_pairs_by_spread()
