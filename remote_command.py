import subprocess
import sys


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

if __name__ == "__main__:":

    run_remote_command('null', 'null')