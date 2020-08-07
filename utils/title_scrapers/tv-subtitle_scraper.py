from selenium import webdriver
from requests_html import HTML
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
import time

url = "https://tv-subtitle.com/tvshows"

print(f"Starting Browswre to get the site >>> {url}")
driver = webdriver.Firefox()
driver.get(url)

resutls_dictionary = {}

print(f"Finished loading page, Now Setting select option to ALl.")
elem = driver.find_element_by_css_selector("select.custom-select")
for option in elem.find_elements_by_tag_name('option'):
    if option.text == 'All':
        option.click()  # select() in earlier versions of webdriver
        break

print(f"Now getting each title and appending title data to a result dictionary...")
start_time = time.time()
html_source = driver.page_source
req_html = HTML(html=html_source)

for match in req_html.find("tr.even, tr.odd", first=False):
    show_title = match.find("td a", first=True).text
    show_link = "https://tv-subtitle.com" + match.find("a", first=True).attrs['href']
    show_index = match.find("td.align-middle", first=False)[0].text
    show_seasons_available = match.find("td.align-middle")[2].text
    show_episodes_available = match.find("td.align-middle")[3].text
    show_subtitles_available = match.find("td.align-middle")[4].text
    show_year = match.find("td.align-middle")[5].text

    # print((show_index, show_title, show_link, show_seasons_available, show_episodes_available, show_subtitles_available, show_year))

    resutls_dictionary[show_title] = {"show_index": show_index,
                                      "show_title": show_title,
                                      "show_link": show_link,
                                      "show_seasons_available": show_seasons_available,
                                      "show_episodes_available": show_episodes_available,
                                      "show_subtitles_available": show_subtitles_available,
                                      "show_year": show_year}


print(f"Finished getting all the titles. Finished in {time.time() - start_time} Secconds")
print("Now writting the dictionary to disk...")
with open("TV_SUBTITTLE_RFERENCE_DICTIONARY.json", "w") as refFo:
    json.dump(resutls_dictionary, refFo, indent=2)

print("\n\t\tDone making reference dictionary")

driver.close()







