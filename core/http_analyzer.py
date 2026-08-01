import requests

def http_probe(url, timeout):
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=False)
    except requests.exceptions.RequestException:
        return None

    return response.status_code

