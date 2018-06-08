from flask import Flask, request, render_template
import datetime
import remote_command
import measure_bandwith
app = Flask(__name__, static_url_path='/')


@app.route('/')
def index():
    return render_template('index.html', server_time=datetime.datetime.now())


@app.route('/prodbuilders')
def prodbuilders():
    return render_template('prodbuilders.html', server_time=datetime.datetime.now())


@app.route('/prodbuilders/serverstatus')
def pbserverstatus():
    # Get a list of builders, this will be in a config file later on
    # For the poor sod who reads this 4 years later and its not in a config file I'm sorry.
    builders = ['prodbuilder1', 'prodbuilder2', 'prodbuilder3']
    stats = []
    for builder in builders:
        stats.append(measure_bandwith.read_server_status(builder))
    return render_template('pbserverstatus.html', server_status=stats)


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
