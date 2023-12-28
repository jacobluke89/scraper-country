from typing import Any, Dict

from pandas import DataFrame

from data_cleanser.scraper import get_wiki_page
from data_cleanser.data_cleaner import data_cleaner
from logger.logger import message_logger

dict_of_wiki_urls = {
    "pop_density": "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population_density",
    "pop_percent": "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population",
    "pop_by_age": "https://en.wikipedia.org/wiki/List_of_countries_by_age_structure",
    "mortality_inf_u_5": "https://en.wikipedia.org/wiki/List_of_countries_by_infant_and_under-five_mortality_rates",
    "literacy_rate": "https://en.wikipedia.org/wiki/List_of_countries_by_literacy_rate",  # gender gap shown here
    "GDP_PC": "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(PPP)_per_capita",
    "min_wage":  "https://en.wikipedia.org/wiki/List_of_countries_by_minimum_wage",
    "gini_coef": "https://en.wikipedia.org/wiki/List_of_countries_by_income_equality"
}


def obtain_clean_data(dict_of_urls=None) -> Dict[Any, dict[Any, DataFrame]]:
    if dict_of_urls is None:
        dict_of_urls = dict_of_wiki_urls
    dict_of_df = {}
    for k, v in dict_of_urls.items():
        try:
            df = get_wiki_page(v)
            print(df)
            df = data_cleaner(df)
            dict_of_df[k] = df
            print(f'{v} passed!')
        except Exception as e:
            message_logger(f'{k} failed, Error: {e}')
    return dict_of_df
