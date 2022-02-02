import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata


run_count = 0
ADAFRUIT_IO_USERNAME = "BiggyCheese"
ADAFRUIT_IO_KEY = "aio_xXuM00Hx0AsoQBEUqbdFsxG7KrDV"


aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


board = pyfirmata.Arduino('COM4')


it = pyfirmata.util.Iterator(board)
it.start()


led = board.get_pin('d:13:o')
pot = board.get_pin('a:0:i')


try:
	togle = aio.feeds('togle')
except RequestError:
	feed = Feed(name='togle')
	togle = aio.create_feed(feed)



while True:
	print('Sending count:', run_count)
	run_count += 1
	aio.send_data('counter', run_count)

	potVal = pot.read()
	print('Sending pot value:', potVal)
	aio.send_data('potmet', potVal)
	

	data = aio.receive(togle.key)


	print('Data: ', data.value)

	if data.value == "1":
		led.write(True)
	else:
		led.write(False)
	
	time.sleep(3)

