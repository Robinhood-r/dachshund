import socket



def dns_lookup(hostname):

    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        return None



if __name__ == "__main__":
    print(dns_lookup("google.com"))
    print(dns_lookup("fake-domain-that-doesnt-exist-123.com"))