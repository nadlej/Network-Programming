# Piotr Pzemielewski - Programowanie sieciowe 

import requests
import re
from bs4 import BeautifulSoup


def getInfo():

    URL = 'https://pogoda.interia.pl/prognoza-szczegolowa-krakow,cId,4970'

    result = requests.get(URL)

    # Sprawdzamy status pobranej strony, jezeli == 200, przechodzimy dalej

    if not result.status_code == 200:
        return 'WRONG STATUS CODE'

    # Ze slownika naglowkow (dictionary of response headers) pobierany zawartosc naglowka 'Content-Type'

    content_type = result.headers['Content-Type'].lower()

    # Sprawdzamy czy strona jest strona HTML

    if 'text/html' not in content_type:
        return 'IT IS NOT A HTML PAGE'

    # Pobieramy zawartosc strony korzystajac z biblioteki BeautifulSoup

    soup = BeautifulSoup(result.text, 'html.parser')

    # Szukamy danych zawartych w div'ie, gdzie obiektowi class przypisana jest nazwa "weather-currently-temp-strict"

    result = soup.find("div", {"class": "weather-currently-temp-strict"}).text

    # Pobrane dane przesylamy do funkcji checkValue, gdzie zostaja sprawdzone warunki ich poprawnosci

    value = checkValue(result)

    # Wypisujemy na ekran otrzymana temperature

    print('WEATHER IN CRACOW: ' + value)


def checkValue(result):

    # Sprawdzamy czy informacja, ktora pobralismy, nie jest pustym obiektem

    if result == 'None':
        return 'EMPTY INFO'

    # Sprawdzamy czy dane, ktore otrzymalismy sa podane w stopniach Celsjusza, uzywajac wyrazen regularnych
    # Szukamy dopasowania liczba + °C
    # Sprawdzamy czy zawiera co najmniej 1 liczbe

    match = re.search(r'\d+°C', result)
    if not match:
        return 'INFORMATION IS NOT A TEMPERATURE IN CELSIUS'

    # Tworzymy tymczasowego stringa ucinajac dwa ostatnie znaki, by otrzymac stringa zawierajacego same liczby

    temp = result[0:len(result) - 2]

    # Sprawdzamy czy string zawiera same liczby

    if not temp.isnumeric():
        return 'INFORMATION IS NOT A TEMPERATURE'

    # Sprawdzamy czy temperatura miesci sie w okreslonych progach

    if int(temp) < -30 | int(temp) > 40:
        return 'TEMPERATURE OUT OF BOUNDS'

    # Jezeli dane przeszly wszystkie testy, temperatura jest zwracana

    return result


if __name__ == '__main__':
    getInfo()
