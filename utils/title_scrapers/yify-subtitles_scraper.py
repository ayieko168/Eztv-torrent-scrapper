from requests_html import HTMLSession, HTML
import json, time

last_page = 834
results_dictionart = {}
start_titme = time.time()

print(f"Starting script, Visiting site...")
session = HTMLSession()
r = session.get("https://yts-subs.com/browse?page=834")

print("Vissiting each page and on each page getting the titles from that page...")
page_count = last_page
for page in r.html:
    result_links = page.find("li.media-movie-clickable div.media-body a", first=False)
    for a_element in result_links:  # list of a elements
        movie_subtitle_link = "https://yts-subs.com" + a_element.attrs['href']
        movie_subtitle_title = a_element.find(".media-heading", first=True).text
        movie_subtitle_year = a_element.find("span.movinfo-section", first=True).text.replace("year", "").strip()

        results_dictionart[movie_subtitle_title] = {"movie_title": movie_subtitle_title,
                                                    "subtitle_movie_link": movie_subtitle_link,
                                                    "subtitle_year": movie_subtitle_year}

    page_count+=1
    if (page_count % 20) == 0:
        print(f"Just an update, we are currently at page {page_count}")

print("Done visiring the web pages."
      "Now writting the result dictionary to disk...")
with open("YIFI_SUBTITLES_REFERENCE_DICTIONARY.json", "w") as refFo:
    json.dump(results_dictionart, refFo, sort_keys=True, indent=2)

print(f"****** Please UPDATE the <last_page> variable on this file to >> {page_count} ******")
print(f"\n\t\tDone with all operations in {time.time() - start_titme} Seconds\n\n")



