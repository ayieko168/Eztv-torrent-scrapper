from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import json, math, os

ost = OpenSubtitles()
token = ost.login(int(64084487842968137541007709925799131749).to_bytes(math.ceil(int(64084487842968137541007709925799131749).bit_length() / 8), 'little').decode(), int(546355688029801288302918137390656857).to_bytes(math.ceil(int(546355688029801288302918137390656857).bit_length() / 8), 'little').decode())


def get_str_info(file_path):
    result_dict = {}
    print(token)

    f = File(file_path)

    data = ost.search_subtitles([{'sublanguageid': 'all', 'moviehash': f.get_hash(), 'moviebytesize': f.size}])

    print(data)
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

    print(json.dumps({'data': result_dict}, indent=2))
    return result_dict
    # print(json.dumps({'data': data}, indent=2))
    # id_subtitle_file = data[0].get('IDSubtitleFile')
    # print(id_subtitle_file)

get_str_info(r"C:\Users\royalstate\Movies\Series\The Spy\The.Spy.S01E02.WEBRip.X264-PHENOMENAL[eztv].mkv")

