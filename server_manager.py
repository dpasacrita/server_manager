from flask import Flask, request, render_template, jsonify
import datetime
import remote_command
import measure_bandwith
import pickle
import log
from time import sleep
import npc
import os
app = Flask(__name__, static_url_path='/')


# Globals
SAVE_DATA_DIR = ''


@app.route('/')
def index():
    return render_template('index.html', server_time=datetime.datetime.now())


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


@app.route('/amuse/setup/')
def setup_scenario():
    return render_template('setup.html')


@app.route('/amuse/setup/playerchar/')
def setup_player():
    return render_template('setup_player.html')


@app.route('/amuse/setup/monster/')
def setup_monster():
    return render_template('setup_monster.html')


@app.route('/amuse/setup/savedata/')
@app.route('/amuse/setup/savedata/<data>/')
def save_data(data=None):
    if data == "player":
        # Pickle code to save data here
        # Let's grab every passed stat
        saved_stats = {
            "name": request.args.get('name'),
            "race": request.args.get('race'),
            "age": request.args.get('name'),
            "strength": request.args.get('strength'),
            "intelligence": request.args.get('intelligence'),
            "agility": request.args.get('agility'),
            "skill": request.args.get('skill')
        }
        # Now pickle the stats to player.p
        pickle.dump(saved_stats, open("/opt/sites/rs2/server_manager/data/player.p", "w"))
        return render_template('save_data.html', data=data)
    elif data == "monster":
        # Pickle code to save data here
        # Let's grab every passed stat
        saved_stats = {
            "name": request.args.get('name'),
            "race": request.args.get('race'),
            "age": request.args.get('name'),
            "strength": request.args.get('strength'),
            "intelligence": request.args.get('intelligence'),
            "agility": request.args.get('agility'),
            "skill": request.args.get('skill')
        }
        # Now pickle the stats to monster.p
        pickle.dump(saved_stats, open("/opt/sites/rs2/server_manager/data/monster.p", "w"))
        return render_template('save_data.html', data=data)
    else:
        return render_template('console.html', data=data)


@app.route('/amuse/setup/loaddata/')
@app.route('/amuse/setup/loaddata/<data>/')
def load_data(data=None):
    if data == "player":
        player = pickle.load(open("/opt/sites/rs2/server_manager/data/player.p", "w"))
        return jsonify(player)
    elif data == "monster":
        monster = pickle.load(open("/opt/sites/rs2/server_manager/data/player.p", "w"))
        return jsonify(monster)
    else:
        return "Nothing"


@app.route('/amuse/console/')
def console():
    return render_template('console.html')


@app.route('/stream')
def stream():
    def generate():
        with open('data/console.log') as f:
            while True:
                yield f.read()
                sleep(1)

    return app.response_class(generate(), mimetype='text/event-stream')


@app.route('/ajax', methods=['POST'])
def ajax_request():
    username = request.form['username']
    return jsonify(username=username)
