from requests_html import HTMLSession, HTML
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import re, json, math, time, string, datetime, os
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QTextCursor

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
        scrape_url = "https://eztv.io/search/{}".format(movie_title)
        searched_title = movie_title
        signals.log_data.emit("eztv", f"scrape url set to : {scrape_url} for searched title : {searched_title}")
    elif (ez_id is not None) and (type(ez_id) == int):
        scrape_url = f"https://eztv.io/search/?q1=&q2={ez_id}&search=Search"
        searched_title = HTMLSession().get(f"https://eztv.io/shows/{ez_id}/").html.url.split("/")[-2].replace("-", " ").title()
        scrape_url = f"https://eztv.io/shows/{ez_id}/{searched_title.lower().replace(' ', '-')}/"
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


def kick_ass_scraper_anime(signals, movie_title=None, print_output=False):

    """Use thereadpool to open the next pages"""

    signals.log_data.emit("Application", "")
    signals.log_data.emit("kickass(anime)", "Scraping using kickass(anime)...")

    def fetch(page_url):
        ## Get torrent data from all pages
        return_dict = {}
        dict_count = 0

        # print(f"working on {page_url}")
        signals.log_data.emit("kickass(anime)", f"[worker- {page_url}] = working on {page_url}")

        scrape_url = page_url
        searched_title = movie_title

        ## Create the requests session
        signals.log_data.emit("kickass(anime)", f"[worker- {page_url}] = Starting the requests session...")
        main_session = HTMLSession()
        r_main = main_session.get(scrape_url, timeout=40)

        ## Start scraping for data
        signals.log_data.emit("kickass(anime)", f"[worker- {page_url}] = session successfully established, now getting torrent matches...")
        matches = r_main.html.find("tr.even,tr.odd", first=False)

        for match in matches:

            # get the magnet link
            torrent_page_url = match.find("a.cellMainLink", first=True).attrs['href']
            torrent_page_url = "https://kickasstorrents.to" + torrent_page_url
            # print(f"getting magnet link from {torrent_page_url}")
            session2 = HTMLSession()
            r2 = session2.get(torrent_page_url, timeout=40)

            # Magnet link
            try:
                magnet_link = r2.html.find("a.kaGiantButton", first=True).attrs['href']
            except Exception as e:
                if print_output: print(e)
                signals.log_data.emit("kickass(anime)[ERROR]", f"[worker- {page_url}] = Error getting magnet link: {e}")
                magnet_link = ''

            # Torrent Title
            try:
                torrent_title = match.find("a.cellMainLink", first=True).text
            except Exception as e:
                if print_output: print(e)
                signals.log_data.emit("kickass(anime)[ERROR]", f"[worker- {page_url}] = Error getting magnet link: {e}")
                torrent_title = ''

            # Size
            try:
                size = match.find("td.nobr", first=True).text
            except Exception as e:
                if print_output: print(e)
                signals.log_data.emit("kickass(anime)[ERROR]", f"[worker- {page_url}] = Error getting magnet link: {e}")
                size = ''

            # seeders
            try:
                seeders = match.find("td.green", first=True).text
            except Exception as e:
                if print_output: print(e)
                signals.log_data.emit("kickass(anime)[ERROR]", f"[worker- {page_url}] = Error getting magnet link: {e}")
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

            signals.log_data.emit("kickass(anime)", f"[worker- {page_url}] = found torrent : {torrent_title}")

        return return_dict, dict_count, True

    final_result_dict = {}
    count = 0

    ## generagte list of pages to visit
    signals.log_data.emit("kickass(anime)", f"getting a list of all torrent results pages to scrape...")
    start_time = time.time()

    if print_output: print("Started process")
    signals.log_data.emit("kickass(anime)", f"Started process...")
    main_url = "https://kickasstorrents.to/search/{}/category/anime/1/".format(movie_title)
    signals.log_data.emit("kickass(anime)", f"scrape url set to : {main_url} for searched title : {movie_title}")
    if print_output: print("getting pages")
    signals.log_data.emit("kickass(anime)", f"getting pages...")
    main_session = HTMLSession()
    r_main = main_session.get(main_url)
    count_str = r_main.html.find("tr td a.plain", first=True).text
    if count_str == 'omikrosgavri':
        signals.log_data.emit("kickass(anime)", f"omikrosgavri error, found 0 torrens")
        return final_result_dict, count, False
    page_count = math.ceil(int(count_str.split(" ")[-1]) / int(count_str.split(" ")[-3].split('-')[1]))
    pages_list = [main_url.replace(main_url.split('/')[-2], str(i)) for i in range(1, page_count + 1)]
    if print_output: print(f"Scrapping {page_count} pages")
    signals.log_data.emit("kickass(anime)", f"Scrapping {page_count} pages.")

    if print_output: print("Starting threadpool...")
    signals.log_data.emit("kickass(anime)", f"starting thread-pool with 25 workers")
    with ThreadPoolExecutor(max_workers=25) as executor:
        results = executor.map(fetch, pages_list)

    try:
        for result in results:
            for val in result[0].values():
                final_result_dict[count] = val
                count += 1
    except Exception as e:
        signals.log_data.emit("kickass(anime)[ERROR]", f"Error, exception : {e}")
        if print_output: print("Exception, error = ", e)
        else:
            pass

    if print_output:
        print(json.dumps(final_result_dict, indent=2))
        print(f"Finished all ops in {time.time() - start_time} seconds")
        print("Done")

    signals.log_data.emit("kickass(anime)", f"Finished all ops in {time.time() - start_time} seconds, found {len(final_result_dict.keys())} torrents.")

    return final_result_dict, count, True


