from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import mysql.connector


app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOP SECRET'
app.debug = True
socketio = SocketIO(app)
mydata = None


@app.route('/')
def index2():
	return render_template('index2.html')

@socketio.event
def my_ping():
	emit('my_pong')

@socketio.event
def get_sqldata():
	global mydata

	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="elev",
		database="3elda"
	)

	mycursor = mydb.cursor()

	mycursor.execute("SELECT verdi FROM sensor ORDER BY tid DESC LIMIT 1")

	mydata = mycursor.fetchone()


@socketio.event
def sql_data():
	global mydata
	print(mydata)
	emit('sqldata', {'POT': mydata[0]})


if __name__ == '__main__':
	socketio.run(app)