import subprocess
import sys
from fabric import Connection


def run_remote_command(host, command):

    # HOST="storefront@prodbuilder1.crownawards.com"
    HOST = 'storefront@'+host+'.crownawards.com'
    # Ports are handled in ~/.ssh/config since we use OpenSSH
    # COMMAND="sudo /usr/sbin/builder_restart.sh"
    COMMAND = command

    ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        print("ERROR: %s" % error)
    else:
        print(result)


def run_remote_command2(host, command):

    # First lets try running the command, and trap the result.
    # If we get an error, print and error message and exit.
    try:
        result = Connection(host=host, user="storefront").run(command)
        # Now print our findings.
        msg = "Ran {.command!r} on {.host}, got this stdout:\n{.stdout}"
        print(msg.format(result))
    except Exception as e:
        print("ERROR: Unable to run remote command on host %s" % host)
        print(e)


if __name__ == "__main__:":

    run_remote_command('null', 'null')
