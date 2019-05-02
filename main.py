import urllib.request
from bs4 import BeautifulSoup
import json
from ast import literal_eval


def main():

    movie = "billions"

    url = "https://eztv.io/search/{}".format(movie)

    hdr = {"User-Agent": "Mozila/5.0"}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)

    soup = BeautifulSoup(page, "html.parser")

    # returns a list of all the <tr> tags under class forum_header_border
    tr_tags = soup.find_all("tr", {"class": "forum_header_border", "name": "hover"})

    for tr_elements in tr_tags:

        tb_tags = tr_elements.find_all("td", {"class": "forum_thread_post"})

        for tb_elements in tb_tags:

            print(tb_elements, "\n")

        title = tb_tags[1].find("a").get("title")
        title = tb_tags[1].find("a").get("title")

        # print(t)

        break


main()
