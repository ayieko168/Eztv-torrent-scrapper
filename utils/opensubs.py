import struct
import os


def hashFile(name):
    try:

        longlongformat = '<q'  # little-endian long long
        bytesize = struct.calcsize(longlongformat)

        f = open(name, "rb")

        filesize = os.path.getsize(name)
        hash = filesize

        if filesize < 65536 * 2:
            return "SizeError"

        for x in range(int(65536/bytesize)):
            buffer = f.read(bytesize)
            (l_value,) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

        f.seek(max(0, filesize-65536), 0)
        for x in range(int(65536/bytesize)):
            buffer = f.read(bytesize)
            (l_value,) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash = "%016x" % hash
        return returnedhash

    except (IOError):
        return "IOError"



def get_opensubtitle_url(file):

    _hash = hashFile(file)

    url = f"https://www.opensubtitles.org/en/search/sublanguageid-eng/moviehash-{_hash}/dragsearch-on"

    print(url)


ret = get_opensubtitle_url("D:\Movies\TONY\The Sopranos - The Complete Series (Season 1, 2, 3, 4, 5 & 6) + Extras\Season 2\The Sopranos Season 2 Episode 03 - Toodle-fucking-oo.avi")