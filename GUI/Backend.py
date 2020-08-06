import urllib.request
from bs4 import BeautifulSoup
import json
from ast import literal_eval
import sys, time, re, string, multiprocessing, datetime
import operator, webbrowser
from PyQt5.QtCore import QPoint, pyqtSlot, QThreadPool, QRunnable, QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QMessageBox, QTableWidgetItem, QApplication, QMenu
from PyQt5.QtGui import QTextCursor
# from PyQt5 import QtGui, QtCore
from utils.design_files.MainDesign import *
from utils.resources import torrent_scrapers
from collections import OrderedDict

## Plartform Spesific Variables
if (sys.platform == "win32") or (sys.platform == "cygwin"):
    resultPath = "utils\\resources\\result.json"
    EZTV_RFERENCE_DICTIONARYPath = "utils\\resources\\EZTV_RFERENCE_DICTIONARY.json"
    ref_Path = "utils\\resources\\ref_.json"
elif sys.platform == "linux":
    print("plartform is linux")
    resultPath = "./utils/resources/result.json"
    EZTV_RFERENCE_DICTIONARYPath = "./utils/resources/EZTV_RFERENCE_DICTIONARY.json"
    # ref_Path = "./utils/resources/ref_.json"
    ref_Path = "utils/resources/EZTV_RFERENCE_DICTIONARY.json"

