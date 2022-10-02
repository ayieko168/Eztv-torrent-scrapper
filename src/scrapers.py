from requests_html import HTMLSession, HTML
from concurrent.futures import ThreadPoolExecutor
import json
import re
import math
import time

eztv_season_R_expression = r'(S[0-9]+|[0-9]+x[0-9]+)'
eztv_episode_R_expression = r'(E[0-9]+|[0-9]+x[0-9]+)'


def eztv_scraper(signals, movie_title=None, ez_id=None, print_output=False):
    """
    :keywords : movie_title=None OR ez_id=None
        A string containing the movie title or movie eztv ID, If None, exits.
    :returns : > Dict containing torrent links.
                    :keys = torrent result count (int)
                    :values = [searched_title, ez_title, torrent_link, magnet_link, size, seeders, season, episode] (list)
               > The number of torrents found
               > Weather the scrape was successful

    """

    signals.log_data.emit("Application", "")
    signals.log_data.emit("eztv", "Scraping using EZTV...")

    return_dict = {}
    dict_count = 0

    if (movie_title is None) and (ez_id is None):
        # raise Exception("Querry Error! Enter a valid movie title or id.")
        signals.log_data.emit("eztv[ERROR]", "Query Error! Enter a valid movie title or id.")
        return return_dict, dict_count, False

    if movie_title is not None:
        scrape_url = "https://eztv.re/search/{}".format(movie_title)
        searched_title = movie_title
        signals.log_data.emit("eztv", f"scrape url set to : {scrape_url} for searched title : {searched_title}")
    elif (ez_id is not None) and (type(ez_id) == int):
        scrape_url = f"https://eztv.re/search/?q1=&q2={ez_id}&search=Search"
        searched_title = HTMLSession().get(f"https://eztv.re/shows/{ez_id}/").html.url.split("/")[-2].replace("-", " ").title()
        scrape_url = f"https://eztv.re/shows/{ez_id}/{searched_title.lower().replace(' ', '-')}/"
        signals.log_data.emit("eztv", f"scrape url set to : {scrape_url} for searched title : {searched_title}")
    else:
        return return_dict, dict_count, False

    signals.log_data.emit("eztv", "Starting requests session...")
    session = HTMLSession()
    r = session.get(scrape_url)
    signals.log_data.emit("eztv", "Done establishing connection.")

    matches = r.html.find("tr.forum_header_border", first=False)

    signals.log_data.emit("eztv", "Getting torrents...")
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

        signals.log_data.emit("eztv", f"found a torrent : {eztv_title}, currently found {dict_count} results.")


    if print_output:
        print(json.dumps(return_dict, indent=2))
        print(f"\n\tDictionary count = {dict_count}\n\tDictionary Key count = {len(return_dict.keys())}")

    signals.log_data.emit("eztv", f"Finished scraping for torrents. Found {len(return_dict.keys())} torrents for {searched_title}")

    return return_dict, dict_count, True


