import os

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from pprint import pprint
from requests_html import HTMLSession, HTML
from concurrent.futures import ThreadPoolExecutor
import json
import re
import math
import time
import urllib.parse
import requests
from .utils import *

eztv_season_R_expression = r'(S[0-9]+|[0-9]+x[0-9]+)'
eztv_episode_R_expression = r'(E[0-9]+|[0-9]+x[0-9]+)'
ROOT_DIR = f"{os.sep}".join(os.path.abspath(__file__).split(os.sep)[:-2])

## Load the settings
with open(os.path.join(ROOT_DIR, "src/settings.json"), "r") as fo: SETTINGS = json.load(fo)


class WorkerSignals(QObject):

    finished = Signal()
    finished_show = Signal()
    finished_tabulate = Signal(object)
    log_data = Signal(object)
    message_signal = Signal(object, object, object)


class EZTV:

    def __init__(self, central_widget: QWidget, limit=50):

        self.base_url = SETTINGS['tv-scrapers']['EZTV']
        self.limit = int(limit)
        self.max_workers = 20
        self.main_show_list = []
        self.central_widget = central_widget

    def get_show_by_imdb_id(self, imdb_id: str, signals: WorkerSignals = None) -> list:

        def get_page_show_details(url):
            try:
                r = requests.get(url)
                json_data = r.json()

                if json_data.get('torrents') is None:
                    log(f"[EZTV SCRAPER] [NO DATA ERROR] No data found for {url}")
                    signals.log_data.emit(f"[EZTV SCRAPER] [NO DATA ERROR] No data found for {url}")
                    signals.finished.emit()
                    return

                ## Get out the show data
                for movie in json_data['torrents']:
                    movie_dict = {}
                    movie_dict['title'] = movie['title']
                    movie_dict['torrent_url'] = movie['torrent_url']
                    movie_dict['magnet_url'] = movie['magnet_url']
                    movie_dict['imdb_id'] = movie['imdb_id']
                    movie_dict['season'] = movie['season']
                    movie_dict['episode'] = movie['episode']
                    movie_dict['seeds'] = movie['seeds']
                    movie_dict['peers'] = movie['peers']
                    movie_dict['small_screenshot'] = movie['small_screenshot']
                    movie_dict['size_bytes'] = convert_size(int(movie['size_bytes']))

                    self.main_show_list.append(movie_dict)
                    signals.log_data.emit(f"[EZTV SCRAPER] Found torrent! {movie['title']}")


                log(f"[EZTV SCRAPER] Done scraping url {url}")
                signals.log_data.emit(f"[EZTV SCRAPER] Done scraping url {url}")


            except Exception as e:
                log(f'[EZTV SCRAPER] Failed to start the scrape_torrent_info session, URL: {url}, Exception: {e}')
                signals.log_data.emit(f'[EZTV SCRAPER] Failed to start the scrape_torrent_info session, URL: {url}, Exception: {e}')


        ## Create the endpoint url
        imdb_id = int(imdb_id.replace('t', ''))
        endpoint_url = urllib.parse.urljoin(self.base_url, f"api/get-torrents?imdb_id={imdb_id}&limit={self.limit}&page=1")

        ## Get the number of pages to visit
        r = requests.get(endpoint_url)
        json_data = r.json()

        if json_data.get('torrents') is None:
            log(f"[EZTV SCRAPER] [ERROR] Could not get any torrents for url ==> {endpoint_url}")
            signals.log_data.emit(f"[EZTV SCRAPER] [ERROR] Could not get any torrents for url ==> {endpoint_url}")
            signals.finished.emit()
            return []

        pages_count = math.ceil(json_data['torrents_count'] / json_data['limit'])
        log(f"[EZTV SCRAPER] Visiting {pages_count} pages for the api for {endpoint_url}")
        signals.log_data.emit(f"[EZTV SCRAPER] Visiting {pages_count} pages for the api for {endpoint_url}")


        ## Create a list of urls to visit
        log(f"[EZTV SCRAPER] Creating a list of urls to visit...")
        signals.log_data.emit(f"[EZTV SCRAPER] Creating a list of urls to visit...")
        page_urls = []
        for i in range(1, pages_count+1):
            url = urllib.parse.urljoin(self.base_url, f"api/get-torrents?imdb_id={imdb_id}&limit={self.limit}&page={i}")
            page_urls.append(url)

        ## Creating the threadpool
        log("[EZTV SCRAPER] Creating the threadpool")
        signals.log_data.emit("[EZTV SCRAPER] Creating the threadpool")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            result = executor.map(get_page_show_details, page_urls)
            for results in result: pass

        signals.message_signal.emit(self.central_widget, f"Finished scraping! found {len(self.main_show_list)} torrents", 4)
        signals.finished.emit()
        signals.finished_tabulate.emit(self.main_show_list)
        pprint(self.main_show_list)
        return self.main_show_list




# x = EZTV()
# x.get_show_by_imdb_id("tt2442560")