class App(QMainWindow):

    def __init__(self):

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        ## Variables
        self.changed = False
        self.threadpool = QThreadPool()


        ## Connections
        self.ui.titleCombo.addItems(self.getTitles())
        # self.ui.getDataButton.clicked.connect(self.getDataCMD)
        self.ui.getDataButton.clicked.connect(self.get_data_cmd)
        self.ui.searchButton.clicked.connect(self.searchCMD)
        self.ui.moreInfoButton.clicked.connect(self.showMoreInfo)
        self.ui.searchForCombo.currentIndexChanged.connect(self.change_scrapers_in_combo)
        self.ui.scraperCombo.currentIndexChanged.connect(self.make_scaper_combo_changes)
        self.ui.showStatusCheck.clicked.connect(self.show_status_callback)
        self.ui.clearButton.clicked.connect(lambda: self.ui.loggingConsole.clear())
        self.ui.backButton.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))

        ## SETUP TABLES
        for table in [self.ui.showResutlTable, self.ui.moviesResutlTable, self.ui.animeResutlTable, self.ui.subtitleResutlTable]:
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            # header.setSectionResizeMode(3, QHeaderView.Stretch)
            table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            table.customContextMenuRequested.connect(self.on_customContextMenuRequested)

        ## get the current database title and set the "dataNameLable"
        self.get_current_db_title()

    def show_status_callback(self):

        if self.ui.showStatusCheck.isChecked():
            self.ui.stackedWidget_2.setCurrentIndex(1)
        else:
            self.ui.stackedWidget_2.setCurrentIndex(0)

    def make_scaper_combo_changes(self):

        self.changed = True

    def get_current_db_title(self):

        try:
            with open(resultPath) as titlesOb:
                currentTitle = json.load(titlesOb)["0"][0]
                self.ui.dataNameLabel.setText(currentTitle)
        except:
            self.ui.dataNameLabel.setText(None)

    def getTitles(self):
        """get the titles available from the 'titles' database"""

        with open(EZTV_RFERENCE_DICTIONARYPath) as titlesOb:
            data = json.load(titlesOb)
            titles = [k.replace("-", " ").title() for k,v in data.items()]
            titles.insert(0, "Select A Title...")
        
        return titles

    def change_scrapers_in_combo(self):

        if self.ui.searchForCombo.currentText().lower() == "TV-Show".lower():
            print("change to tv show scrapers")
            tv_scrapers = ['EZTV', 'Kickass', 'The Pirate Bay', 'All Sites']
            self.ui.scraperCombo.clear()
            self.ui.scraperCombo.addItems(tv_scrapers)
            self.ui.titleEdit.setPlaceholderText("Enter Tv-Show Title")

        elif self.ui.searchForCombo.currentText().lower() == "Movie".lower():
            print("change to movie scrapers")
            movie_scrapers = ['YIFI', 'Kickass', 'The Pirate Bay', 'All Sites']
            self.ui.scraperCombo.clear()
            self.ui.scraperCombo.addItems(movie_scrapers)
            self.ui.titleEdit.setPlaceholderText("Enter Movie Title")

            if not self.ui.displayAllCheck.isChecked():
                self.ui.displayAllCheck.click()

        elif self.ui.searchForCombo.currentText().lower() == "Anime".lower():
            print("change to anime scrapers")
            anime_scrapers = ['Nyaa', 'Anime Tosho', 'Kickass', 'All Sites']
            self.ui.scraperCombo.clear()
            self.ui.scraperCombo.addItems(anime_scrapers)
            self.ui.titleEdit.setPlaceholderText("Enter Anime Title")

            if not self.ui.displayAllCheck.isChecked():
                self.ui.displayAllCheck.click()

        elif self.ui.searchForCombo.currentText().lower() == "Subtitles".lower():
            print("change to subs sracpers")
            subs_scrapers = ['Open Subs', 'YIFI Subs', 'Tv Subs .com', 'Tv Subs .net', 'All Sites']
            self.ui.scraperCombo.clear()
            self.ui.scraperCombo.addItems(subs_scrapers)
            self.ui.titleEdit.setPlaceholderText("Enter Subtitle Title")

        elif self.ui.searchForCombo.currentText().lower() == "All Categories".lower():
            print("change to all torrent sracpers")
            subs_scrapers = ['Kickass', 'The Pirate Bay', 'Torrent Galaxy', 'RARBG get', '1337x', 'All Sites']
            self.ui.scraperCombo.clear()
            self.ui.scraperCombo.addItems(subs_scrapers)
            self.ui.titleEdit.setPlaceholderText("Enter Subtitle Title")

    def finished_collecting_torrents(self):

        ## Disable Buttons
        self.ui.getDataButton.setEnabled(True)
        self.ui.searchButton.setEnabled(True)

        ## Move back to results view
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.ui.showStatusCheck.setChecked(False)

    def data_logger(self, sender, message):

        _time = datetime.datetime.now().strftime("%H:%M:%S")
        log_text = f">>> [{_time}] [{sender.upper().strip()}] ==> {str(message).title().strip()}\n"

        if self.ui.autoScroll.isChecked():
            self.ui.loggingConsole.moveCursor(QTextCursor.End)
            self.ui.loggingConsole.insertPlainText(log_text)
        else:
            self.ui.loggingConsole.insertPlainText(log_text)

    def get_data_cmd(self):

        ## Disable Buttons
        self.ui.getDataButton.setEnabled(False)
        self.ui.searchButton.setEnabled(False)

        ## Move to the logging view
        self.ui.stackedWidget_2.setCurrentIndex(1)
        self.ui.showStatusCheck.setChecked(True)

        ## Set the auto scroll to true
        self.ui.autoScroll.setChecked(True)

        worker = Worker(self.getDataCMD)
        worker.signals.message_signal.connect(self.message)
        worker.signals.log_data.connect(self.data_logger)
        worker.signals.finished.connect(self.finished_collecting_torrents)
        self.threadpool.start(worker)

    def getDataCMD(self, signals):
        """command that downloads the <title> torrent info and writes it to a json file as a search reference"""

        return_code = False

        ## Get title references for local db
        with open('utils/resources/result.json', 'r') as resutlsFO:
            results_dictionary = json.load(resutlsFO)
        with open('utils/resources/EZTV_RFERENCE_DICTIONARY.json', 'r') as eztv_ref_FO:
            eztv_reference_dictionary = json.load(eztv_ref_FO)

        ## Ensure there is a query title
        if (self.ui.titleEdit.text() == '') and (self.ui.enterCheck.isChecked()):
            self.message("Please Enter a Search title. Try Game Of Thrones :)", "INFO")
            return
        if (self.ui.titleCombo.currentText() == 'Select A Title...') and (self.ui.chooseCheck.isChecked()):
            self.message("Please Enter a Search title. Try Game Of Thrones :)", "INFO")
            return

        ## Get the current search title (the previously searched title)
        if self.ui.enterCheck.isChecked(): title = self.ui.titleEdit.text()
        elif self.ui.chooseCheck.isChecked(): title = self.ui.titleCombo.currentText()

        title = title.strip()

        ## check if the title you want to search is the one in the current local db
        if results_dictionary != {}:
            if (title == results_dictionary["0"][0]) and (not self.changed):
                x = signals.message_signal.emit("This title is already scraped, Do you want to scrape again?")
                print("value of x = ", x)
                return
                # rc = self.message("This title is already scraped, Do you want to scrape again?", message_type='ASK')
                # if rc == QMessageBox.Yes:
                #     pass
                # elif rc == QMessageBox.No:
                #     return

        ## Check for the selected scraper
        requested_scraper = self.ui.scraperCombo.currentText().lower()

        ## Use requested scraper to get the torrents
        if requested_scraper == 'eztv':
            title = title.strip().lower().replace(' ', '-')

            # check if the title is in the eztv reference, if it is there us its eztv id to do the search
            if title in eztv_reference_dictionary.keys():
                print("using id")
                title_eztv_id = int(eztv_reference_dictionary[title][1])
                torrents_dictionary, torrents_count, return_code = torrent_scrapers.eztv_scraper(ez_id=title_eztv_id, signals=signals)

            else:
                print("using title")
                torrents_dictionary, torrents_count, return_code = torrent_scrapers.eztv_scraper(movie_title=title, signals=signals)

        elif requested_scraper == 'kickass' and self.ui.searchForCombo.currentText().lower() == "tv-show":

            print("use kickass tv show")
            torrents_dictionary, torrents_count, return_code = torrent_scrapers.kick_ass_scraper_tv(movie_title=title, signals=signals)

        elif requested_scraper == 'kickass' and self.ui.searchForCombo.currentText().lower() == "anime":

            print("use kickass anime")
            torrents_dictionary, torrents_count, return_code = torrent_scrapers.kick_ass_scraper_anime(movie_title=title, signals=signals)

        elif requested_scraper == "nyaa":
            print("use nyaa anime")
            torrents_dictionary, torrents_count, return_code = torrent_scrapers.nyaa_scraper(movie_title=title, signals=signals)

        elif requested_scraper.lower() == 'Anime Tosho'.lower():
            print("use Anime Tosho")
            torrents_dictionary, torrents_count, return_code = torrent_scrapers.anime_tosho_scraper(movie_title=title, signals=signals)

        elif requested_scraper.lower() == "YIFI".lower():

            print("use YIFY Movies")
            torrents_dictionary, torrents_count, return_code = torrent_scrapers.yify_movie_scraper(movie_title=title, signals=signals)

        elif requested_scraper.lower() == "All Sites".lower():
            print("Gathering torrents from all the sites")

            # Get the search category
            if self.ui.searchForCombo.currentText().lower() == "TV-Show":
                # Search for the torrent using tv_series torren sites
                pass

        else:

            signals.message_signal.emit("It seams the scraper you selected is not yet functional, please select another")
            # self.message("It seams the scraper you selected is not yet functional, please select another")
            return

        ## Process the returned torrent data
        # If the scrape was successful
        if return_code == True:

            ## Write the info to the reference dictionary
            with open('utils/resources/result.json', 'w') as result_fo:
                json.dump(torrents_dictionary, result_fo, indent=2)

            ## Give successfull message box
            # self.message(f"The scrape was successful. Found {torrents_count} torrent. Thank ayieko168 latter! ")
            signals.message_signal.emit(f"The scrape was successful. Found {torrents_count} torrent. Thank ayieko168 latter! ")

            ## Rename the 'current database' label
            try:
                self.ui.dataNameLabel.setText(torrents_dictionary[0][0].title())
            except KeyError:
                self.ui.dataNameLabel.setText("None")
                with open('utils/resources/result.json', 'w') as result_fo:
                    json.dump({"0": ["None", "", "", "", "", "", "", ""]}, result_fo, indent=2)

            ## Fill the table with all the data
            # Clear all table rows and display results
            if self.ui.searchForCombo.currentText().lower() == "TV-Show".lower(): table = self.ui.showResutlTable
            elif self.ui.searchForCombo.currentText().lower() == "Movie".lower(): table = self.ui.moviesResutlTable
            elif self.ui.searchForCombo.currentText().lower() == "Anime".lower(): table = self.ui.animeResutlTable
            elif self.ui.searchForCombo.currentText().lower() == "Subtitles".lower(): table = self.ui.subtitleResutlTable
            else: table = self.ui.showResutlTable

            table.setRowCount(0)
            for found_torrent_list in self.search_for(all=True, sort_value=self.ui.sortValueCombo.currentText()):
                self.displayResultOnTable(found_torrent_list, on_table=table)

        # If the process was NOT suucessful
        if return_code == False:

            ## Give runtime error message box
            # self.message("There was a problem during the scrape")
            signals.message_signal.emit("There was a problem during the scrape")
        
        ## Change the scraper combo variable
        self.changed = False

        ## Emit the finished signal
        signals.finished.emit()

    def displayResultOnTable(self, torrent_dictionary, on_table):

        table = on_table

        rowPosition = table.rowCount()
        table.insertRow(rowPosition)

        ## Set column data
        table.setItem(rowPosition, 0, QTableWidgetItem(str(torrent_dictionary[1])))  # Title
        table.setItem(rowPosition, 1, QTableWidgetItem(str(torrent_dictionary[4])))  # Size
        table.setItem(rowPosition, 2, QTableWidgetItem(str(torrent_dictionary[5])))  # Seeds
        table.setItem(rowPosition, 3, QTableWidgetItem(str(torrent_dictionary[3])))  # Magnet link

        ## Set text alignment
        table.item(rowPosition, 1).setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        table.item(rowPosition, 2).setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def searchCMD(self):
        """Call back function for the 'search' button, for quering the local db"""

        ## Get the table where to display the info
        if self.ui.searchForCombo.currentText().lower() == "TV-Show".lower(): table = self.ui.showResutlTable
        elif self.ui.searchForCombo.currentText().lower() == "Movie".lower(): table = self.ui.moviesResutlTable
        elif self.ui.searchForCombo.currentText().lower() == "Anime".lower(): table = self.ui.animeResutlTable
        elif self.ui.searchForCombo.currentText().lower() == "Subtitles".lower(): table = self.ui.subtitleResutlTable
        else: table = self.ui.showResutlTable

        ## Populate the table with queried data
        sort_key = self.ui.sortValueCombo.currentText()

        # Season, Episode and Search Term
        if (self.ui.seasonCheck.isChecked() and self.ui.seasonCheck.isEnabled()) and (self.ui.episodeCheck.isChecked() and self.ui.episodeCheck.isEnabled()) and (self.ui.searchTermCheck.isChecked() and self.ui.searchTermCheck.isEnabled()):

            print("Season, Episode and Search Term")
            season_query = self.ui.seasonSpin.text()
            episode_query = self.ui.episodeSpin.text()
            term_query = self.ui.searchTermEntry.text()

            query_dict = self.search_for(query_season=season_query, query_episode=episode_query, sort_value=sort_key, query_term=term_query)

            # Clear all table rows and display results
            table.setRowCount(0)
            for found_torrent_list in query_dict:
                self.displayResultOnTable(found_torrent_list, on_table=table)

        # Season and episode
        elif (self.ui.seasonCheck.isChecked() and self.ui.seasonCheck.isEnabled()) and (self.ui.episodeCheck.isChecked() and self.ui.episodeCheck.isEnabled()):
            print("Season and episode")
            season_query = self.ui.seasonSpin.text()
            episode_query = self.ui.episodeSpin.text()

            query_dict = self.search_for(query_season=season_query, query_episode=episode_query, sort_value=sort_key)

            # Clear all table rows and display results
            table.setRowCount(0)
            for found_torrent_list in query_dict:
                self.displayResultOnTable(found_torrent_list, on_table=table)

        # Season And Serch Term
        elif (self.ui.searchTermCheck.isChecked() and self.ui.searchTermCheck.isEnabled()) and (self.ui.seasonCheck.isChecked() and self.ui.seasonCheck.isEnabled()):
            print("Season And Serch Term")
            term_query = self.ui.searchTermEntry.text()
            season_query = self.ui.seasonSpin.text()

            query_dict = self.search_for(query_season=season_query, query_term=term_query, sort_value=sort_key)

            # Clear all table rows and display results
            table.setRowCount(0)
            for found_torrent_list in query_dict:
                self.displayResultOnTable(found_torrent_list, on_table=table)

        # Season
        elif self.ui.seasonCheck.isChecked() and self.ui.seasonCheck.isEnabled():

            print("Season")
            season_query = self.ui.seasonSpin.text()

            query_dict = self.search_for(query_season=season_query, sort_value=sort_key)

            # Clear all table rows and display results
            table.setRowCount(0)
            for found_torrent_list in query_dict:
                self.displayResultOnTable(found_torrent_list, on_table=table)

        # Search Term, All
        elif (self.ui.searchTermCheck.isChecked() and self.ui.searchTermCheck.isEnabled()) and (self.ui.displayAllCheck.isChecked() and self.ui.displayAllCheck.isEnabled()):

            print("Search term and all")
            term_query = self.ui.searchTermEntry.text()

            query_dict = self.search_for(query_term=term_query, sort_value=sort_key)

            # Clear all table rows and display results
            table.setRowCount(0)
            for found_torrent_list in query_dict:
                self.displayResultOnTable(found_torrent_list, on_table=table)

        # Search Term Only
        elif self.ui.searchTermCheck.isChecked() and self.ui.searchTermCheck.isEnabled():

            print("Search Term Only")
            term_query = self.ui.searchTermEntry.text()

            query_dict = self.search_for(query_term=term_query, sort_value=sort_key)

            # Clear all table rows and display results
            table.setRowCount(0)
            for found_torrent_list in query_dict:
                self.displayResultOnTable(found_torrent_list, on_table=table)


        # All
        elif self.ui.displayAllCheck.isChecked() and self.ui.displayAllCheck.isEnabled() and not self.ui.searchTermCheck.isChecked():
            print("All")
            query_dict = self.search_for(all=True, sort_value=sort_key)

            # Clear all table rows and display results
            table.setRowCount(0)
            for found_torrent_list in query_dict:
                self.displayResultOnTable(found_torrent_list, on_table=table)

        else:
            print("else, all")
            query_dict = self.search_for(all=True, sort_value=sort_key)

            # Clear all table rows and display results
            table.setRowCount(0)
            for found_torrent_list in query_dict:
                self.displayResultOnTable(found_torrent_list, on_table=table)

        w.processEvents()

    @pyqtSlot(QPoint)
    def on_customContextMenuRequested(self, pos):

        w.processEvents()
        table = QApplication.focusWidget()
        tableName = table.objectName()

        if table.rowCount() <= 0:
            return

        def getItemData(itemIndex):
            data = []

            for i in range(table.columnCount()):
                try:
                    data.append(table.item(itemIndex, i).text())
                except:
                    pass

            return data
        
        top_menu = QMenu(self)
        menu = top_menu.addMenu("Menu")

        copy = menu.addAction("Copy")
        menu.addSeparator()
        if self.ui.searchForCombo.currentText() == "TV-Show":
            _open = menu.addAction("Open in Bittorren Client")
            menu.addSeparator()
        elif self.ui.searchForCombo.currentText() == "Movie":
            _open = menu.addAction("Open in Bittorren Client")
            menu.addSeparator()
        elif self.ui.searchForCombo.currentText() == "Anime":
            _open = menu.addAction("Open in Bittorren Client")
            menu.addSeparator()
        elif self.ui.searchForCombo.currentText() == "Subtitles":
            _open = menu.addAction("Open in Bittorren Client")
            menu.addSeparator()
        elif self.ui.searchForCombo.currentText() == "All Categories":
            _open = menu.addAction("Open in Bittorren Client")
            menu.addSeparator()
        
        action = menu.exec_(QtGui.QCursor.pos())

        if action == copy:
            item_row = table.currentIndex().row()
            itemName = table.item(item_row, 0).text()
            itemData = getItemData(item_row)

            magnet_link = itemData[3]

            # copy selected path to clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(magnet_link)
        
        elif action == _open:

            item_row = table.currentIndex().row()
            itemName = table.item(item_row, 0).text()
            itemData = getItemData(item_row)

            magnet_link = itemData[3]

            webbrowser.open_new_tab(magnet_link)

            ## Move Spin-Box episode by one value up and higlight
            self.ui.episodeSpin.setValue(self.ui.episodeSpin.value()+1)
            self.ui.episodeSpin.selectAll()

    def showMoreInfo(self):

        print("show more info")

        ## Get the current title
        with open(resultPath, "r") as resultsFo:
            resultsDict = json.load(resultsFo)
            current_title = resultsDict["0"][0].lower().replace(" ", "-")

        try:

            with open(ref_Path, "r") as refFo:
               referenceDict = json.load(refFo)
               lis = referenceDict[current_title]
               title = current_title
               title_ID = lis[1]

            url = f"https://eztv.io/shows/{title_ID}/{title}/"
            image_url = f"https://eztv.io/ezimg/thumbs/{title}-{title_ID}.jpg"
            print(title_ID, title)
            webbrowser.open_new(url)
        except KeyError:
            print("Cant find the title on the local reference, opening google and imdb...")

            google_url = f"https://google.com/search?&q={current_title}"
            imdb_url = f"https://www.imdb.com/search/title/?title={current_title}"

            webbrowser.open_new(google_url)
            webbrowser.open_new(imdb_url)

    def downloadAdditionalInfo(self, url):

        info_dictionary = {}

        try:
            hdr = {"User-Agent": "Mozila/5.0"}
            req = urllib.request.Request(url, headers=hdr)
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, "html.parser")
        except Exception as e:
            # print(e.args)
            # print("CHECK YOUR INTERNET CONNECTION")
            return 402
        
        td_element = soup.find("td", {"class": "show_info_banner_logo"})
        description = td_element.find("span").text

        table_element = soup.findChildren("table", {"class": "section_thread_post show_info_description"})
        # x = table_element.text
        
        with open ("the_data.md", "w")as fff:
            fff.write(str(table_element))

    def search_for(self, query_season=None, query_episode=None, query_term=None, sort_value='name', all=False):

        filtered_dict = {}
        sorted_dict = OrderedDict()
        sort_value = sort_value.lower()

        with open("./utils/resources/result.json", "r") as jsonFo:
            search_dictionary = json.load(jsonFo)

        if not all:
            ## (Apply the filter) Loop through each item in the result dictonary - each item is a list containig individual torrent data
            count = 0
            for _, values in search_dictionary.items():
                # print(values)

                ## Get the individual item data values
                title, torrent_name, torrent_link, magnet_link, size, seeds, season, episode = values

                # season only filter
                if query_term is None and query_season is not None and query_episode is None:
                    query_season = "{:02}".format(int(query_season))
                    if query_season == season:
                        # print(values[1])
                        filtered_dict[count] = values
                        count += 1

                # season and episode filter
                elif query_term is None and query_season is not None and query_episode is not None:
                    query_season = "{:02}".format(int(query_season))
                    query_episode = "{:02}".format(int(query_episode))
                    if query_season == season and query_episode == episode:
                        # print(values[1])
                        filtered_dict[count] = values
                        count += 1

                # query term filter only
                elif query_term is not None and query_term != '' and query_season is None and query_episode is None:
                    if query_term.lower() in torrent_name.lower():
                        filtered_dict[count] = values
                        count += 1

                # query term and season filter only
                elif query_term is not None and query_term != '' and query_season is not None and query_episode is None:
                    query_season = "{:02}".format(int(query_season))

                    if query_term.lower() in torrent_name.lower() and query_season == season:
                        filtered_dict[count] = values
                        count += 1

                # query term season and episode filter
                elif query_term is not None and query_term != '' and query_season is not None and query_episode is not None:
                    query_season = "{:02}".format(int(query_season))
                    query_episode = "{:02}".format(int(query_episode))

                    if query_term.lower() in torrent_name.lower() and query_season == season and query_episode == episode:
                        filtered_dict[count] = values
                        count += 1

            ## (Sort the filterde content) Loop through the filtered dictionaty and use the filter value as key so as to sort with key
            for _, values in filtered_dict.items():
                ## Get the individual item data values
                title, torrent_name, torrent_link, magnet_link, size, seeds, season, episode = values

                if sort_value.lower() == 'Name'.lower():
                    sorted_dict[str(values)] = torrent_name

                elif sort_value.lower() == 'Seeders'.lower():

                    try:
                        moded_seeds = int(seeds)
                    except:
                        moded_seeds = 0

                    sorted_dict[str(values)] = moded_seeds

                elif sort_value.lower() == 'Size'.lower():

                    if "k".upper() in size.upper():
                        moded_size = float(size.strip(string.ascii_letters)) * 1e-3
                    elif "m".upper() in size.upper():
                        moded_size = float(size.strip(string.ascii_letters))
                    elif "g".upper() in size.upper():
                        moded_size = float(size.strip(string.ascii_letters)) * 1e3
                    else:
                        moded_size = float(size.strip(string.ascii_letters)) * 1e6

                    sorted_dict[str(values)] = moded_size

            ## Create the dictionary to hold the sorted filtered values
            sorted_x = sorted(sorted_dict.items(), key=lambda kv: kv[1])
            sorted_dict = OrderedDict(sorted_x)  # key=a string list containig values, value=sort value

            ## The final list of torrent lists
            final_list = [literal_eval(i) for i in sorted_dict.keys()]

        if all:
            ## (Sort the filterde content) Loop through the filtered dictionaty and use the filter value as key so as to sort with key
            for _, values in search_dictionary.items():
                ## Get the individual item data values
                title, torrent_name, torrent_link, magnet_link, size, seeds, season, episode = values

                if sort_value.lower() == 'Name'.lower():
                    sorted_dict[str(values)] = torrent_name

                elif sort_value.lower() == 'Seeders'.lower():

                    try:
                        moded_seeds = int(seeds)
                    except:
                        moded_seeds = 0

                    sorted_dict[str(values)] = moded_seeds

                elif sort_value.lower() == 'Size'.lower():

                    if "k".upper() in size.upper():
                        moded_size = float(size.strip(string.ascii_letters)) * 1e-3
                    elif "m".upper() in size.upper():
                        moded_size = float(size.strip(string.ascii_letters))
                    elif "g".upper() in size.upper():
                        moded_size = float(size.strip(string.ascii_letters)) * 1e3
                    else:
                        moded_size = float(size.strip(string.ascii_letters)) * 1e6

                    sorted_dict[str(values)] = moded_size

            ## Create the dictionary to hold the sorted filtered values
            sorted_x = sorted(sorted_dict.items(), key=lambda kv: kv[1])
            sorted_dict = OrderedDict(sorted_x)  # key=a string list containig values, value=sort value

            ## The final list of torrent lists
            final_list = [literal_eval(i) for i in sorted_dict.keys()]

        return final_list

    def message(self, message_text, message_type="INFO"):
        message_text = message_text.title()

        matches = list(re.compile(r'\[[A-Za-z]+\]').finditer(message_text))

        for match in matches:
            match = match.group()
            message_text = message_text.replace(match, match.upper())

        if message_type.upper() == "INFO":
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(message_text)
            msgBox.setWindowTitle("INFORMATION".upper())
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            return returnValue

        elif message_type.upper() == 'ASK':
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(message_text)
            msgBox.setWindowTitle("QUESTIon".upper())
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            returnValue = msgBox.exec()
            return returnValue


class Worker(QRunnable):

    def __init__(self, func, *args, **kwargs):

        super(Worker, self).__init__()

        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):

        print("geting data...")
        self.func(self.signals)
        print("done.")



class WorkerSignals(QObject):

    finished = pyqtSignal()
    log_data = pyqtSignal(object, object)
    message_signal = pyqtSignal(object)



if __name__ == "__main__":

    w = QApplication([])
    app = App()
    app.show()
    w.exec_()



















