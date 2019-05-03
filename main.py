import urllib.request
from bs4 import BeautifulSoup
import json
from ast import literal_eval
import operator


def main(movieTitle):
    """create a json file containing the torrents result of 'movieTitle' """
    with open("ref_.json", "r")as f0:
        refDict = json.load(f0)

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
            torrent1 = tb_tags[2].find("a", {"class": "download_1"}).get("href")  # torrent file
        except:
            pass
        try:
            torrent2 = tb_tags[2].find("a", {"class": "magnet"}).get("href")  # torrent magnet
        except:
            pass
        size = tb_tags[3].text
        releaseDate = tb_tags[4].text
        seeds = tb_tags[5].text

        try:
            x = [se for se in title.split(" ") if se.startswith("S") and se.index("E") == 3][0]
            Se, Ep = x.replace("S", "").split("E")
        except:
            pass

        movie_result_dictionary[count] = [movieTitle.title(), title, torrent1, torrent2, size, releaseDate, seeds, Se, Ep]

        count += 1

        with open("result.json", "w") as resultFo:
            json.dump(movie_result_dictionary, resultFo, indent=2)

    print("Done\n")


def search_for(Se=4, Ep=3):
    """search for the season and episode in the results json"""
    dic = {}

    Se = "{:02}".format(Se)
    Ep = "{:02}".format(Ep)

    with open("result.json", "r") as jsonFo:
        resultDictionary = json.load(jsonFo)

    x = 0
    for k in resultDictionary.values():
        if (k[-2] == Se) and (k[-1] == Ep):
            # print("title:{}\nsize:{}\nseeders:{}\ntorrent_link:{}\n".format(k[1], k[4], k[6], k[3]))  # print the result, returns a list of values
            # print("\n")
            x += 1
            # sort by k[value]
            dic[k[6]] = [k[1], k[4], k[6], k[3]]

    # return a sorted list sorted by the index of the desired value ie 4=size"
    for k2, v in sorted(dic.items()):
        # print(v)
        print("title:{}\nsize:{}\nseeders:{}\ntorrent_link:{}\n".format(v[0], v[1], v[2], v[3]))
        print("\n")
    print(x, " torrents found")


# main(r"dynasty")
search_for(2, 13)
