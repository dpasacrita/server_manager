#!/bin/bash
# Server Manager
# This script is used by the server manager on RS2 to manage tomcat.

restart_tomcat() {
    # Determine PID of tomcat
    tomcat_pid="$(ps aux | grep '[t]omcat' | awk '{print $2}')"
    # ERROR HANDLING - If failure, start tomcat
    if [[ -n "$tomcat_pid" ]]
    then
        # Success, keep moving through the script, as this means tomcat is running.
        printf "[$CURRENT_DATE] - Successfully retrieved tomcat pid.\n" >> "$LOG_DIRECTORY""$LOG_FILE"
    else
        printf "[$CURRENT_DATE] - ERROR: Did not successfully retrieve pid! Tomcat might not be running\n" >&2 >> "$LOG_DIRECTORY""$LOG_FILE"
        # Start Tomcat
        printf "[$CURRENT_DATE] - Starting tomcat...\n" >> "$LOG_DIRECTORY""$LOG_FILE"
        su -c ''"$TOMCAT_DIRECTORY"'bin/startup.sh' storefront >> "$LOG_DIRECTORY""$LOG_FILE"
        # ERROR HANDLING
        if [[ $? -eq 0 ]]
        then
            # Say that it successfully restarted, and exit
	        printf "[$CURRENT_DATE] - Tomcat has been restarted.\n" >> "$LOG_DIRECTORY""$LOG_FILE"
            exit 0
        else
	    # Print another Error and just give up already.
            printf "[$CURRENT_DATE] - ERROR: Failed to start tomcat! Shutting down.\n" >> "$LOG_DIRECTORY""$LOG_FILE"
	        exit 1
        fi
    fi

    # Restart tomcat
    printf "[$CURRENT_DATE] - Killing tomcat...\n" >> "$LOG_DIRECTORY""$LOG_FILE"
    kill -9 "$tomcat_pid" >> "$LOG_DIRECTORY""$LOG_FILE"
    # ERROR HANDLING
    if [[ $? -eq 0 ]]
    then
        printf "[$CURRENT_DATE] - Tomcat process has been killed.\n" >> "$LOG_DIRECTORY""$LOG_FILE"
    else
        printf "[$CURRENT_DATE] - ERROR: Failed to kill tomcat process!\n" >> "$LOG_DIRECTORY""$LOG_FILE"
        exit 1
    fi
    # Run tomcat as storefront
    su -c ''"$TOMCAT_DIRECTORY"'bin/startup.sh' storefront >> "$LOG_DIRECTORY""$LOG_FILE"
    # ERROR HANDLING
    if [[ $? -eq 0 ]]
    then
        # Say that it successfully restarted, and exit
        printf "[$CURRENT_DATE] - Tomcat has been restarted.\n" >> "$LOG_DIRECTORY""$LOG_FILE"
        exit 0
    else
        # Print another Error and just give up already.
        printf "[$CURRENT_DATE] - ERROR: Failed to start tomcat! Shutting down.\n" >> "$LOG_DIRECTORY""$LOG_FILE"
        exit 1
    fi
}

stop_tomcat() {
    # Determine PID of tomcat
    tomcat_pid="$(ps aux | grep '[t]omcat' | awk '{print $2}')"
    # ERROR HANDLING - If failure, tomcat is already stopped, so stop.
    if [[ -n "$tomcat_pid" ]]
    then
        # Success, keep moving through the script, as this means tomcat is running.
        printf "[$CURRENT_DATE] - Successfully retrieved tomcat pid.\n" >> "$LOG_DIRECTORY""$LOG_FILE"
    else
        printf "[$CURRENT_DATE] - ERROR: Did not successfully retrieve pid! Tomcat might not be running\n" >&2 >> "$LOG_DIRECTORY""$LOG_FILE"
        # End Script.
        printf "[$CURRENT_DATE] - Ending script, as tomcat has already been stopped.\n" >> "$LOG_DIRECTORY""$LOG_FILE"
        exit 0
    fi

    # Kill tomcat
    printf "[$CURRENT_DATE] - Killing tomcat...\n" >> "$LOG_DIRECTORY""$LOG_FILE"
    kill -9 "$tomcat_pid" >> "$LOG_DIRECTORY""$LOG_FILE"
    # ERROR HANDLING
    if [[ $? -eq 0 ]]
    then
        printf "[$CURRENT_DATE] - Tomcat process has been killed.\n" >> "$LOG_DIRECTORY""$LOG_FILE"
    else
        printf "[$CURRENT_DATE] - ERROR: Failed to kill tomcat process!\n" >> "$LOG_DIRECTORY""$LOG_FILE"
        exit 1
    fi
}

start_tomcat() {
    # Check if tomcat is already running by checking for PID.
    tomcat_pid="$(ps aux | grep '[t]omcat' | awk '{print $2}')"
    # ERROR HANDLING - If failure, continue.
    if [[ -n "$tomcat_pid" ]]
    then
        # Success, exit immediately as this means that tomcat is already running.
        printf "[$CURRENT_DATE] - Successfully retrieved tomcat pid.\n" >> "$LOG_DIRECTORY""$LOG_FILE"
        printf "[$CURRENT_DATE] - Ending script, as this means tomcat is already running.\n" >&2 >> "$LOG_DIRECTORY""$LOG_FILE"
        exit 0
    else
        printf "[$CURRENT_DATE] - Did not successfully retrieve pid, starting tomcat.\n" >&2 >> "$LOG_DIRECTORY""$LOG_FILE"
        # Start Tomcat
        printf "[$CURRENT_DATE] - Starting tomcat...\n" >> "$LOG_DIRECTORY""$LOG_FILE"
        su -c ''"$TOMCAT_DIRECTORY"'bin/startup.sh' storefront >> "$LOG_DIRECTORY""$LOG_FILE"
        # ERROR HANDLING
        if [[ $? -eq 0 ]]
        then
            # Say that it successfully restarted, and exit
	        printf "[$CURRENT_DATE] - Tomcat has been restarted.\n" >> "$LOG_DIRECTORY""$LOG_FILE"
            exit 0
        else
	    # Print another Error and just give up already.
            printf "[$CURRENT_DATE] - ERROR: Failed to start tomcat! Shutting down.\n" >> "$LOG_DIRECTORY""$LOG_FILE"
	        exit 1
        fi
    fi
}

# Load bash profile
. ~/.bash_profile

# Determine PWD, and time.
WORK_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
TOMCAT_DIRECTORY="/opt/tomcat/tomcat6/"
LOG_DIRECTORY="/var/log/"
LOG_FILE="server_manager.log"
CURRENT_DATE=$(date)
PROPERTIES_SOURCE="/opt/resources/"


while [[ "$1" != "" ]]; do
    case $1 in
    start)
        start_tomcat
        ;;
    stop)
        stop_tomcat
        ;;
    restart)
        restart_tomcat
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart}"
        exit 1
    esac
done