def kick_ass_scraper_all(torrent_name=None, print_output=False):

    def fetch(page_url):
        ## Get torrent data from all pages
        return_dict = {}
        dict_count = 0

        print(f"working on {page_url}\n")

        scrape_url = page_url
        searched_title = torrent_name

        ## Create the requests session
        main_session = HTMLSession()
        r_main = main_session.get(scrape_url, timeout=40)

        ## Start scraping for data
        matches = r_main.html.find("tr.even,tr.odd", first=False)

        for match in matches:

            # get the magnet link
            torrent_page_url = match.find("a.cellMainLink", first=True).attrs['href']
            torrent_page_url = "https://kat.am/usearch/" + torrent_page_url
            print(f"getting magnet link from {torrent_page_url}")
            session2 = HTMLSession()
            r2 = session2.get(torrent_page_url, timeout=40)

            # Magnet link
            try:
                magnet_link = r2.html.find("a.kaGiantButton", first=True).attrs['href']
            except Exception as e:
                print(e)
                magnet_link = ''

            # Torrent Title
            try:
                torrent_title = match.find("a.cellMainLink", first=True).text
            except Exception as e:
                print(e)
                torrent_title = ''

            # Size
            try:
                size = match.find("td.nobr", first=True).text
            except Exception as e:
                print(e)
                size = ''

            # seeders
            try:
                seeders = match.find("td.green", first=True).text
            except Exception as e:
                print(e)
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
            return_dict[dict_count] = [torrent_name, torrent_title, torrent_page_url, magnet_link, size, seeders, season,
                                       episode]
            dict_count += 1

        return return_dict, dict_count, True

    final_result_dict = {}
    count = 0

    ## generagte list of pages to visit
    start_time = time.time()

    if print_output: print("Started process")
    main_url = "https://kat.am/search/{}/".format(torrent_name)
    if print_output: print("getting pages")
    main_session = HTMLSession()
    r_main = main_session.get(main_url)
    count_str = r_main.html.find("tr td a.plain", first=True).text
    if count_str == 'omikrosgavri':
        return final_result_dict, count, False
    page_count = math.ceil(int(count_str.split(" ")[-1]) / int(count_str.split(" ")[-3].split('-')[1]))
    pages_list = [main_url.replace(main_url.split('/')[-2], str(i)) for i in range(1, page_count + 1)][:50]
    if print_output: print(f"Scrapping {page_count} pages")

    if print_output: print("Starting threadpool...")
    with ThreadPoolExecutor(max_workers=25) as executor:
        results = executor.map(fetch, pages_list)

    try:
        for result in results:
            for val in result[0].values():
                final_result_dict[count] = val
                count += 1
    except Exception as e:
        if print_output: print("Exception, error = ", e)
        else:
            pass

    if print_output:
        print(json.dumps(final_result_dict, indent=2))
        print(f"Finished all ops in {time.time() - start_time} seconds")
        print("Done")

    return final_result_dict, count, True


