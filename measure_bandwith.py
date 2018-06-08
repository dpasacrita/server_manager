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

    return stats

if __name__ == "__main__:":

    pb1 = read_server_status("prodbuilder1")

    # Try printing the server status to the page as a test
    print(pb1)
    print("We printed the server-status, I think.")
