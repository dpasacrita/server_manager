from flask import Flask, request, render_template
import time
import remote_command
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/button_test')
def button_test():
    return render_template('button_test.html', server_time=time.time())

@app.route('/start/')
@app.route('/start/<server>')
def start(server=None):
    return 'We\'re gonna start server %s, or we would, but this is still a work in progress! Stick to restarting.' % server

@app.route('/stop/')
@app.route('/stop/<server>')
def stop(server=None):
    return 'We\'re gonna stop server %s, or we would, but this is still a work in progress! Stick to restarting.' % server

@app.route('/restart/')
@app.route('/restart/<server>')
def restart(server=None):
    remote_command.run_remote_command(server, 'sudo /usr/sbin/builder_restart.sh')
    return 'We\'re gonna restart server %s' % server