def nyaa_scraper(signals, movie_title=None, print_output=False):

    """
    :keywords : movie_title=None
        A string containing the movie title or movie eztv ID, If None, exits.
    :returns : > Dict containing torrent links.
                    :keys = torrent result count (int)
                    :values = [searched_title, ez_title, torrent_link, magnet_link, size, seeders, season, episode] (list)
               > The number of torrents found
               > Weather the scrape was successful

    """

    signals.log_data.emit("Application", "")
    signals.log_data.emit("nyaa", "Scraping using nyaa...")

    final_result_dict = {}
    count = 0

    if movie_title is None:
        # raise Exception("Querry Error! Enter a valid movie title")
        signals.log_data.emit("nyaa[Error]", "Query Error! Enter a valid movie title.")
        return final_result_dict, count, False

    if movie_title is not None:
        scrape_url = f"https://nyaa.si/?f=0&c=0_0&q={movie_title}"
        searched_title = movie_title
        signals.log_data.emit("nyaa", f"scrape url set to : {scrape_url} for searched title : {searched_title}")
        # print(scrape_url)
    else:
        return final_result_dict, count, False

    ## Get the number of pages to visit
    signals.log_data.emit("nyaa", f"getting the number of pages to visit...")
    pagnation_session = HTMLSession()
    pagnation_request = pagnation_session.get(scrape_url)
    t = pagnation_request.html.find("div.pagination-page-info", first=True).text
    results_count = int(list(re.finditer(r'of [0-9]+ results', t))[0].group().split(" ")[1])
    per_page_count = int(list(re.finditer(r'results [0-9]+-[0-9]+ out', t))[0].group().split(" ")[1].split("-")[1])
    try:total_pages = math.ceil(results_count/per_page_count)
    except: total_pages = 1
    if print_output: print(total_pages)
    signals.log_data.emit("nyaa", f"Done, Number of pages to be visited : {total_pages}.")


    ## Generate a list of result page urls
    signals.log_data.emit("nyaa", f"generating a list of urls (from the parent url) to visit...")
    pages_urls = [f"https://nyaa.si/?f=0&c=0_0&q={movie_title}&p={page}" for page in range(1, total_pages + 1)]
    signals.log_data.emit("nyaa", f"done, pages list = {pages_urls}")

    def get_page_data(page_url):

        signals.log_data.emit("nyaa", f"[worker - {page_url}] = working on {page_url}")

        return_dict = {}
        dict_count = 0

        signals.log_data.emit("nyaa", f"[worker - {page_url}] = starting requests session...")
        session = HTMLSession()
        r = session.get(page_url)

        signals.log_data.emit("nyaa", f"[worker - {page_url}] = done, now getting all torrent matches")
        matches = r.html.find("div.table-responsive tbody tr", first=False)

        for match in matches:

            ## Get the title
            try: torrent_title = match.find("td:not(.text-center) a:not(.comments)", first=False)[-1].attrs['title']
            except: torrent_title = " "

            ## Get The Magnet Link
            try: magnet_link = match.find("td.text-center", first=False)[0].find('a')[1].attrs['href']
            except: magnet_link = " "

            ## Get The .torrent link
            try: torrent_link = " "
            except: torrent_link = " "

            ## Get size
            try: size = match.find("td.text-center", first=False)[1].text
            except: size = " "

            ## Get the seeders
            try: seeders = match.find("td.text-center", first=False)[3].text
            except: seeders = " "

            ## Get season:
            try: season = " "
            except: season = " "

            ## Get Episode:
            try: episode = " "
            except: episode = " "

            return_dict[dict_count] = [movie_title, torrent_title, torrent_link, magnet_link, size, seeders, season, episode]
            dict_count += 1

            signals.log_data.emit("nyaa", f"[worker - {page_url}] = Found torrent : {torrent_title}, currently the {dict_count}'th torrent.")

        return return_dict, dict_count, True

    ## Start the threadpool executor
    signals.log_data.emit("nyaa", f"starting the thread-pool...")
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(get_page_data, pages_urls)

    try:
        signals.log_data.emit("nyaa", f"(Try loop) Combining restored info")
        for result in results:
            for val in result[0].values():
                final_result_dict[count] = val
                count += 1
    except Exception as e:
        signals.log_data.emit("nyaa[error]", f"Exception : {e}")
        if print_output: print("Exception, error = ", e)
        else:
            pass

    if print_output:
        print(json.dumps(final_result_dict, indent=2))
        print(f"Finished all ops in {time.time() - start_time} seconds")
        print(f"Found {count} items")
        print("Done")

    signals.log_data.emit("nyaa", f"Done with all operations in {time.time() - start_time} seconds, found {len(final_result_dict.keys())} torrents.")

    return final_result_dict, count, True


