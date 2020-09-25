import argparse
import pyRofex as rofex

FIRST_PRICE_ORDER = 75.25
SIZE_OF_FIRST_ORDER = 1
PRICE_TO_SUBTRACT = 0.01

def send_order(ticker, size, price):
    print("Ingresando orden a", price)
    order = rofex.send_order(ticker=ticker,
                            side=rofex.Side.BUY,
                            size=size,
                            price=price,
                            order_type=rofex.OrderType.LIMIT)
    print("Cerrando sesión en Remarkets")
    return order

def on_ok(market_data):
    print("Último precio operado:", market_data['marketData']['LA']['price'])

    print("Consultando BID")

    orders =  market_data['marketData']["BI"]

    if orders:
        bid_price = orders[0]['price']
        bid_size = orders[0]['size']
        new_order_price = bid_price - PRICE_TO_SUBTRACT
        print("Precio de BID:", bid_price)
        send_order(ticker=args['asset'], size=bid_size, price=new_order_price)
    else:
        print("No hay BIDs activos")
        send_order(ticker=args['asset'], size=SIZE_OF_FIRST_ORDER, price=FIRST_PRICE_ORDER)

def on_error(market_data):
    print("Símbolo inválido")
    print("Cerrando sesión en Remarkets")

MARKET_DATA_STATUS = {'OK': on_ok,
                      'ERROR': on_error}

ap = argparse.ArgumentParser(description='Buy.')

ap.add_argument("asset", type=str, help="Symbol of the assets")
ap.add_argument("-u", "--user", required=True, type=str,
   help="remarkets user")
ap.add_argument("-p", "--password", required=True, type=str,
   help="remarkets password")

args = vars(ap.parse_args())

print("Iniciando sesión en Remarkets")

rofex.initialize(user=args['user'],
                   password=args['password'],
                   account="REM5031",
                   environment=rofex.Environment.REMARKET)

print("Consultando símbolo")
market_data = rofex.get_market_data(ticker=args['asset'], entries= [rofex.MarketDataEntry.BIDS, rofex.MarketDataEntry.LAST])
market_data_status = market_data['status']

MARKET_DATA_STATUS[market_data_status](market_data)
