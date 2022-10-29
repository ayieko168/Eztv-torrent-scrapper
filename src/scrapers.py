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

    def get_show_by_imdb_id(self, imdb_id: str, signals: WorkerSignals = None, keyword: str = "") -> list:

        self.main_show_list = []

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

            ## Add a contingency in case the id search didnt work
            log(f"\n\n[EZTV SCRAPER] [FALL BACK] Falling back to keyword search")
            signals.log_data.emit(f"[EZTV SCRAPER] [FALL BACK] Falling back to keyword search")
            if not self.main_show_list:
                self.main_show_list = self.get_show_by_name(show_name=keyword, signals=signals)

                signals.message_signal.emit(self.central_widget, f"Finished scraping! found {len(self.main_show_list)} torrents", 4)
                signals.finished.emit()
                signals.finished_tabulate.emit(self.main_show_list)

                return self.main_show_list

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

        ## Write the data to disk for future
        with open(os.path.join(ROOT_DIR, "src/results.json"), "w") as fo: json.dump(self.main_show_list, fo, indent=2)

        # pprint(self.main_show_list)
        return self.main_show_list

    def get_show_by_name(self, show_name: str, signals: WorkerSignals = None) -> list:

        self.main_show_list = []

        signals.log_data.emit("[EZTV SCRAPER - TITLE] Scraping using EZTV...")

        ## Rectify the search title
        show_name = show_name.lower().replace(' ', '-').strip()
        scrape_url = urllib.parse.urljoin(self.base_url, f"search/{show_name}")

        ## Start a session
        signals.log_data.emit(f"[EZTV SCRAPER - TITLE] Starting requests session... URL: {scrape_url}")
        session = HTMLSession()
        r = session.get(scrape_url)
        signals.log_data.emit("[EZTV SCRAPER - TITLE] Done establishing connection.")

        ## Start the scrape
        signals.log_data.emit("[EZTV SCRAPER - TITLE] Getting torrents...")
        show_elements = r.html.find("tr.forum_header_border", first=False)

        for match in show_elements:

            show_dictionary = {}

            try: seeders = match.find("td.forum_thread_post_end")[0].text
            except: seeders = ""

            try: size = match.find("td", first=False)[3].text
            except: size = ''

            try: magnet_link = match.find("a", first=False)[2].attrs['href']
            except: magnet_link = ''

            try: torrent_link = match.find("a", first=False)[3].attrs['href']
            except: torrent_link = ''

            try: eztv_title = match.find("a", first=False)[1].attrs['title']
            except: eztv_title = ''

            try:
                query_string = list(re.compile(r'([SE][0-9]+|[0-9]+x[0-9]+)').finditer(eztv_title))[0].group()

                if query_string.startswith("S"):
                    se_ep_ptring = list(re.compile(r'[SE][0-9]+').finditer(eztv_title))
                    season = se_ep_ptring[0].group().replace("S", "")
                    episode = se_ep_ptring[1].group().replace("E", "")
                elif len(query_string.split("x")) == 2:
                    se_ep_ptring = list(re.compile(r'[0-9]+x[0-9]+').finditer(eztv_title))
                    season = "{:02}".format(int(se_ep_ptring[0].group().split("x")[0]))
                    episode = se_ep_ptring[0].group().split("x")[1]
                else:
                    season = None
                    episode = None
            except:
                   season = "00"
                   episode = "00"

            ## Save the data
            show_dictionary['title'] = eztv_title
            show_dictionary['torrent_url'] = torrent_link
            show_dictionary['magnet_url'] = magnet_link
            show_dictionary['imdb_id'] = "tt"
            show_dictionary['season'] = season
            show_dictionary['episode'] = episode
            show_dictionary['seeds'] = seeders
            show_dictionary['peers'] = "00"
            show_dictionary['small_screenshot'] = ""
            show_dictionary['size_bytes'] = size

            self.main_show_list.append(show_dictionary)
            signals.log_data.emit(f"[EZTV SCRAPER - TITLE] Found torrent! {eztv_title}")

        ## Finish the scrape
        log(f"[EZTV SCRAPER - TITLE] Done scraping url {scrape_url}")
        signals.log_data.emit(f"[EZTV SCRAPER - TITLE] Done scraping url {scrape_url}")

        signals.message_signal.emit(self.central_widget, f"Finished scraping! found {len(self.main_show_list)} torrents", 4)
        signals.finished.emit()
        signals.finished_tabulate.emit(self.main_show_list)

        ## Write the data to disk for future
        with open(os.path.join(ROOT_DIR, "src/results.json"), "w") as fo: json.dump(self.main_show_list, fo, indent=2)

        # pprint(self.main_show_list)
        # return self.main_show_list



x = EZTV(QWidget)
# x.get_show_by_name("peaky blinders", WorkerSignals())
# x.get_show_by_imdb_id('tt2442560', WorkerSignals())
