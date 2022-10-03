import json
from pprint import pprint
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor
import requests
import math

file_name = "yifi_movie_titles.json"
failed_path = "failed_yify.txt"
base_url = "https://yts.mx/api/v2/list_movies.json"
main_shows_dict = {}
MAX_WORKERS = 20
LIMIT = 50   # The limit number of results per query, default is 20 &limit=50

start_time = time()

## Get the number of pages to visit
print(f"Getting the number of pages to visit...")
r = requests.get(base_url + f"?page=1&limit={LIMIT}")
json_data = r.json()

if not json_data['status'] == 'ok':
    print(f"[RESPONSE NOT OK] Error. {json_data}")
    exit(1)

movie_count = json_data['data']['movie_count']
limit = json_data['data']['limit']
pages_count_o = math.ceil(movie_count / limit)
pages_count = 5 * round(pages_count_o / 5)

print(f"Visiting {pages_count} pages with each having {limit} movies each. MOVIE_COUNT = {movie_count}, ORIGINAL_PAGES = {pages_count_o}")

## Format the failed list
with open(failed_path, 'w') as fo: fo.write('')

def get_page_show_details(url):
    try:
        r = requests.get(url)
        json_data = r.json()

        if not json_data:
            print(f"[NO DATA ERROR] No data found for {url}")
            return

        ## Get out the show data
        movie_dict = {}
        for movie in json_data['data']['movies']:
            movie_dict[movie['title_english']] = movie['imdb_code']

        main_shows_dict.update(movie_dict)

        print(f"Done scraping url {url}")

    except Exception as e:
        print(f'Failed to start the scrape_torrent_info session, URL: {url}, Exception: {e}')
        with open(failed_path, 'a') as fo: fo.write(f"{url}\n")


## Create a list of urls to visit
print(f"Creating a list of urls to visit...")
page_urls = []
for i in range(pages_count):
    url = base_url + f"?page={i}&limit={LIMIT}"
    page_urls.append(url)

## Creating the threadpool
print("Creating the threadpool")
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    result = executor.map(get_page_show_details, page_urls)
    for results in result: pass

## Save the data to disk
print(f"Saving the data to disk..")
with open(file_name, 'w') as fo:
    json.dump(main_shows_dict, fo, indent=2, sort_keys=True)

print(f"Finished all operations in {time() - start_time} seconds")
print(f"Found {len(main_shows_dict.keys())} shows.")

