import urllib.request
from bs4 import BeautifulSoup
import json
from ast import literal_eval


def main():

    movie_result_dictionary = {}
    movie = "peaky blinders"
    url = "https://eztv.io/search/{}".format(movie)
    count = 0

    hdr = {"User-Agent": "Mozila/5.0"}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)

    soup = BeautifulSoup(page, "html.parser")

    # returns a list of all the <tr> tags under class forum_header_border
    tr_tags = soup.find_all("tr", {"class": "forum_header_border", "name": "hover"})

    for tr_elements in tr_tags:

        tb_tags = tr_elements.find_all("td")

        for tb_elements in tb_tags:

            print(tb_elements, "\n")

        title = tb_tags[1].find("a").get("title")
        try:
            torrent1 = tb_tags[2].find("a", {"class": "download_1"}).get("href") # torrent file
        except:
            pass
        try:
            torrent2 = tb_tags[2].find("a", {"class": "magnet"}).get("href") # torrent magnet
        except:
            pass
        size = tb_tags[3].text
        releaseDate = tb_tags[4].text
        seeds = tb_tags[5].text

        # print(torrent2)

        movie_result_dictionary[count] = [title, torrent1, torrent2, size, releaseDate, seeds]

        with open("result.json", "w") as resultFo:
            json.dump(movie_result_dictionary, resultFo, indent=2)
        
        count+=1




main()
