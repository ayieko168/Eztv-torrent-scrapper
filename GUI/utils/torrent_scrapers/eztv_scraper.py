from requests_html import HTMLSession, HTML
import re

season_R_expression = r'(S[0-9]+|[0-9]+x[0-9]+)'
episode_R_expression = r'(E[0-9]+|[0-9]+x[0-9]+)'


def get_torrents(movie_title=None, ez_id=None):
    """
    :keywords > movie_title=None OR ez_id=None
        A string containing the movie title or movie eztv ID, If None, exits.
    :returns > Dict containing torrent links.
        :keys = torrent result count (int)
        :values = [searched_title, ez_title, torrent_link, magnet_link, size, seeders, season, episode] (list)

    """

    return_dict = {}
    dict_count = 0

    if (movie_title is None) and (ez_id is None):
        # raise Exception("Querry Error! Enter a valid movie title or id.")
        return return_dict, dict_count, False

    if movie_title is not None:
        scrape_url = "https://eztv.io/search/{}".format(movie_title)
        searched_title = movie_title
    elif (ez_id is not None) and (type(ez_id) == int):
        scrape_url = f"https://eztv.io/search/?q1=&q2={ez_id}&search=Search"
        searched_title = HTMLSession().get(f"https://eztv.io/shows/{ez_id}/").html.url.split("/")[-2].replace("-", " ").title()
    else:
        return return_dict, dict_count, False

    session = HTMLSession()
    r = session.get(scrape_url)
    # r.html.render(timeout=20)

    matches = r.html.find("tr.forum_header_border", first=False)

    for match in matches:

        # seeders = match.find("td.forum_thread_post_end")[0].text
        # size = match.find("td", first=False)[3].text
        # magnet_link = match.find("a", first=False)[2].attrs['href']
        # torrent_link = match.find("a", first=False)[3].attrs['href']
        # eztv_title = match.find("a", first=False)[1].attrs['title']
        # season = list(re.compile(r'S[0-9]+').finditer(eztv_title))[0][0].replace("S", "")
        # episode = list(re.compile(r'E[0-9]+').finditer(eztv_title))[0][0].replace("E", "")

        try:
            seeders = match.find("td.forum_thread_post_end")[0].text
        except:
            seeders = ""

        try:
            size = match.find("td", first=False)[3].text
        except:
            size = ''

        try:
            magnet_link = match.find("a", first=False)[2].attrs['href']
        except:
            magnet_link = ''

        try:
            torrent_link = match.find("a", first=False)[3].attrs['href']
        except:
            torrent_link = ''

        try:
            eztv_title = match.find("a", first=False)[1].attrs['title']
        except:
            eztv_title = ''

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

        ## add item to dict

        return_dict[dict_count] = [searched_title, eztv_title, torrent_link, magnet_link, size, seeders, season, episode]
        dict_count += 1

        print(f"\n"
              f"Title = {searched_title}\n"
              f"Eztv Title = {eztv_title}\n"
              f"Season = {season}\n"
              f"Episode = {episode}\n"
              f"Torrent Link = {torrent_link}\n"
              f"Magnet Link = {magnet_link[:50]} ...\n"
              f"Size = {size}\n"
              f"Seeders = {seeders}")

    print("\n\tDictionary count = ", dict_count)

    return return_dict, dict_count, True



# print(get_torrents(ez_id=1))
# get_torrents(ez_id=2055)
# get_torrents("Game Of Thrones")


