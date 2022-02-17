from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread


app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOP SECRET'
app.debug = True
socketio = SocketIO(app)


stop_thread = False
board = None
thr = None
start_thread = False

pins = {
    'COM': None,
    'A0': 0,
    'A1': 0,
    'A2': 0,
    'A3': 0,
    'A4': 0,
    'A5': 0,
}


def arduino_start(id, stop):
    import pyfirmata
    import time
    global board
    global pins
    global start_thread

    while True:

        if start_thread:
            board = None
            if board is None:
                board = pyfirmata.Arduino(str(pins['COM']))

            it = pyfirmata.util.Iterator(board)
            it.start()

            lamp_out = board.get_pin('d:13:o')
            analog_0 = board.get_pin('a:0:i')
            analog_1 = board.get_pin('a:1:i')
            analog_2 = board.get_pin('a:2:i')
            analog_3 = board.get_pin('a:3:i')
            analog_4 = board.get_pin('a:4:i')
            analog_5 = board.get_pin('a:5:i')

            start_thread = False

        while not stop_thread:
            lamp_out.write(True)
            time.sleep(0.5)
            lamp_out.write(False)
            time.sleep(0.5)

            pins['A0'] = analog_0.read()
            pins['A1'] = analog_1.read()
            pins['A2'] = analog_2.read()
            pins['A3'] = analog_3.read()
            pins['A4'] = analog_4.read()
            pins['A5'] = analog_5.read()

            if stop():
                board.exit()
                break


@app.route('/')
def index1():
    return render_template('index1.html')


@socketio.on('message', namespace='/test')
def handle_message(data):
    print('Received message: ' + data)


@socketio.event
def my_ping():
    emit('my_pong')


@socketio.event
def COM(message):
    pins['COM'] = message['data']


@socketio.event
def arduino_test():
    emit('my_response', {
        'COM': pins['COM'],
        'A0': pins['A0'],
        'A1': pins['A1'],
        'A2': pins['A2'],
        'A3': pins['A3'],
        'A4': pins['A4'],
        'A5': pins['A5'],
    })


@socketio.event
def arduino(data):
    global stop_thread
    global thr
    global start_thread

    if data['data'] == 'arduino_start':
        stop_thread = False
        start_thread = True
        if thr is None:
            thr = Thread(target=arduino_start, args=(id, lambda: stop_thread))
            thr.start()
    if data['data'] == 'arduino_stop':
        stop_thread = True


if __name__ == '__main__':
    socketio.run(app)