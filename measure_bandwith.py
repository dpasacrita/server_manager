# Import Statements
import requests


def read_server_status(host):
    # Make the URL
    url = "http://"+host+".crownawards.com/server-status?auto"
    # Try to open the server status page
    try:
        server_status = requests.get(url)
    except Exception:
        print("ERROR: Unable to load server-status!")
        print(Exception)
        return

    # Split the data into a list
    stats = format_stats(server_status.text)

    return stats


def format_stats(stats):

    # Split the data into a list
    stats = stats.splitlines()

    # Pop off the Scoreboard, because we don't need it here.
    stats.pop()
    return stats


def calculate_full_stats(stats):

    # We're going to calculate all of our stats one at a time.
    # First initialize all the variables we need.
    accesses = 0
    kbytes = 0
    mbytes = 0
    average_cpu = 0
    average_uptime = 0
    req_per_sec = 0
    bytes_per_sec = 0
    bytes_per_req = 0

    # Now lets fill them all with the builder stats
    for builder in stats:
        accesses = accesses + int(builder[0].split(": ", 1)[1])
        kbytes = kbytes + float(builder[1].split(": ", 1)[1])
        average_cpu = average_cpu + float(builder[2].split(": ", 1)[1])
        average_uptime = average_uptime + float(builder[3].split(": ", 1)[1])
        req_per_sec = req_per_sec + float(builder[4].split(": ", 1)[1])
        bytes_per_sec = bytes_per_sec + float(builder[5].split(": ", 1)[1])
        bytes_per_req = bytes_per_req + float(builder[6].split(": ", 1)[1])

    # Finally lets do some final calculations.
    # Get the total megabytes
    mbytes = kbytes / 1000
    # Divide CPU by the number of builders to get the average load.
    average_cpu = average_cpu / len(stats)
    # Divide uptime by the number of builders to get the average uptime.
    average_uptime = average_uptime / len(stats)
    average_uptime = average_uptime / 3600
    # Estimate Requests per hour
    req_per_hour = req_per_sec * 3600
    # Estimate kBytes per hour
    mbytes_per_hour = (req_per_hour * bytes_per_req) / 1000000

    # Fill the list and return it.
    full_stats = [accesses, kbytes, mbytes, average_cpu, req_per_sec, bytes_per_sec, bytes_per_req, req_per_hour, mbytes_per_hour, average_uptime]

    return full_stats


if __name__ == "__main__:":

    pb1 = read_server_status("prodbuilder1")

    # Try printing the server status to the page as a test
    print(pb1)
    print("We printed the server-status, I think.")