def anime_tosho_scraper(signals, movie_title=None, print_output=False):


    signals.log_data.emit("Application", "")
    signals.log_data.emit("anime-tosho", f"Scraping using anime tosho...")

    final_result_dict = {}
    count = 0
    start_time = time.time()

    if movie_title is None:
        # raise Exception("Querry Error! Enter a valid movie title")
        signals.log_data.emit("anime-tosho", f"Query Error! Enter a valid movie title")
        return final_result_dict, count, False
    else:
        scrape_url = f"https://animetosho.org/search?q={movie_title.replace(' ', '%20')}"
        searched_title = movie_title
        signals.log_data.emit("anime-tosho", f"scrape url set to : {scrape_url} for the search title : {searched_title}")

    ## Get The List Of pages available using pagination
    signals.log_data.emit("anime-tosho", f"Getting the list of pages available for pagination...")
    if print_output:
        print("Getting The Pagination Pages")

    paginarion_session = HTMLSession()
    r = paginarion_session.get(scrape_url)
    pages_list = [html.url for html in r.html]  # A list Of Result pages
    signals.log_data.emit("anime-tosho", f"Done, pagination pages url list = {pages_list}")
    # pages_list = ["https://animetosho.org/search?q=Fairy%20Tail", "https://animetosho.org/search?q=Fairy%20Tail&page=2", "https://animetosho.org/search?q=Fairy%20Tail&page=3", "https://animetosho.org/search?q=Fairy%20Tail&page=4"]

    ## Construct The Info Getting Function
    def get_torrent_data(url):
        return_dict = {}
        dict_count = 0

        signals.log_data.emit("anime-tosho", f"[worker - {url}] = Working on url : {url}.")

        signals.log_data.emit("anime-tosho", f"[worker - {url}] = starting requests session...")
        session = HTMLSession()
        r = session.get(url)

        signals.log_data.emit("anime-tosho", f"[worker - {url}] = Done, now getting the torrent matches...")
        matches = r.html.find("div div.home_list_entry", first=False)

        for match in matches:

            try:
                size = match.find("div.size")[0].text
            except:
                size = ""

            try:
                seeds = match.find("div.links span[title]")[0].attrs['title'].split('/')[0].replace(':', '').strip(
                    string.ascii_letters).strip()
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
            signals.log_data.emit("anime-tosho", f"[worker - {url}] = found torrent : {torrent_title}")

        return return_dict

    ## Get torrent info from each paginatied page
    signals.log_data.emit("anime-tosho", f"getting torrent info from each pagination page...")
    if print_output:
        print("Now getting the torrent data from each paginated page")
    signals.log_data.emit("anime-tosho", f"starting thread-pool using 25 workers")
    with ThreadPoolExecutor(max_workers=25) as executor:
        results = executor.map(get_torrent_data, pages_list)

    ## Merge the individual page results to one final dictionary
    signals.log_data.emit("anime-tosho", f"merging individual worker results into one...")
    if print_output:
        print("Now Merging pages results to final dictionary copy")
    try:
        for result in results:
            for val in result.values():
                final_result_dict[count] = val
                count += 1
    except Exception as e:
        signals.log_data.emit("anime-tosho[error]", f"exception : {e}")
        if print_output: print("Exception, error = ", e)
        else:
            pass

    if print_output:
        print(json.dumps(final_result_dict, indent=2))
        print(f"Finished all ops in {time.time() - start_time} seconds")
        print(f"Found {count} items")
        print("Done")

    signals.log_data.emit("anime-tosho", f"Finished all operations in {time.time() - start_time} seconds, and found {len(final_result_dict.keys())} torrents")

    return final_result_dict, count, True


