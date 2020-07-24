from requests_html import HTMLSession, HTML
import re, json, math, time, string
from concurrent.futures import ThreadPoolExecutor

eztv_season_R_expression = r'(S[0-9]+|[0-9]+x[0-9]+)'
eztv_episode_R_expression = r'(E[0-9]+|[0-9]+x[0-9]+)'

# all functions here must return :returns : > Dictionary of:
#                                                :keys = torrent result count (int)
#                                                :values = [searched_title, torrent_title, torrent_link, magnet_link, size, seeders, season, episode] (list)
#                                            > The number of torrents found
#                                            > Weather the scrape was successful


def eztv_scraper(movie_title=None, ez_id=None, print_output=False):
    """
    :keywords : movie_title=None OR ez_id=None
        A string containing the movie title or movie eztv ID, If None, exits.
    :returns : > Dict containing torrent links.
                    :keys = torrent result count (int)
                    :values = [searched_title, ez_title, torrent_link, magnet_link, size, seeders, season, episode] (list)
               > The number of torrents found
               > Weather the scrape was successful

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
        scrape_url = f"https://eztv.io/shows/{ez_id}/{searched_title.lower().replace(' ', '-')}/"
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

    if print_output:
        print(json.dumps(return_dict, indent=2))
        print(f"\n\tDictionary count = {dict_count}\n\tDictionary Key count = {len(return_dict.keys())}")

    return return_dict, dict_count, True


def kick_ass_scraper_tv(movie_title=None, print_output=False):

    """Use thereadpool to open the next pages"""

    def fetch(page_url):
        ## Get torrent data from all pages
        return_dict = {}
        dict_count = 0

        print(f"working on {page_url}")

        scrape_url = page_url
        searched_title = movie_title

        ## Create the requests session
        main_session = HTMLSession()
        r_main = main_session.get(scrape_url, timeout=40)

        ## Start scraping for data
        matches = r_main.html.find("tr.even,tr.odd", first=False)

        for match in matches:

            # get the magnet link
            torrent_page_url = match.find("a.cellMainLink", first=True).attrs['href']
            torrent_page_url = "https://kickasstorrents.to" + torrent_page_url
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
            return_dict[dict_count] = [movie_title, torrent_title, torrent_page_url, magnet_link, size, seeders, season,
                                       episode]
            dict_count += 1

        return return_dict, dict_count, True

    final_result_dict = {}
    count = 0

    ## generagte list of pages to visit
    start_time = time.time()

    if print_output: print("Started process")
    main_url = "https://kickasstorrents.to/search/{}/category/tv/1/".format(movie_title)
    if print_output: print("getting pages")
    main_session = HTMLSession()
    r_main = main_session.get(main_url)
    count_str = r_main.html.find("tr td a.plain", first=True).text
    if count_str == 'omikrosgavri':
        return final_result_dict, count, False
    page_count = math.ceil(int(count_str.split(" ")[-1]) / int(count_str.split(" ")[-3].split('-')[1]))
    pages_list = [main_url.replace(main_url.split('/')[-2], str(i)) for i in range(1, page_count + 1)]
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


def kick_ass_scraper_anime(movie_title=None, print_output=False):

    """Use thereadpool to open the next pages"""

    def fetch(page_url):
        ## Get torrent data from all pages
        return_dict = {}
        dict_count = 0

        print(f"working on {page_url}")

        scrape_url = page_url
        searched_title = movie_title

        ## Create the requests session
        main_session = HTMLSession()
        r_main = main_session.get(scrape_url, timeout=40)

        ## Start scraping for data
        matches = r_main.html.find("tr.even,tr.odd", first=False)

        for match in matches:

            # get the magnet link
            torrent_page_url = match.find("a.cellMainLink", first=True).attrs['href']
            torrent_page_url = "https://kickasstorrents.to" + torrent_page_url
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
            return_dict[dict_count] = [movie_title, torrent_title, torrent_page_url, magnet_link, size, seeders, season,
                                       episode]
            dict_count += 1

        return return_dict, dict_count, True

    final_result_dict = {}
    count = 0

    ## generagte list of pages to visit
    start_time = time.time()

    if print_output: print("Started process")
    main_url = "https://kickasstorrents.to/search/{}/category/anime/1/".format(movie_title)
    if print_output: print("getting pages")
    main_session = HTMLSession()
    r_main = main_session.get(main_url)
    count_str = r_main.html.find("tr td a.plain", first=True).text
    if count_str == 'omikrosgavri':
        return final_result_dict, count, False
    page_count = math.ceil(int(count_str.split(" ")[-1]) / int(count_str.split(" ")[-3].split('-')[1]))
    pages_list = [main_url.replace(main_url.split('/')[-2], str(i)) for i in range(1, page_count + 1)]
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


def nyaa_scraper(movie_title=None, print_output=False):

    """
    :keywords : movie_title=None
        A string containing the movie title or movie eztv ID, If None, exits.
    :returns : > Dict containing torrent links.
                    :keys = torrent result count (int)
                    :values = [searched_title, ez_title, torrent_link, magnet_link, size, seeders, season, episode] (list)
               > The number of torrents found
               > Weather the scrape was successful

    """

    final_result_dict = {}
    count = 0

    if movie_title is None:
        # raise Exception("Querry Error! Enter a valid movie title")
        return final_result_dict, count, False

    if movie_title is not None:
        scrape_url = f"https://nyaa.si/?f=0&c=0_0&q={movie_title}"
        searched_title = movie_title
        print(scrape_url)
    else:
        return final_result_dict, count, False

    ## Get the number of pages to visit
    pagnation_session = HTMLSession()
    pagnation_request = pagnation_session.get(scrape_url)
    t = pagnation_request.html.find("div.pagination-page-info", first=True).text
    results_count = int(list(re.finditer(r'of [0-9]+ results', t))[0].group().split(" ")[1])
    per_page_count = int(list(re.finditer(r'results [0-9]+-[0-9]+ out', t))[0].group().split(" ")[1].split("-")[1])
    try:total_pages = math.ceil(results_count/per_page_count)
    except: total_pages = 1
    if print_output: print(total_pages)


    ## Generate a list of result page urls
    pages_urls = [f"https://nyaa.si/?f=0&c=0_0&q={movie_title}&p={page}" for page in range(1, total_pages + 1)]

    def get_page_data(page_url):
        return_dict = {}
        dict_count = 0

        session = HTMLSession()
        r = session.get(page_url)

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

        return return_dict, dict_count, True

    ## Start the threadpool executor
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(get_page_data, pages_urls)

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
        print(f"Found {count} items")
        print("Done")

    return final_result_dict, count, True


def anime_tosho_scraper(movie_title=None, print_output=False):

    final_result_dict = {}
    count = 0
    start_time = time.time()

    if movie_title is None:
        # raise Exception("Querry Error! Enter a valid movie title")
        return final_result_dict, count, False
    else:
        scrape_url = f"https://animetosho.org/search?q={movie_title.replace(' ', '%20')}"
        searched_title = movie_title

    ## Get The List Of pages available using pagination
    if print_output:
        print("Getting The Pagination Pages")
    paginarion_session = HTMLSession()
    r = paginarion_session.get(scrape_url)
    pages_list = [html.url for html in r.html]  # A list Of Result pages
    # pages_list = ["https://animetosho.org/search?q=Fairy%20Tail", "https://animetosho.org/search?q=Fairy%20Tail&page=2", "https://animetosho.org/search?q=Fairy%20Tail&page=3", "https://animetosho.org/search?q=Fairy%20Tail&page=4"]

    ## Construct The Info Getting Function
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

        return return_dict

    ## Get torrent info from each paginatied page
    if print_output:
        print("Now getting the torrent data from each paginated page")
    with ThreadPoolExecutor(max_workers=25) as executor:
        results = executor.map(get_torrent_data, pages_list)

    ## Merge the individual page results to one final dictionary
    if print_output:
        print("Now Merging pages results to final dictionary copy")
    try:
        for result in results:
            for val in result.values():
                final_result_dict[count] = val
                count += 1
    except Exception as e:
        if print_output: print("Exception, error = ", e)
        else:
            pass

    if print_output:
        print(json.dumps(final_result_dict, indent=2))
        print(f"Finished all ops in {time.time() - start_time} seconds")
        print(f"Found {count} items")
        print("Done")

    return final_result_dict, count, True

# anime_tosho_scraper("Fairy Tail", print_output=True)
# kick_ass_scraper(movie_title="peaky blinders", print_output=True)
# eztv_scraper(movie_title="100", print_output=True)
# nyaa_scraper(movie_title="Dr stone", print_output=True)




