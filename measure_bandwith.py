# Import Statements
import urllib.request as request


def read_server_status(host):
    # Make the URL
    url = "http://"+host+".crownawards.com/server-status?auto"
    # Try to open the server status page
    try:
        server_status = request.urlopen(url)
    except Exception:
        print("ERROR: Unable to load server-status!")
        print(Exception)
        return

    return server_status


if __name__ == "__main__:":

    pb1 = read_server_status("prodbuilder1")

    # Try printing the server status to the page as a test
    print(pb1)
    print("We printed the server-status, I think.")
