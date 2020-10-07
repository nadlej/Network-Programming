# Piotr Przemielewski - Programowanie sieciowe

import requests
import json
import _collections
import sys


def personInfo():

    # Sprawdzamy, czy pobrane ID to ID zespolu, a nie artysty

    if 'members' not in y:
        print('IT IS NOT A BAND')
        sys.exit(1)

    # Pobieramy ilosc czlonkow zespolu

    size = len(y['members'])

    # Uruchamiamy funkcje do sprawdzania czy ilosc zapytan, ktore chcemy wykonac,
    # nie przekroczy rate limiting'u

    checkRequestAmount(size)

    # Wyodrebniamy id czlonkow zespolu

    for k in range(0, size):
        sth.append(y['members'][k]['id'])

    # Rozpoczynamy sprawdanie kazdego z uczesnikow zespolu

    for k in range(0, size):
        doRequest(sth[k])


def doRequest(person_id):
    person_url = 'https://api.discogs.com/artists/' + str(person_id)

    # Pobieramy dane sprawdzanego uczestnika

    person_text = requests.get(person_url).text

    # Zapisujemy je w formacie JSON

    y = json.loads(person_text)

    # Zapisujemy ilosc zespolow, w ktorych gral dany artysta

    num_groups = len(y['groups'])

    # W petli sprawdzamy czy artysta gral w zespole innym niz ten, ktorego ID podalismy na poczatku
    # Jezeli tak jest, zapisujemy nazwe zespolu do slownika jako klucz, a artyste jako wartosc
    # W razie, gdy nazwa danego zespolu wystepuje juz w slowniku, arysta jest dodawany do listy uczestnikow

    for k in range(0, num_groups):
        if not y['groups'][k]['name'] == bandName:
            if not y['groups'][k]['name'] in dic:
                b = y['groups'][k]['name']
                dic[b] = y['name']

            else:
                members = []
                old_mem = dic.get(y['groups'][k]['name'])

                if not str(type(old_mem)) == "<class 'list'>":
                    members.append(old_mem)
                else:
                    for m in old_mem:
                        members.append(m)

                members.append(y['name'])
                b = y['groups'][k]['name']
                dic[b] = members


def getInfo():
    # Sortujemy slownik, tak aby zespoly byly wyswietlane wzgledem nazwy

    sort_dic = _collections.OrderedDict(sorted(dic.items()))

    key_set = sort_dic.keys()

    # W petli rozpoczynamy wyswietlanie danego zespolu wraz z artystami, ktorzy nalezeli do zespolu podanego na poczatku
    # Rekordy, ktore nie sa listami (czyli < 2 czlonkow zespolu w nim gralo) sa odrzucane

    for x in key_set:
        if not str(type(dic.get(x))) == "<class 'str'>":
            print(x + ": ")
            members = dic.get(x)
            for k in members:
                print(k)
            print()


def checkStatus():
    # Sprawdzamy czy status strony jest == 200 oraz czy strona jest w formacie json

    if not result.status_code == 200:
        print('WRONG STATUS CODE')
        sys.exit(1)

    if not result.headers['Content-Type'] == 'application/json':
        print('IT IS NOT A JSON PAGE')
        sys.exit(1)


def checkRequestAmount(size):
    # Sprawdzamy, czy ilosc requestow, ktore chcemy wykonac, nie przekroczy limitu ustalonego przez strone

    limit = result.headers['X-Discogs-Ratelimit-Remaining']

    if size > int(limit) + 1:
        print('TOO MANY REQUESTS, WAIT A FEW SECONDS')
        sys.exit(1)


if __name__ == '__main__':
    # Pobieramy nazwe zespolu

    bandID = input("Podaj ID zespolu: ")

    # Pobieramy status pobranej strony

    URL = 'https://api.discogs.com/artists/' + str(bandID)
    result = requests.get(URL)

    # Sprawdzamy status pobranej strony

    checkStatus()

    # Pobieramy zawartosc strony

    result_text = requests.get(URL).text

    # Zapisujemy dane w formacie JSON

    y = json.loads(result_text)

    # Tworzymy slownik i tablice, ktore posluza nam w przyszlosci do pozyskania interesujacych nas danych

    sth = []
    dic = {}

    # Wyodrebniamy nazwe zespolu

    bandName = y['name']

    # Rozpoczynamy dzialanie dwoch glownych funkcji

    personInfo()
    getInfo()
