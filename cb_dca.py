import cbpro
import pprint 
import datetime
import time
import sys
import logging
from timeit import default_timer


if len(sys.argv) > 1:
	if sys.argv[1] == "-r":
		from settings import *
else:
	from sandbox_settings import *

logging.basicConfig(filename=LOG_FILE, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
logging.warning("{} mode.".format(MODE))

# Log connection errors
try:
	auth_client = cbpro.AuthenticatedClient(API_SECRET, B64SECRET, PASSPHRASE, api_url=API_URL)
except:
	logging.error('Connection failed.')
	sys.exit()


if __name__ == '__main__':
	logging.info('DCA process is now active.')
	while True :
		currDate = datetime.datetime.now()
		day = int(currDate.strftime("%d"))
		if day == INVESTMENT_DAY:
			logging.info('Today is investment day.')
			for market in MARKET_LIST:
				order = auth_client.buy(funds=FUNDS,
							order_type='market',
							product_id=market)
				logging.info("Buy order sent.") 
				start = default_timer()
				
				# Wait for the order to be filled
				while order['status'] != "done":
					order = auth_client.get_order(order['id'])
					time.sleep(1)
					duration = default_timer() - start
					
					# Prevent blocked order
					if duration >= 15:
						logging.error("Order not filled.")
						auth_client.cancel_order(order['id'])
						break

				logging.info("{} order filled. {} BTC bought for {} €".format(order['product_id'], 
												order['filled_size'], 
												order['funds']))

			time.sleep(SLEEP_TIME)
