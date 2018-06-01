from flask import Flask, request, render_template
import datetime
import remote_command
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', server_time=datetime.datetime.now())


@app.route('/prodbuilders')
def prodbuilders():
    return render_template('prodbuilders.html', server_time=datetime.datetime.now())


@app.route('/testapis')
def testapis():
    return render_template('testapis.html', server_time=datetime.datetime.now())


@app.route('/start/')
@app.route('/start/<server>')
def start(server=None):
    remote_command.run_remote_command2(server, 'sudo /usr/sbin/server_manager.sh start')
    return render_template('run_remote_command.html', command='Start', servername=server)


@app.route('/stop/')
@app.route('/stop/<server>')
def stop(server=None):
    remote_command.run_remote_command2(server, 'sudo /usr/sbin/server_manager.sh stop')
    return render_template('run_remote_command.html', command='Stop', servername=server)


@app.route('/restart/')
@app.route('/restart/<server>')
def restart(server=None):
    remote_command.run_remote_command2(server, 'sudo /usr/sbin/server_manager.sh restart')
    return render_template('run_remote_command.html', command='Restart', servername=server)
