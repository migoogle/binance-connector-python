from binance.spot import Spot

client = Spot()

# Get server timestamp
print(client.time())
# Get klines of BTCUSDT at 1m interval
#print(client.klines("BTCUSDT", "1m"))
# Get last 10 klines of BNBUSDT at 1h interval
print(client.klines("BNBUSDT", "1h", limit=10))

# API key/secret are required for user data endpoints
client = Spot(api_key='xvBGfd056zjKhHsRu8IIbiqKC1CpQSXHJeYgYatJK5HaizvFXs8kGWwSQlAoEh2m', api_secret='QIVcb1ZBvlurqLNvVw5hF9xQSqq061yjzjA7m8OkuRmcW3QsGfqVrOHcUeiQDLQM')

# Get account and balance information
#print(client.account())

response = client.funding_wallet()
print(response)
# write the account information to a file .json
import json
with open('account.json', 'w') as f:
    json.dump(client.account(), f)


