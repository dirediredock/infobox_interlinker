# by Matias I. Bofarull Oddo - 2022.10.30

import json
from scraper_psychologists import scrape_psychologists
from scraper_programming_languages import scrape_programming_languages

href_seed = "Carl_Jung"

dict_wikigraph = scrape_psychologists(href_seed)
with open("network_data_" + href_seed + ".json", "w") as json_file:
    json.dump(dict_wikigraph, json_file, sort_keys=True, indent=4)

href_seed = "Fortran"

dict_wikigraph = scrape_programming_languages(href_seed)
with open("network_data_" + href_seed + ".json", "w") as json_file:
    json.dump(dict_wikigraph, json_file, sort_keys=True, indent=4)
