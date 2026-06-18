import requests

def detect_technology(url):

    try:

        response = requests.get(url, timeout=5)

        return {
            "server": response.headers.get("Server"),
            "powered_by": response.headers.get("X-Powered-By")
        }

    except Exception as e:

        return {
            "error": str(e)
        }
