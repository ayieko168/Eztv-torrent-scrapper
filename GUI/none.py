from requests_html import HTMLSession
import urllib.parse

url = "http://192.168.0.17:8000/Arduino%20Projects%20Research/Arduino%20Oscciloscope/"

print(f"Starting script, Visiting site...")
session = HTMLSession()
r = session.get(url)

for page in r.html:
    for li_element in page.find("ul li"):
        print(li_element.absolute_links)





