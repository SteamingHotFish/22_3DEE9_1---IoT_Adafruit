import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata


#run_count vil holde tellingen på hvor mange ganger koden looper
run_count = 0
#for å koble til riktig dashbord må man bruke brukernavnet ditt og nøkkelen som du finner på dashbordet du skal bruke
ADAFRUIT_IO_USERNAME = "BiggyCheese"
ADAFRUIT_IO_KEY = "aio_xXuM00Hx0AsoQBEUqbdFsxG7KrDV"


aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


#Definer hvilken COM arduinoen du bruker er koblet til
board = pyfirmata.Arduino('COM4')


#Les av det som kommer inn på COM-porten som ble satt
it = pyfirmata.util.Iterator(board)
it.start()


#For å gjør koden mer lesbar gir vi board.get_pin() navn
led = board.get_pin('d:13:o')
pot = board.get_pin('a:0:i')


#Test om det finnes en feed som heter togle, hvis ikke så skal dashbordet lage en
try:
	togle = aio.feeds('togle')
except RequestError:
	feed = Feed(name='togle')
	togle = aio.create_feed(feed)



while True:
	#Når while looper print run_count til både cmd og dashbord, så øk run_count for neste gang
	print('Sending count:', run_count)
	run_count += 1
	aio.send_data('counter', run_count)

	#les av verdien som kommer in gjennom pot og print den til cmd og send til dashbord
	potVal = pot.read()
	print('Sending pot value:', potVal)
	aio.send_data('potmet', potVal)
	

	#mota en verdi fra dashbord
	data = aio.receive(togle.key)


	#print verdien du fikk fra dashbord
	print('Data: ', data.value)

	#Hvis verdien er 1 så skriver du True til led
	if data.value == "1":
		led.write(True)
	else:
		led.write(False)
	
	#delay som senker koden litt ned, fint for å se hva som skjer, men dashbordet har en grense på hvor mye som kan komme inn så vi kan ikke kjøre full gass
	time.sleep(3)