def yify_movie_scraper(signals, movie_title=None, print_output=False):

    signals.log_data.emit("Application", "")
    signals.log_data.emit("yify(movies)", f"Scraping using yify movies...")

    final_result_dict = {}
    count = 0

    if movie_title is None:
        signals.log_data.emit("yify(movies)", f"Query Error! Enter a valid movie title")
        return final_result_dict, count, False
    else:
        start_time = time.time()
        corected_movie_title = movie_title.lower().replace(' ', '%20').replace('-', '%20')
        url = f"https://yts.mx/browse-movies/{corected_movie_title}/all/all/0/latest/0/all"
        signals.log_data.emit("yify(movies)", f"Scrape url set to : {url} for search title : {movie_title}")


    def fetch_data(url):

        signals.log_data.emit("yify(movies)", f"[worker - {url}] = working on {url}")
        result_dict = {}

        signals.log_data.emit("yify(movies)", f"[worker - {url}] = staring requests session...")
        session = HTMLSession()
        r = session.get(url)

        signals.log_data.emit("yify(movies)", f"[worker - {url}] = done, now getting torrent matches...")
        matches = r.html.find("div.modal-torrent", first=False)

        count = 0
        for match in matches:
            torrent_name = match.find("a.download-torrent", first=True).attrs['title'].replace("Download", "").strip()
            magnet_link = match.find("a.magnet", first=True).attrs['href']
            torrent_link = match.find("a.button-green-download2-big", first=True).attrs['href']
            size = match.find("p.quality-size", first=False)[-1].text
            movie_mode = match.find("p.quality-size", first=True).text
            seeders = 999
            season = ""
            episode = ""
            searched_title = ""

            torrent_name = f"{torrent_name} - {movie_mode}"

            result_dict[count] = [searched_title, torrent_name, torrent_link, magnet_link, size, seeders, season,
                                  episode]
            count += 1

            signals.log_data.emit("yify(movies)", f"[worker - {url}] = found torrent : {torrent_name}, currently found {count} torrents")

        return result_dict

    ## Get the list of movie results
    signals.log_data.emit("yify(movies)", f"getting the list of pagination urls...")
    session = HTMLSession()
    r = session.get(url)

    if print_output:
        print("Getting the list of movie results...")

    movie_result_list = [movie.attrs['href'] for movie in r.html.find("div.row div.browse-movie-wrap a.browse-movie-link", first=False)]
    signals.log_data.emit("yify(movies)", f"done getting pagination url list, list = {movie_result_list}")


    if print_output:
        print("List of movies found : ", movie_result_list)

    ## Now visit each movie url and get torrent data
    signals.log_data.emit("yify(movies)", f"Now visit each movie url and get torrent data.")
    if print_output:
        print("Now visit each movie url and get torrent data")

    signals.log_data.emit("yify(movies)", f"Starting thread-pool with 25 workers...")
    with ThreadPoolExecutor(max_workers=25) as executor:
        results = executor.map(fetch_data, movie_result_list)

    signals.log_data.emit("yify(movies)", f"Done getting individual torrents, now merging into one result dictionary...")
    try:
        for result in results:
            for val in result.values():
                val[0] = movie_title.title()
                final_result_dict[count] = val
                count += 1
    except Exception as e:
        signals.log_data.emit("yify(movies)[error]", f"exception : {e}")
        if print_output: print("Exception, error = ", e)
        else:
            pass

    if print_output:
        print(json.dumps(final_result_dict, indent=2))
        print(f"Finished all ops in {time.time() - start_time} seconds")
        print(f"Found {count} items")
        print("Done")

    signals.log_data.emit("yify(movies)", f"Finished all operations in {time.time() - start_time} seconds, found {len(final_result_dict.keys())} torrents.")

    return final_result_dict, count, True


