import requests
from bs4 import BeautifulSoup

def enumerate_directories(url):

    findings = []

    with open("wordlist.txt") as file:

        for line in file:

            path = line.strip()

            target = f"{url}/{path}"

            try:

                response = requests.get(target, timeout=3)

                if response.status_code in [200, 301, 302, 403]:

                    soup = BeautifulSoup(
                        response.text,
                        "html.parser"
                    )

                    title = (
                        soup.title.string.strip()
                        if soup.title and soup.title.string
                        else "No Title"
                    )

                    findings.append(
                        (
                            target,
                            response.status_code,
                            title
                        )
                    )

            except:
                pass

    return findings
