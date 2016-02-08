from colorama import init, Fore
from requests import get, codes
from argparse import ArgumentParser
from json import loads
from collections import defaultdict
from urllib import quote

from bs4 import BeautifulSoup
from tabulate import tabulate

PAGE = "http://www.thesaurus.com/browse/%s?s=t"
COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN]


class NoResultException(Exception):
    pass


def is_okay(res):
    return res.status_code == codes.ok


def search(query):
    res = get(PAGE % quote(query))
    if not is_okay(res):
        raise NoResultException()
    return res.text


def find_synonyms(html):
    bs = BeautifulSoup(html, "lxml")

    mask = bs.find('div', class_="mask")
    synonym_groups = {}
    for tab in mask.find_all('strong', class_="ttl"):
        synonym_groups[tab.text] = defaultdict(list)

    relevancy_lists = bs.find_all('div', class_="relevancy-list")
    if relevancy_lists is None or not relevancy_lists or len(relevancy_lists) != len(synonym_groups):
        raise NoResultException()

    for idx, relevancy in enumerate(relevancy_lists):
        for common_word in relevancy.find_all('a'):
            category = int(loads(common_word["data-category"])["name"].split("relevant-")[1])
            synonym = common_word.find('span', class_="text").text
            synonym_groups[synonym_groups.keys()[idx]][category].append(synonym)

    return synonym_groups


def get_arguments():
    parser = ArgumentParser(description="A command line tool for thesaurus.com")
    parser.add_argument('q', help="Query to search for at thesaurus")
    args = parser.parse_args()

    if args.q is None:
        exit(1)
    return args.q


def present_synonyms(synonym_groups):
    table = defaultdict(list)
    for sg in sorted(synonym_groups.keys()):
        synonyms = synonym_groups[sg]
        table[sg] = [COLORS[category - 1] + word
                     for category in sorted(synonyms.keys(), reverse=True)
                     for word in sorted(synonyms[category])]

    print tabulate(table, headers="keys")


if __name__ == '__main__':
    init()
    html = search(get_arguments())
    synonym_groups = find_synonyms(html)
    present_synonyms(synonym_groups)