def kick_ass_scraper_tv(signals, movie_title=None, print_output=False):

    """Use thereadpool to open the next pages"""

    signals.log_data.emit("Application", "")
    signals.log_data.emit("kickass(tv)", "Scraping using kickass(tv)...")

    def fetch(page_url):
        ## Get torrent data from all pages
        return_dict = {}
        dict_count = 0

        signals.log_data.emit("kickass(tv)", f"[worker- {page_url}] = working on {page_url}")

        scrape_url = page_url
        searched_title = movie_title

        ## Create the requests session
        signals.log_data.emit("kickass(tv)", f"[worker- {page_url}] = Starting requests session...")
        main_session = HTMLSession()
        r_main = main_session.get(scrape_url, timeout=40)

        ## Start scraping for data
        signals.log_data.emit("kickass(tv)", f"[worker- {page_url}] = Done. Now getting torrent matches...")
        matches = r_main.html.find("tr.even,tr.odd", first=False)

        for match in matches:

            # get the magnet link
            torrent_page_url = match.find("a.cellMainLink", first=True).attrs['href']
            torrent_page_url = "https://kickasstorrents.to" + torrent_page_url
            if print_output: print(f"getting magnet link from {torrent_page_url}")
            session2 = HTMLSession()
            r2 = session2.get(torrent_page_url, timeout=40)

            # Magnet link
            try:
                magnet_link = r2.html.find("a.kaGiantButton", first=True).attrs['href']
            except Exception as e:
                if print_output: print(e)
                signals.log_data.emit("kickass(tv)[ERROR]", f"[worker- {page_url}] = Error getting magnet link: {e}")
                magnet_link = ''

            # Torrent Title
            try:
                torrent_title = match.find("a.cellMainLink", first=True).text
            except Exception as e:
                if print_output: print(e)
                signals.log_data.emit("kickass(tv)[ERROR]", f"[worker- {page_url}] = Error getting torrent link: {e}")
                torrent_title = ''

            # Size
            try:
                size = match.find("td.nobr", first=True).text
            except Exception as e:
                if print_output: print(e)
                signals.log_data.emit("kickass(tv)[ERROR]", f"[worker- {page_url}] = Error getting size: {e}")
                size = ''

            # seeders
            try:
                seeders = match.find("td.green", first=True).text
            except Exception as e:
                if print_output: print(e)
                signals.log_data.emit("kickass(tv)[ERROR]", f"[worker- {page_url}] = Error getting seeders: {e}")
                seeders = ''

            # Season And Episode
            try:
                query_string = list(re.compile(r'([SE][0-9]+|[0-9]+x[0-9]+)').finditer(torrent_title))[0].group()

                if query_string.startswith("S"):
                    se_ep_ptring = list(re.compile(r'[SE][0-9]+').finditer(torrent_title))
                    season = se_ep_ptring[0].group().replace("S", "")
                    episode = se_ep_ptring[1].group().replace("E", "")
                elif len(query_string.split("x")) == 2:
                    se_ep_ptring = list(re.compile(r'[0-9]+x[0-9]+').finditer(torrent_title))
                    season = "{:02}".format(int(se_ep_ptring[0].group().split("x")[0]))
                    episode = se_ep_ptring[0].group().split("x")[1]
                else:
                    season = None
                    episode = None
            except Exception as e:
                season = ''
                episode = ''

            ## add item to dict
            return_dict[dict_count] = [movie_title, torrent_title, torrent_page_url, magnet_link, size, seeders, season,
                                       episode]
            dict_count += 1

            signals.log_data.emit("kickass(tv)", f"[worker- {page_url}] = found torrent : {torrent_title}, currently the {dict_count}'th torrent.")

        return return_dict, dict_count, True

    final_result_dict = {}
    count = 0

    signals.log_data.emit("kickass(tv)", "Getting a list of the result pages to visit..."
                                         "")
    ## generagte list of pages to visit
    start_time = time.time()

    signals.log_data.emit("kickass(tv)", "Started process...")
    if print_output: print("Started process")
    main_url = "https://kickasstorrents.to/search/{}/category/tv/1/".format(movie_title)
    signals.log_data.emit("kickass(tv)", f"scrape url set to : {main_url} for searched title : {movie_title}")
    signals.log_data.emit("kickass(tv)", "Getting pages...")
    if print_output: print("getting pages")
    main_session = HTMLSession()
    r_main = main_session.get(main_url)
    count_str = r_main.html.find("tr td a.plain", first=True).text
    if count_str == 'omikrosgavri':
        signals.log_data.emit("kickass(tv)", "omikrosgavri error, found 0 torrents")
        return final_result_dict, count, False
    page_count = math.ceil(int(count_str.split(" ")[-1]) / int(count_str.split(" ")[-3].split('-')[1]))
    pages_list = [main_url.replace(main_url.split('/')[-2], str(i)) for i in range(1, page_count + 1)]
    if print_output: print(f"Scrapping {page_count} pages")
    signals.log_data.emit("kickass(tv)", f"Scrapping {page_count} pages")

    if print_output: print("Starting thread-pool...")
    signals.log_data.emit("kickass(tv)", "Starting thread-pool using 25 workers...")
    with ThreadPoolExecutor(max_workers=25) as executor:
        results = executor.map(fetch, pages_list)

    signals.log_data.emit("kickass(tv)", "All threads are done working, combining individual results to one...")
    try:
        for result in results:
            for val in result[0].values():
                final_result_dict[count] = val
                count += 1
    except Exception as e:
        signals.log_data.emit("kickass(tv)[ERROR]", f"Exception, error = {e}")
        if print_output:
            print("Exception, error = ", e)
        else:
            pass

    if print_output:
        print(json.dumps(final_result_dict, indent=2))
        print(f"Finished all ops in {time.time() - start_time} seconds")
        print("Done")

    signals.log_data.emit("kickass(tv)", f"Finished all ops in {time.time() - start_time} seconds, found {len(final_result_dict.keys())} torrents")

    return final_result_dict, count, True
