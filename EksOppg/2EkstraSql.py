import mysql.connector
import datetime
import pyfirmata
import time


mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="elev",
	database="3elda"
)


board = pyfirmata.Arduino('COM6')
it = pyfirmata.util.Iterator(board)
it.start()


pot = board.get_pin('a:0:i')
led = board.get_pin('d:13:o')


mycursor = mydb.cursor()


print("SQL connected..")


sql = "INSERT INTO sensor(verdi,tid) VALUES(%s, %s)"

while True: 
	print("reading...")

	verdi = pot.read()
	tid = datetime.datetime.now()

	val = (verdi, tid)
	
	print("Executing...")

	mycursor.execute(sql,val)
	mydb.commit()

	print("Done")

	time.sleep(3)