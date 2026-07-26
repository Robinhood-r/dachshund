import socket


# A function to look up each dns entered. It takes 2 parameters: hostname and timeout. Hostname is the url and 
# timeout is the time limit for giving up after there is no answer
def dns_lookup(hostname, timeout=2.0):

# Trying to see if the domain exists within the timeframe. 
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except (socket.gaierror, socket.timeout):
        return None


# Testing the app
if __name__ == "__main__":
    print(dns_lookup("google.com"))
    print(dns_lookup("fake-domain-that-doesnt-exist-123.com"))