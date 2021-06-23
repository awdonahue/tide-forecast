from typing import List

def build_tide_urls(url: str, locations: List[str], path: str) -> List[tuple]:
    """ Build tides URL based on area and state

    :param url: Base url for tides page
    :param locations: List of tuples. Format: [(area: str, state: str),]
    :param path: url path to latest tide forecasts

    :return urls: List of tuple urls, with and without state in the url
    """
    urls = []
    for location in locations:
        urls.append((
            f'{url}/{location[0]}-{location[1]}/{path}',
            f'{url}/{location[0]}/{path}'
        ))

    return urls
