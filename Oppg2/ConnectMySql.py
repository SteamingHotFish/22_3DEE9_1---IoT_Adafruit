import mysql.connector
import datetime
import pyfirmata
import time


#Koble til serveren med å skrive inn, addressen (localhost kan brukes hvis serveren er på denne pcen), brukeren, passordet og hvilken database som skal brukes
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="elev",
	database="3elda"
)


#definer COM-porten arduinoen er koblet til og les av hva du får der
board = pyfirmata.Arduino('COM4')
it = pyfirmata.util.Iterator(board)
it.start()

pot = board.get_pin('a:0:i')


#mydb.cursor brukes til å kunne execute og commit info til serveren
mycursor = mydb.cursor()

print("Connected..")

#i sql så skriver du inn hvilke tabeller og kolonner du vil bruke
sql = "INSERT INTO sensor(verdi, tid) VALUES (%s, %s)"


while True:
	verdi = pot.read()
	tid = datetime.datetime.now()

	#val skal holde på verdiene til både verdi og tid sånn at vi kan legge begge i mycursor.execute()
	val = (verdi, tid)

	print("Executing...")

	mycursor.execute(sql, val)
	mydb.commit()

	print("Done")

	time.sleep(3)