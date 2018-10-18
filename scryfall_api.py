import requests


class ScryfallAPIError(Exception):
    pass


class CardNotFound(ScryfallAPIError):
    pass


def _url(path):
    return 'https://api.scryfall.com/' + path


def search_card(card_name):
    r = requests.get(_url('/cards/named'), params={'exact': card_name})

    if r.status_code == 404:
        raise CardNotFound("Card \"{}\" was not found on Scryfall API".format(
            card_name
        ))
    elif r.status_code != 200:
        raise ScryfallAPIError(
            "Unknown error when searching for \"{}\" : {}".format(card_name,
                                                               r.text))
    else:
        return r.json()
