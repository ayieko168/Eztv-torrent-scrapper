from bs4 import BeautifulSoup
import urllib.request
import json

url = "https://eztv.io/showlist/"

try:
    print("downloadong web page info...")
    hdr = {"User-Agent": "Mozila/5.0"}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
except Exception as e:
    print(e.args)
    # print("CHECK YOUR INTERNET CONNECTION")
    # return 402

tr_tags = soup.find_all("tr", {"name": "hover"})

Titles_Dictionary = {}

count = 1
for tr_tag in tr_tags:
    print(f"Processing item {count} out of {len(tr_tags)}")

    a_tag = tr_tag.find("a")

    show_link = a_tag.get("href") #/shows/449/10-oclock-live/
    show_title = a_tag.text #10 O'Clock Live
    show_ID = show_link.split("/")[2]
    show_name = show_link.split("/")[3]

    Titles_Dictionary[show_name] = [show_title, show_ID, show_link]
    count+=1


with open("EZTV_RFERENCE_DICTIONARY.json", "w") as refFO:
    json.dump(Titles_Dictionary, refFO, indent=2)

