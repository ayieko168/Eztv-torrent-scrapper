from requests_html import HTMLSession, HTML
import re, json, math, time, string
from concurrent.futures import ThreadPoolExecutor

movie_title = "Fary... ed"
def get_torrent_data(url):
    return_dict = {}
    dict_count = 0

    session = HTMLSession()
    r = session.get(url)

    matches = r.html.find("div div.home_list_entry", first=False)

    for match in matches:

        try:
            size = match.find("div.size")[0].text
        except:
            size = ""

        try:
            seeds = match.find("div.links span[title]")[0].attrs['title'].split('/')[0].replace(':', '').strip(string.ascii_letters).strip()
        except:
            seeds = "-"

        try:
            magnet_link = [i for i in match.find("a[href]") if 'magnet' in i.attrs['href']][0].attrs['href']
        except:
            magnet_link = ""

        try:
            torrent_link = [i for i in match.find("a[href]") if '.torrent' in i.attrs['href']][0].attrs['href']
        except:
            torrent_link = ""

        try:
            torrent_title = match.find("div.link a")[0].text
        except:
            torrent_title = "NONE"

        season = ""
        episode = ""

        ## add item to dict
        return_dict[dict_count] = [movie_title, torrent_title, torrent_link, magnet_link, size, seeds, season,
                                   episode]
        dict_count += 1

    return return_dict



x = get_torrent_data("https://animetosho.org/search?q=Fairy%20Tail")

print(json.dumps(x, indent=2))




