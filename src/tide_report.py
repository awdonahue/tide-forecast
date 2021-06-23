import time
import requests
from typing import List
from bs4 import BeautifulSoup
from bs4.element import ResultSet

import configs
from utils import build_tide_urls

def scrape_tides(location_urls: List[tuple]) -> List[ResultSet]:
    """ Scrape data from tide web site: https://www.tide-forecast.com

    :param location_urls: Full urls to tide forecast locations

    :return: List of BeautifulSoup ResultSet
    """
    results = []
    for url in location_urls:
        res = requests.get(url[0])

        # If url not found, use alt url without state
        if res.status_code == 404:
            res = requests.get(url[1])

        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            results.append(soup.find('div', class_=configs.TIDES_TABLE_NAME))

    return results

def build_tide_report(tide_results: List[ResultSet]) -> None:
    """ Parse ResultSet for tide data and build List of dictionaries for report

    :param tide_results: ResultSet from BeautifulSoup based on urls
    """
    # Tables each have a cell for Sun/Moon times

    # Parse results of locations
    for tide_result in tide_results:
        # Parse each day tide table for location
        tide_day_table = tide_result.find_all('div', class_='tide-day')
        for day in tide_day_table:
            # Header info for location and date
            report = f'{day.find("h4", class_="tide-day__date").text}\n'

            # Get daylight time
            sun_moon_table = day.find('table', class_='not-in-print tide-day__sun-moon')

            sunrise_time_str = list(sun_moon_table.find('tr').children)[configs.RISES_COLUMN['sunrise']].find('span', class_='tide-day__value').text.lstrip()
            sunset_time_str = list(sun_moon_table.find('tr').children)[configs.RISES_COLUMN['sunset']].find('span', class_='tide-day__value').text.lstrip()
            sunrise_time = time.strptime(sunrise_time_str, '%I:%M%p')
            sunset_time = time.strptime(sunset_time_str, '%I:%M%p')

            tides_table = day.find('table', class_='tide-day-tides')
            for row in tides_table.find_all('tr'):
                tide = list(row.children)

                if tide[configs.TIDE_COLUMN['type']].text.lower() == 'low tide':
                    low_tide_time = tide[configs.TIDE_COLUMN['time']].find('b').text.lstrip()
                    low_tide_height = tide[configs.TIDE_COLUMN['height']].find('b', class_='js-two-units-length-value__primary').text

                    # TODO FIX website uses %H for midnight (00) and %I (12) for all other times, thus breaking midnight tide times...
                    # Add daylight times and heights
                    if sunrise_time < time.strptime(low_tide_time, '%H:%M %p') < sunset_time:
                        report += 'Low Tide during day:\n'
                        report += f' Time: {low_tide_time}\n'
                        report += f' Height: {low_tide_height}\n'

            print(report)


## Run the script and build tide report
if __name__ == '__main__':
    urls = build_tide_urls(configs.TIDES_URL, configs.LOCATIONS, configs.TIDES_LATEST_PATH)

    results = scrape_tides(urls)
    if results:
        build_tide_report(results)
    else:
        SystemExit('No results found for urls supplied')
