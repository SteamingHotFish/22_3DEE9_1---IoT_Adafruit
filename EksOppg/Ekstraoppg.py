from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SUPER_SECRET'


@app.route('/')
def index(): 
	return render_template("index.html")

@app.route('/gey')
def gey(): 
	return render_template("gey.html")

app.run()