from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor
import time, json

main_url = "https://anidb.net/anime/?h=1&noalias=1&orderby.name=0.1&page=100&type.movie=1&type.ova=1&type.tvseries=1&type.tvspecial=1&view=list"


def get_page_info(page_url):

    result_dict = {}
    print(f"Getting The Url : {page_url}")

    session = HTMLSession()
    r = session.get(page_url)

    matches = r.html.find("div.animelist_list table#animelist.animelist tbody tr", first=False)

    for match in matches:
        anime_title = match.find("td.name,main,anime", first=True).text
        anime_type = match.find("td.type,movie,tv_series", first=True).text
        anime_info_link = "https://anidb.net" + match.find("td.name a", first=True).attrs['href']

        result_dict[anime_title] = [anime_title, anime_info_link, anime_type]

        return result_dict

## Get the pages urls to visit
# session = HTMLSession()
# r = session.get(main_url)
#
# start_time = time.time()
#
#
# with open("anime_pages_urls.txt", 'a') as urls_fo:
#     urls_list = []
#     for html in r.html:
#         page_url = html.url
#         print(page_url)
#         urls_list.append(page_url)
#         urls_fo.flush()
#         urls_fo.write(page_url)
#         urls_fo.write("\n")

start_time = time.time()
urls_list = []
with open("anime_pages_urls.txt", 'r') as urls_fo:
    for url in urls_fo.readlines():
        url = url.split()[0]
        urls_list.append(url)

print(len(urls_list), urls_list)


## Pause wait for confirmation of recapture
input("Press Enter when ready to goto the next step...")

## Visit each page and get the data
main_result_dict = {}

with ThreadPoolExecutor(max_workers=25) as executor:
    results = executor.map(get_page_info, urls_list)

    for result in results:
        print("\tResult : ", result)
        for name, value in result:
            main_result_dict[name] = value

with open("anime_titles_reference.json", 'w') as dict_fo:
    json.dump(main_result_dict, dict_fo, indent=2, sort_keys=True)

print(f"Finished all ops in {time.time() - start_time} seconds")



