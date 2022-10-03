import json
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor
import requests

# last_page = 0
# page_no = 260
last_page = 260
file_name = "tvmaze_show_titles.json"
base_url = "https://api.tvmaze.com/shows"
main_show_list = []
MAX_WORKERS = 10

start_time = time()


def get_page_show_details(url):
    try:
        r = requests.get(url)
        json_data = r.json()

        if not json_data:
            print(f"[NO DATA ERROR] No data found for {url}")
            return

        ## Get out the show data
        for show in json_data:
            shows_dict = {}
            shows_dict[show['name']] = show['externals']['imdb']
            main_show_list.append(shows_dict)

        print(f"Done scraping url {url}")

    except Exception as e:
        print(f'Failed to start the scrape_torrent_info session, URL: {url}, Exception: {e}')


## Create a list of urls to visit
page_urls = []
for i in range(last_page):
    url = base_url + f"?page={i}"
    page_urls.append(url)

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    result = executor.map(get_page_show_details, page_urls)
    for results in result: pass

## Save the data to disk
with open(file_name, 'w') as fo:
    json.dump(main_show_list, fo, indent=2, sort_keys=True)

print(f"\nFinished all operations in {time() - start_time} seconds")
print(f"Found {len(main_show_list)} shows.")







