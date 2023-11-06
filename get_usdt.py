import ccxt

# Configura el exchange (en este caso, Binance)
exchange = ccxt.binance()

# Define el símbolo (par de trading) que te interesa, en este caso, USDT/USD
symbol = 'USDT/USDT:USDT'

try:
    # Obtiene el libro de órdenes para el símbolo
    order_book = exchange.fetch_order_book(symbol)

    # Obtiene el precio del último trade (puede variar ligeramente)
    last_price = order_book['bids'][0][0]  # Precio de compra (bid)

    # Imprime el precio en tiempo real
    print(f'Precio del USDT en dólares en tiempo real: ${last_price}')

except ccxt.NetworkError as e:
    print(f'Error de red: {e}')

except ccxt.ExchangeError as e:
    print(f'Error del exchange: {e}')

except Exception as e:
    print(f'Error desconocido: {e}')
