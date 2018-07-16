#!/usr/bin/python3.5

# Imports
import time

# Globals
CONSOLE_FILE = '/opt/sites/rs2/server_manager/data/console.log'


def push_to_console(data, logtype):

    # Let's get the current time first in the format we want
    cur_time = time.strftime("%H:%M:%S")

    # Try to open the file, error if it doesn't.
    try:
        console = open(CONSOLE_FILE, "a")
    except Exception as e:
        print(e)
        print("ERROR: Cannot open console file for writing!")
        return

    # Now try and write the the file.
    try:
        console.write(cur_time + " - " + logtype + ": " + data + "\n")
    except Exception as e:
        print(e)
        print("ERROR: Cannot log to console file!")
        return

    # Close the log file and return.
    console.close()
    return
