import cbpro
import pprint 
from settings import *
import datetime
import time

auth_client = cbpro.AuthenticatedClient(SANDBOX_API_SECRET,
                                       SANDBOX_B64SECRET,
                                        SANDBOX_PASSPHRASE,
					api_url="https://api-public.sandbox.pro.coinbase.com")


def log(record):
	f = open("logs.txt", "a")
	date = datetime.datetime.now()
	f.write('################### Trade of {} ################### \n'.format(date))
	for key, value in record.items():
		f.write('%s:%s\n' % (key, value))
	f.write('\n')
	f.close()

if __name__ == '__main__':
	market_list = ["BTC-EUR", "ETC-EUR", "USDT-EUR", "ADA-EUR", "SOL-EUR"]
	while True :
		currDate = datetime.datetime.now()
		day = int(currDate.strftime("%d"))
		if day == 27:
			for market in market_list:
				order = auth_client.buy(funds='40.00',
					order_type='market',
					product_id=market)
				log(order)  
			print('Bot is locked for 90000 seconds')
			time.sleep(10)
