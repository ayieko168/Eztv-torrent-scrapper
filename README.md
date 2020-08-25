# Eztv-torrent-scrapper
scrapes the eztv website for torrent links

This Software is an attempt at making a torrent scraper for TV-Shows from [EZTV](https://eztv.io/).
It searches for requested Show seasons and episodes and responds by listing a list of available magnet links
that can be used to download the requested show episode.

NOTE: Currently works but only on Windows.

# INSTALLATION
#### Requirements
You can get the requirements from [here](/Dependancies/List.txt) but here is a list of the packages
1. urllib
2. BeautifulSoup
3. ast
4. operator
5. PyQt5
6. requests-html

#### Running the software
If you are on windows, you can simply download and extract the [Bundled Rar file](https://github.com/ayieko168/Eztv-torrent-scrapper/raw/master/BUNDLED/BUNDLED.rar) and 
look for the executable file within the extracted file.

If you are on linux, you can help me finish up making the software plartform-indipendent and send pull requests.
For now you will have to wait till I finish it ;)

You can download the [latest release](https://github.com/ayieko168/Eztv-torrent-scrapper/releases/latest) and extract the archive file. you can then follow the instructions on that page to run the program.

# SCREENSHOTS
 Bellow shows a screenshot of the application.
 ![GitHub Logo](/Screenshots/Frontend-Inactive.png)

 An Image showing the program shearch results:
 ![Active Image](/Screenshots/Search-Example.JPG)

# FUTURE ADVANCES
In the future I want to:
- [x] Make the program plartform-indipendent (Work on any plartform, ie:Windows, Linux, OS-X)
- [x] The program should be able to scrape Movies instead of Tv-Shows only
- [ ] The user should be able to chose the websites the crawler visits to scrape for the torrents. From websites such as:
    - [ ] 1337x
    - [ ] Demonoid
    - [ ] ExtraTorrent
    - [x] EZTV
    - [ ] isoHunt
    - [x] KickassTorrents
    - [x] Nyaa Torrents
    - [ ] RARBG
    - [ ] Tamil Rockers 
    - [x] The Pirate Bay 
    - [x] YIFY
    - [x] Open Subtiles
    
 - [x] Ability to scrape for and download subtitles
 - [ ] Ability to get the titles from a rest API (set-up using django-rest-api)
