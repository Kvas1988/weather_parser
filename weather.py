import requests as r
import json
import pandas as pd
from datetime import datetime, time, timedelta
from city import City
from wcalendar import Calendar
from pydantic import parse_file_as
from time import sleep
from tqdm import tqdm

# from sqlalchemy import create_engine, except_


class WeatherParser():
    def __init__(self):
        # TODO: export to config
        self.history_url: str= "https://archive-api.open-meteo.com/v1/archive?&daily=weathercode,temperature_2m_max,temperature_2m_min,temperature_2m_mean&timezone=Europe%2FMoscow"
        #"latitude=55.0415&longitude=82.9346&start_date=2023-09-10&end_date=2023-09-24"

    def get_history(self, city: City, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        self.city = city
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        params = f"&latitude={city.lat}&longitude={city.lng}&start_date={start_date_str}&end_date={end_date_str}"
        url = self.history_url + params
        tqdm.write(url)
        response = r.get(url)

        if response.status_code != 200:
            msg = f"{city.city_name} {start_date_str} - {end_date_str}:\nAPI response status code: {response.status_code}"
            raise RuntimeError(msg)
        # with open('data.json', 'w') as f:
        #     json.dump(response.json(), f)
        df = self.parse_data(response.json())
        df['city'] = city.city_name
        return df

    def parse(self, fname: str):
        with open(fname, 'r') as f:
            data = json.load(f)
            self.parse_data(data)

    def parse_data(self, data: dict):
        df = pd.DataFrame(data['daily'])
        return df


def get_cities(fname: str):
    with open(fname, 'r') as f:
        return json.load(f)


def parse_history(cities: list[City], cln: Calendar):
    wp = WeatherParser()
    it = 0

    for rng in tqdm(cln):
        for city in tqdm(cities):
            try:
                history = wp.get_history(city, rng.start_date, rng.end_date)
                dt = rng.start_date.strftime("%Y_%m")
                xlfile = f"{city.city_name}_{dt}.xlsx"
                history.to_excel(xlfile, index=False)
            except Exception as e:
                tqdm.write(repr(e))

            sleep(1)
            it += 1
            if it > 9000:
                tqdm.write(">9000 API requests made. Terminating")
                quit()


def main():
    cities = parse_file_as(list[City], "cities.json")
    cln = Calendar(backlog=True)
    parse_history(cities, cln)


if __name__ == "__main__":
    main()
