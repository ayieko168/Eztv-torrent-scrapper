import json
from collections import OrderedDict
import time


def search_for(season=1, episode=1, sortValue='size', all=False):
    """ search for the season and episode in the results json file
         :returns: A List of touples with format (sort_value, torent_dictionary)
        sortValue ==> name=Name, size=Size, seeders=Seeders"""

    search_dictionary = OrderedDict()
    match_dictionary = OrderedDict()

    search_season = "{:02}".format(season)
    search_episode = "{:02}".format(episode)

    with open("./utils/resources/result.json", "r") as jsonFo:
        search_dictionary = json.load(jsonFo)

    counter = 1
    for _, ref_value in search_dictionary.items():

        ref_season = ref_value[6]
        ref_episode = ref_value[7]
        ref_name = ref_value[1]
        ref_size = ref_value[4]
        ref_seeds = ref_value[5]
        ref_magnet_link = ref_value[3]
        ref_torrent_link = ref_value[2]

        if "MB" in ref_size:
            mod_ref_size = float(ref_size.replace(" ", "").replace("MB", "").strip())
        elif "GB" in ref_size:
            mod_ref_size = float(ref_size.replace(" ", "").replace("GB", "").strip())
            mod_ref_size = mod_ref_size * 1e3
        else:
            mod_ref_size = float(ref_size)

        # Search to find if the searched <season> and <episode> are in an item's value
        if (ref_season == search_season) and (ref_episode == search_episode) and not all:
            # print("returning searched")
            "name=Name, size=Size, seeders=Seeders"
            if sortValue == "size":
                match_dictionary[mod_ref_size + time.time()] = {"title": ref_name, "torrent_link": ref_torrent_link,
                                                                "magnet_link": ref_magnet_link,
                                                                "size": ref_size, "seeds": ref_seeds,
                                                                "season": ref_season, "episode": ref_episode}
            elif sortValue == "name":
                match_dictionary[ref_name] = {"title": ref_name, "torrent_link": ref_torrent_link,
                                              "magnet_link": ref_magnet_link,
                                              "size": ref_size, "seeds": ref_seeds, "season": ref_season,
                                              "episode": ref_episode}
            elif sortValue == "seeders":
                match_dictionary[float(ref_seeds) + float(time.time())] = {"title": ref_name,
                                                                    "torrent_link": ref_torrent_link,
                                                                    "magnet_link": ref_magnet_link,
                                                                    "size": ref_size, "seeds": ref_seeds,
                                                                    "season": ref_season, "episode": ref_episode}
            else:
                match_dictionary[mod_ref_size + time.time()] = {"title": ref_name, "torrent_link": ref_torrent_link,
                                                                "magnet_link": ref_magnet_link,
                                                                "size": ref_size, "seeds": ref_seeds,
                                                                "season": ref_season, "episode": ref_episode}

        if all:
            # print("returning all")
            if sortValue == "size":
                match_dictionary[mod_ref_size + time.time()] = {"title": ref_name, "torrent_link": ref_torrent_link,
                                                                "magnet_link": ref_magnet_link,
                                                                "size": ref_size, "seeds": ref_seeds,
                                                                "season": ref_season, "episode": ref_episode}
            elif sortValue == "name":
                match_dictionary[ref_name] = {"title": ref_name, "torrent_link": ref_torrent_link,
                                              "magnet_link": ref_magnet_link,
                                              "size": ref_size, "seeds": ref_seeds, "season": ref_season,
                                              "episode": ref_episode}
            elif sortValue == "seeders":
                match_dictionary[float(ref_seeds) + float(time.time())] = {"title": ref_name,
                                                                           "torrent_link": ref_torrent_link,
                                                                           "magnet_link": ref_magnet_link,
                                                                           "size": ref_size, "seeds": ref_seeds,
                                                                           "season": ref_season, "episode": ref_episode}
            else:
                match_dictionary[mod_ref_size + time.time()] = {"title": ref_name, "torrent_link": ref_torrent_link,
                                                                "magnet_link": ref_magnet_link,
                                                                "size": ref_size, "seeds": ref_seeds,
                                                                "season": ref_season, "episode": ref_episode}


    # print(json.dumps(match_dictionary, sort_keys=True, indent=2))

    return sorted(match_dictionary.items())

l = search_for(all=True, sortValue="seed")

for item in l:
    print(item)





