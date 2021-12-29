import cbpro
import pprint 
import datetime
import time
import sys


if len(sys.argv) > 1:
	if sys.argv[1] == "-r":
		from settings import *
else:
	from sandbox_settings import *

auth_client = cbpro.AuthenticatedClient(API_SECRET,
					B64SECRET,
                                        PASSPHRASE,
                                        api_url=API_URL)


def log(record):
	f = open("logs.txt", "a")
	date = datetime.datetime.now()
	f.write('################### Trade of {} ################### \n'.format(date))
	for key, value in record.items():
		f.write('%s:%s\n' % (key, value))
	f.write('\n')
	f.close()


if __name__ == '__main__':
	while True :
		currDate = datetime.datetime.now()
		day = int(currDate.strftime("%d"))
		if day == INVESTMENT_DAY:
			for market in MARKET_LIST:
				order = auth_client.buy(funds=FUNDS,
							order_type='market',
							product_id=market)
				log(order)  
			print('Bot is locked for {} seconds'.format(SLEEP_TIME))
			time.sleep(SLEEP_TIME)
