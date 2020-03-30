from bs4 import BeautifulSoup
from urllib.request import Request, urlopen  # Python 3
import json
from time import sleep, time
from ast import literal_eval
import os

last_page = 241
page_no = 400
data = {}

file_siz = os.path.getsize("YIFY_REFERENCE_DICTIONARY.json")*1e-6
print(f"current filesize = {file_siz} MB")


for curent_page in range(last_page, page_no+1):
    print(f"moving to page {curent_page}")
    url = f"https://yts.mx/api/v2/list_movies.json?limit=50&page={curent_page}&sort_by=title"
    
    try:
        print(f"downloadong web page info of page {curent_page} out of {page_no}")
       
        req = Request(url)
        req.add_header("User-Agent", "Mozila/5.0")
        res_body = urlopen(req).read()

        responce_list = json.loads(res_body.decode("utf-8")) # a list of dictionaries containig show info
        responce_list = responce_list["data"]["movies"]

        for show_info in responce_list:

            QUERY_NAME = show_info["slug"].lower().replace(" ", "-")
            NAME = show_info["title_english"]
            IMDB_ID = show_info["imdb_code"]
            YOUTUBE_ID = show_info["yt_trailer_code"]
            YEAR = show_info["year"]
            RUNTIME = show_info["runtime"]
            GENRE = show_info["genres"]
            YIFY_URL = show_info["url"]
            TORRENTS = show_info["torrents"]
            IMAGE_LINKS = show_info["large_cover_image"]

            data[QUERY_NAME] = {"name": NAME,
                                "imdb_id": IMDB_ID,
                                "youtube_id": YOUTUBE_ID,
                                "year": YEAR,
                                "runtime": RUNTIME,
                                "genre": GENRE,
                                "yify_url": YIFY_URL,
                                "torrents_url": TORRENTS,
                                "image_urls": IMAGE_LINKS
                                }

        if len(data.keys()) >= 4000:
            print("################# writting memory data to file... ##############")

            with open("YIFY_REFERENCE_DICTIONARY.json", "r") as ffo:
                read_dict = json.load(ffo)

            merged_dictionaries = {**read_dict, **data}

            with open("YIFY_REFERENCE_DICTIONARY.json", "w") as tvmazeFO:
                json.dump(merged_dictionaries, tvmazeFO, indent=2)
            
            data = {}

        print(f"done quering page {curent_page}... keys length = {len(data.keys())}\n")

    except Exception as e:
        print(f"*******ERROR WITH PAGE {curent_page} :: ERROR = {e} *******\n", )

    if curent_page == 400:
        
        print("################# writting memory data to file... ##############")

        with open("YIFY_REFERENCE_DICTIONARY.json", "r") as ffo:
            read_dict = json.load(ffo)

        merged_dictionaries = {**read_dict, **data}

        with open("YIFY_REFERENCE_DICTIONARY.json", "w") as tvmazeFO:
            json.dump(merged_dictionaries, tvmazeFO, indent=2)
        
        
        file_siz = os.path.getsize("YIFY_REFERENCE_DICTIONARY.json")*1e-6
        print(f"total titles = {len(merged_dictionaries.keys())} , totla file size = {file_siz} MB")
        print("shutting down...")



    