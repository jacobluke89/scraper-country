from typing import Any, Dict

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
from io import StringIO

dict_of_urls = {
    "pop_density": "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population_density",
    "pop_percent": "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population",
    "pop_by_age": "https://en.wikipedia.org/wiki/List_of_countries_by_age_structure",
    "mortality_inf_u_5": "https://en.wikipedia.org/wiki/List_of_countries_by_infant_and_under-five_mortality_rates",
    "literacy_rate": "https://en.wikipedia.org/wiki/List_of_countries_by_literacy_rate",  # gender gap shown here
    "GDP_PC": "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(PPP)_per_capita",
    "min_wage":  "https://en.wikipedia.org/wiki/List_of_countries_by_minimum_wage",
    "gini_coef": "https://en.wikipedia.org/wiki/List_of_countries_by_income_equality"
}

def get_wiki_page(url: str) -> Dict[Any, DataFrame]:

    page = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(page.content, 'html.parser')

    tables = soup.find_all('table', class_='wikitable')
    dict_of_dfs = {}
    for count, t in enumerate(tables):
        print(count)
        dict_of_dfs[count] = pd.read_html(StringIO(str(t)))[0]

    return dict_of_dfs
