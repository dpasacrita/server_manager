from flask import Flask, request, render_template
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
SAVE_DATA_DIR = '/opt/sites/rs2/server_manager/data/'


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
    builders = ['prodbuilder1', 'prodbuilder2', 'prodbuilder3', 'prodbuilder4', 'prodbuilder5', 'prodbuilder6', 'prodbuilder7', 'prodbuilder8', 'prodbuilder9']
    stats = []
    for builder in builders:
        stats.append(measure_bandwith.read_server_status(builder))
    full_stats = measure_bandwith.calculate_full_stats(stats)
    return render_template('pbserverstatus.html', server_status=stats, server_status_all=full_stats)


@app.route('/testapis')
def testapis():
    return render_template('testapis.html', server_time=datetime.datetime.now())


@app.route('/webstore')
def webstore():
    return render_template('webstore.html', server_time=datetime.datetime.now())


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


@app.route('/manage/prodproship/')
@app.route('/manage/prodproship/<server>')
def prodproship(server=None):
    remote_command.run_remote_command2(server, 'sudo /usr/sbin/server_manager.sh prodproship')
    return render_template('run_remote_command.html', command='Switch to Prod Proship', servername=server)


@app.route('/manage/testproship/')
@app.route('/manage/testproship/<server>')
def testproship(server=None):
    remote_command.run_remote_command2(server, 'sudo /usr/sbin/server_manager.sh testproship')
    return render_template('run_remote_command.html', command='Switch to Test Proship', servername=server)


@app.route('/amuse/setup/')
def setup_scenario():
    return render_template('setup.html')


@app.route('/amuse/setup/playerchar/')
def setup_player():
    return render_template('setup_player.html')


@app.route('/amuse/setup/monster/')
def setup_monster():
    return render_template('setup_monster.html')


@app.route('/amuse/setup/data/')
@app.route('/amuse/setup/data/<data>/')
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
        return render_template('battle.html', data=data)


@app.route('/amuse/fight/')
@app.route('/amuse/fight/<monster>')
def fight(monster=None):
    log.push_to_console("This is a test combat line", "COMBAT")
    return render_template('battle.html', encounter=monster)


@app.route('/stream')
def stream():
    def generate():
        with open('data/console.log') as f:
            while True:
                yield f.read()
                sleep(1)

    return app.response_class(generate(), mimetype='text/event-stream')
