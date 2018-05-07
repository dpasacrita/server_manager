from flask import Flask, request, render_template
import time
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/button_test')
def button_test():
    return render_template('button_test.html', server_time=time.time())

@app.route('/start/')
@app.route('/start/<server>')
def start(server=None):
    return 'We\'re gonna restart server %s' % server