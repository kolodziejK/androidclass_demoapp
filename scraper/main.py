import requests
from bs4 import BeautifulSoup


def pobierz_liczbe_stron(url):
    """Pobiera liczbę stron z nawigatora."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    nawigator = soup.find('nav', class_='page-navigator')
    linki = nawigator.find_all('a')

    liczba_stron = len(linki)

    return liczba_stron


def pobierz_numery_pracownikow(url):
    """Pobiera numery pracowników z tabeli na stronie."""
    numery_pracownikow = []

    for strona in range(1, pobierz_liczbe_stron(url) + 1):
        url_strony = f"{url}?page={strona}"
        response = requests.get(url_strony)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            if link['href'].startswith('/person/'):
                numer_pracownika = link['href'].split('/')[-2]
                numery_pracownikow.append(numer_pracownika)

    return numery_pracownikow


def pobierz_dane_pracownika(numer_pracownika):
    """Pobiera dane pracownika za pomocą API."""
    url_api = f"https://ludzie-dev.wmi.amu.edu.pl/api/getPerson?id={numer_pracownika}"
    response = requests.get(url_api)
    soup = BeautifulSoup(response.text, 'html.parser')

    imie_nazwisko = soup.find('h2', class_='person__name')

    lista_danych = soup.find('ul', class_='person__list')
    email = lista_danych.find('li', class_='person__list__item-mail')
    phone = lista_danych.find('li', class_='person__list__item-tel')

    return {
        'imie_nazwisko': imie_nazwisko.text.strip() if imie_nazwisko else None,
        'email': email.text.strip() if email else None,
        'phone': phone.text.strip() if phone else None
    }


def main():
    url_strony = "https://ludzie-dev.wmi.amu.edu.pl/"
    numery_pracownikow = pobierz_numery_pracownikow(url_strony)

    for numer in numery_pracownikow:
        dane_pracownika = pobierz_dane_pracownika(numer)
        print(f"Dane pracownika {numer}:")
        print(f"Imię i nazwisko: {dane_pracownika['imie_nazwisko']}")
        print(f"Email: {dane_pracownika['email']}")
        print(f"Telefon: {dane_pracownika['phone']}")
        print("\n")


if __name__ == "__main__":
    main()
