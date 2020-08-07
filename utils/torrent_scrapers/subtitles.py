from requests_html import HTMLSession, HTML

url = "https://tv-subtitle.com/tvshows"

session = HTMLSession()
r = session.get(url)
# r.html.render(timeout=20)

matches = r.html.find("tr", first=False)

for match in matches:
    print(match)

