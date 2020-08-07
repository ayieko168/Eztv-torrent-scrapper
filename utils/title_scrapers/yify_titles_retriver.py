from requests_html import HTMLSession, HTML
import json, time

last_page = 834
results_dictionary = {}
start_titme = time.time()

print(f"Starting script, Visiting site...")
session = HTMLSession()
r = session.get(f"https://yts.mx/browse-movies?page={last_page}")

print("Vissiting each page and on each page getting the titles from that page...")
page_count = last_page
for page in r.html:
    # visit every movie container inthe page
    for div_element in page.find("div.browse-movie-wrap", first=False):
        movie_link = div_element.find("a.browse-movie-link", first=True).attrs['href']
        movie_title = div_element.find("div.browse-movie-bottom a.browse-movie-title", first=True).text
        movie_year = div_element.find("div.browse-movie-bottom div.browse-movie-year", first=True).text

        results_dictionary[movie_title] = {"movie_title": movie_title,
                                           "movie_link": movie_link,
                                           "movie_year": movie_year}

    # print(json.dumps(results_dictionary, sort_keys=True, indent=True))

    page_count+=1
    if (page_count % 20) == 0:
        print(f"Just an update, we are currently at page {page_count}")

print("Done visiting the web pages."
      "Now writting the result dictionary to disk...")
with open("YIFI_TITLES_REFERENCE_DICTIONARY.json", "w") as refFo:
    json.dump(results_dictionary, refFo, sort_keys=True, indent=2)

print(f"****** Please UPDATE the <last_page> variable on this file to >> {page_count} ******")
print(f"\n\t\tDone with all operations in {time.time() - start_titme} Seconds\n\n")



