from requests_html import HTMLSession, HTML
import re

def get_torrents(movie_title=None, ez_id=None):
    """
    :returns > Dict containing torrent links.
        :keys = torrent result count (int)
        :values = [movie_title, ez_title, torrent_link, magnet_link, size, season, episode] (list)
    :keywords > movie_title=None OR ez_id=None
        A string containing the movie title or movie eztv ID, If None, exits.
    """

    return_dict = {}
    dict_count = 0

    if (movie_title is None) and (ez_id is None):
        raise Exception("Querry Error! Enter a valid movie title or id.")

    # movie_title = movie_title.replace(" ", "-")
    # scrape_url = "https://thepiratebay.org/search.php?q={}&all=on&search=Pirate+Search&page=0&orderby=".format(movie_title)
    scrape_url = "https://thepiratebay.org/search.php?q=peaky+blinders&cat=0"
    session = HTMLSession()
    r = session.get(scrape_url)
    script = """
            () => {
                return {
                    width: document.documentElement.clientWidth,
                    height: document.documentElement.clientHeight,
                    deviceScaleFactor: window.devicePixelRatio,
                }
            }
        """
    r.html.render(script=script, reload=True, sleep=20, timeout=25)

    # matches = r.html.find("tr.forum_header_border", first=True)

    print(r.html.html)

get_torrents("peaky blinders")


