import urllib.request
from bs4 import BeautifulSoup
import json
from ast import literal_eval
import operator


def main(movieTitle):
    """create a json file containing the torrents result of 'movieTitle' """

    movie_result_dictionary = {}
    movie = str(movieTitle)
    url = "https://eztv.io/search/{}".format(movie)
    count = 0

    hdr = {"User-Agent": "Mozila/5.0"}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")

    # returns a list of all the <tr> tags under class forum_header_border
    tr_tags = soup.find_all("tr", {"class": "forum_header_border", "name": "hover"})

    for tr_elements in tr_tags:

        print(count)

        tb_tags = tr_elements.find_all("td")

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

        try:
            len_title = len(movieTitle.split(" "))
            x = title.split(" ")[len_title:]
            Se, Ep = x[0].replace("S", "").split("E")
        except ValueError:
            pass

        # print(torrent2)
        movie_result_dictionary[count] = [movieTitle.title(), title, torrent1, torrent2, size, releaseDate, seeds, Se, Ep]

        count+=1

        with open("result.json", "w") as resultFo:
            json.dump(movie_result_dictionary, resultFo, indent=2)

    print("Done\n")


def sortBy(what):
    """sort 'object' by 'what'"""

    with open("result.json", "r") as fo:
        resultDictionary = json.load(fo)

        dic = resultDictionary
        sorted_x = sorted(dic.items(), key=operator.itemgetter(1))

        print(sorted_x)




# main("game of thrones")
sortBy("size")
