import requests
from bs4 import BeautifulSoup

def main():
    URL = 'http://th.if.uj.edu.pl/'

    result = requests.get(URL)
    status = result.status_code

    if status != 200:
        return status

    content_type = result.headers['Content-Type'].lower()

    if content_type != 'text/html':
        return status

    soup = BeautifulSoup(result.text, 'html.parser')

    src = soup.find(text="Theorethical Physics Departments")

    if src != "Theorethical Physics Departments":
        return status

    return status

value = main()
print(value)


