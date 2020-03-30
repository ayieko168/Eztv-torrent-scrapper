from bs4 import BeautifulSoup
import urllib.request
import json
from time import sleep, time
from ast import literal_eval

last_page = 0
page_no = 195



for curent_page in range(last_page, page_no+1):
    print(f"moving to page {curent_page}")
    url = f"http://api.tvmaze.com/shows?page={curent_page}"
    main_dictionary = {}
    data = {}

    try:
        print(f"downloadong web page info of page {curent_page}...")
        hdr = {"User-Agent": "Mozila/5.0"}
        res = urllib.request.urlopen(url)
        res_body = res.read()

        responce_list = json.loads(res_body.decode("utf-8")) # a list of dictionaries containig show info

        for show_info in responce_list:
            QUERY_NAME = show_info["name"].lower().replace(" ", "-")
            NAME = show_info["name"]
            IMDB_ID = show_info["externals"]["imdb"]
            IMAGE_LINKS = show_info["image"]
            SCHEDULE = show_info["schedule"]
            PRMERE = show_info["premiered"]
            RUNTIME = show_info["runtime"]
            SHOW_STATUS = show_info["status"]
            GENRE = show_info["genres"]

            
            data[QUERY_NAME] = {"name": NAME,
                                "imdb_id": IMDB_ID,
                                "image_links": IMAGE_LINKS,
                                "genre": GENRE,
                                "status": SHOW_STATUS,
                                "schedule": SCHEDULE,
                                "premere": PRMERE,
                                "runtime": SHOW_STATUS
                                }

        with open("TVMAZE_REFERENCE_DICTIONARY.json", "r") as ffo:
            read_dict = json.load(ffo)

        merged_dictionaries = {**read_dict, **data}

        with open("TVMAZE_REFERENCE_DICTIONARY.json", "w") as tvmazeFO:
            json.dump(merged_dictionaries, tvmazeFO, indent=2)

        print(f"done quering page {curent_page}")

    except Exception as e:
        print(e.args)
    