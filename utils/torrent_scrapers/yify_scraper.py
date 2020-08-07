from requests_html import HTMLSession, HTML
from collections import OrderedDict
import urllib.parse
import bencode
import re, json

def get_size(torrent_link):

    r = HTMLSession().get('https://yts.mx/torrent/download/295D6D644F4D40E9909E5736AFE178DBBEF320D9')
    torrent_content = bencode.decode(r.content)
    del torrent_content['info']
    print(torrent_content['info']['files'])
    # print(json.dumps(torrent_content, sort_keys=True, indent=2))


def get_torrents(searched_title):
    """
    :keywords > movie_title=None OR ez_id=None
        A string containing the movie title or movie eztv ID, If None, exits.
    :returns > Dict containing torrent links.
        :keys = torrent result count (int)
        :values = [searched_title, ez_title, torrent_link, magnet_link, size, seeders, season, episode] (list)

    """

    tracker_list = ['udp://open.demonii.com:1337/announce', 'udp://tracker.openbittorrent.com:80', 'udp://tracker.coppersurfer.tk:6969', 'udp://glotorrents.pw:6969/announce', 'udp://tracker.opentrackr.org:1337/announce', 'udp://torrent.gresille.org:80/announce', 'udp://p4p.arenabg.com:1337', 'udp://tracker.leechersparadise.org:6969']

    scrape_url = f"https://yts.mx/browse-movies/{searched_title}/all/all/0/latest/all"
    session = HTMLSession()
    r = session.get(scrape_url)

    ## visit all result pages
    for html in r.html:
        result_links = html.find("a.browse-movie-link", first=False)
        ## get all the movie links
        for result_link in result_links:
            link = result_link.attrs['href']
            # print(f"Scraping {link}")
            ## Visit the movie link
            r2 = session.get(link)
            matches = r2.html.find("p.hidden-xs.hidden-sm", first=False)
            ## Loop over every download button
            for match in matches:
                for match in match.find("a"):
                    torrent_link = match.attrs['href']
                    hash = match.attrs['href'].split("/")[-1]
                    title = match.attrs['title']
                    year = link.split("/")[-1].split("-")[-1]
                    resolution = title.replace("Download", "").replace("Torrent", "").strip().split(" ")[-1]
                    inc_title = title.replace("Download", "").replace("Torrent", "").replace(resolution, "").strip()
                    complete_title = f"{inc_title} ({year}) [{resolution}] [YTS.LT]"
                    encoded_title = urllib.parse.quote_plus(complete_title)
                    size = 0
                    seeders = 0

                    magnet_link = f"magnet:?xt=urn:btih:{hash}&dn={encoded_title}&"+"tr=".join(tracker_list)

                    print((link, magnet_link, torrent_link))
                    print()




get_size("f")


