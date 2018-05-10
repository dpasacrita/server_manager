from flask import Flask, request, render_template
import datetime
import remote_command
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/button_test')
def button_test():
    return render_template('button_test.html', server_time=datetime.datetime.now().strftime('%b-%d-%I%M%p-%G'))

@app.route('/start/')
@app.route('/start/<server>')
def start(server=None):
    remote_command.run_remote_command(server, 'sudo /usr/sbin/server_manager.sh start')
    return 'We\'re gonna start server %s' % server

@app.route('/stop/')
@app.route('/stop/<server>')
def stop(server=None):
    remote_command.run_remote_command(server, 'sudo /usr/sbin/server_manager.sh stop')
    return 'We\'re gonna stop server %s' % server

@app.route('/restart/')
@app.route('/restart/<server>')
def restart(server=None):
    remote_command.run_remote_command(server, 'sudo /usr/sbin/server_manager.sh restart')
    return 'We\'re gonna restart server %s' % server