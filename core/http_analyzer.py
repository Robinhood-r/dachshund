import requests

def http_probe(url, timeout):
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=False)
    except requests.exceptions.RequestException:
        return None

    return response.status_code

if __name__ == "__main__":
    print(http_probe("https://www.google.com"))
    print(http_probe("https://this-domain-does-not-exist-asdf123.com"))