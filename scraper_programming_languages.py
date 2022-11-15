# by Matias I. Bofarull Oddo - 2022.10.30

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, unquote_plus

rest_API = "https://en.wikipedia.org/api/rest_v1/page/html/"
param_API = "?redirect=true&stash=false"
url_regex = re.compile(r"\/page\/html\/(.*?)[\?|^]")
influenced_by_regex = re.compile(r"Influenced\s*(?:\s*<.*?>\s*){0,2}\s*by")


def scrape_programming_languages(root_href):

    dict_wikigraph = {}

    def wikiscrape_infobox(page_href):

        try:

            if page_href not in dict_wikigraph:
                dict_wikigraph[page_href] = {}

            sesh = requests.Session()
            page = sesh.get(
                rest_API + quote_plus(page_href) + param_API,
                timeout=100,
            )
            url_match = url_regex.search(page.url)
            true_href = unquote_plus(url_match.group(1))

            soup = BeautifulSoup(page.content, "html.parser")
            infobox_HTML = soup.find("table", {"class": "infobox"})
            infobox_rows = [row.prettify() for row in infobox_HTML.find_all("tr")]

            row_index = 0
            data_strings = {
                "incoming": "",
                "outgoing": "",
            }

            # Parsing for the "programming languages" infobox template

            for row in infobox_rows:
                if influenced_by_regex.search(row) or "Influences" in row:
                    data_strings["incoming"] += infobox_rows[row_index]
                    data_strings["incoming"] += infobox_rows[row_index + 1]
                elif "Influenced" in row:
                    data_strings["outgoing"] += infobox_rows[row_index]
                    data_strings["outgoing"] += infobox_rows[row_index + 1]
                row_index += 1

            data_incoming = BeautifulSoup(
                data_strings["incoming"],
                "html.parser",
            )
            list_incoming = [
                str(a["href"])[2:]
                for a in data_incoming.find_all(
                    "a",
                    {"rel": True},
                )
            ]

            data_outgoing = BeautifulSoup(
                data_strings["outgoing"],
                "html.parser",
            )
            list_outgoing = [
                str(a["href"])[2:]
                for a in data_outgoing.find_all(
                    "a",
                    {"rel": True},
                )
            ]

            if page_href in dict_wikigraph:

                dict_wikigraph[page_href]["incoming"] = list_incoming
                dict_wikigraph[page_href]["outgoing"] = list_outgoing
                dict_wikigraph[page_href]["true_href"] = true_href
                dict_wikigraph[page_href]["match"] = str(page_href == true_href)

                print()
                print(page_href)
                print(true_href, "[" + str(page_href == true_href) + "]")
                print(list_incoming)
                print(list_outgoing)

            list_href = sorted(set(list_incoming + list_outgoing))
            for href in list_href:
                if href not in dict_wikigraph:
                    wikiscrape_infobox(href)

        except Exception as error_message:
            print()
            print("FAILED [" + page_href + "]")
            print("ERROR: " + str(error_message))

    wikiscrape_infobox(root_href)

    return dict_wikigraph