def open_subs_scraper(signals, movie_path=None, print_output=False, directory=False):

    signals.log_data.emit("Application", "")
    signals.log_data.emit("OpenSubs", f"Scraping using Open-Subtitles...")

    start_time = time.time()
    final_result_dict = {}
    count = 0

    def get_str_info(file_path):
        ost = OpenSubtitles()
        token = ost.login(int(64084487842968137541007709925799131749).to_bytes(math.ceil(int(64084487842968137541007709925799131749).bit_length() / 8), 'little').decode(), int(546355688029801288302918137390656857).to_bytes(math.ceil(int(546355688029801288302918137390656857).bit_length() / 8), 'little').decode())

        result_dict = {}
        signals.log_data.emit("OpenSubs", f"Token assigned is {token}")

        signals.log_data.emit("OpenSubs", f"Getting file data for file at path : {file_path}...")

        f = File(file_path)
        data = ost.search_subtitles([{'sublanguageid': 'eng', 'moviehash': f.get_hash(), 'moviebytesize': f.size}])

        signals.log_data.emit("OpenSubs", f"File data acquisition successful.")

        count = 0
        for match in data:
            search_path = os.path.basename(file_path)
            sub_name = match['SubFileName']
            sub_size = match['SubSize']
            sub_seeders = match['SubDownloadsCnt']
            sub_zip_link = match['ZipDownloadLink']
            sub_link = match['SubtitlesLink']

            result_dict[count] = [search_path, sub_name, sub_link, sub_zip_link, sub_size, sub_seeders]
            count+=1

            signals.log_data.emit("OpenSubs", f"Found subtitle : {sub_name}")

        return result_dict

    if directory:

        ## Get the list of files in the directory
        movie_list = os.listdir(movie_path)

        movie_abs_path_list = [os.path.join(movie_path, movie) for movie in movie_list]

        with ThreadPoolExecutor(max_workers=25) as executor:
            results = executor.map(get_str_info, movie_abs_path_list)

            try:
                for result in results:
                    for val in result.values():
                        val[0] = os.path.basename(movie_path).title()
                        final_result_dict[count] = val
                        count += 1
            except Exception as e:
                signals.log_data.emit("OpenSubs[error]", f"exception : {e}")
                if print_output: print("Exception, error = ", e)
                else:
                    pass

        return final_result_dict, count, True

    else:
        final_result_dict = get_str_info(file_path=movie_path)
        count = len(final_result_dict.keys())

        if print_output:
            print(json.dumps(final_result_dict, indent=2))
            print(f"Finished all ops in {time.time() - start_time} seconds")
            print(f"Found {count} items")
            print("Done")

        signals.log_data.emit("OpenSubs", f"Finished all operations in {time.time() - start_time} seconds, found {len(final_result_dict.keys())} subtitles.")
        return final_result_dict, count, True

class WorkerSignals(QObject):

    finished = pyqtSignal()
    log_data = pyqtSignal(object, object)
    message_signal = pyqtSignal(object)

my_signals = WorkerSignals()

# open_subs_scraper(my_signals, movie_path=r"C:\Users\royalstate\Movies\Series\The Spy", print_output=True, directory=True)
# kick_ass_scraper_all(torrent_name="ben", print_output=True)
# anime_tosho_scraper(signals, "Fairy Tail", print_output=True)
# kick_ass_scraper(movie_title="peaky blinders", print_output=True)
# eztv_scraper(my_signals, movie_title="100", print_output=True)
# nyaa_scraper(movie_title="Dr stone", print_output=True)




