import urllib.request
from bs4 import BeautifulSoup
import json
from ast import literal_eval
import sys, time
import operator, webbrowser
from PyQt5.QtCore import QPoint, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QMessageBox, QTableWidgetItem, QApplication, QMenu
from PyQt5 import QtGui, QtCore
from utils.design_files.MainDesign import *
from utils.torrent_scrapers import eztv_scraper
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

        self.ui.titleCombo.addItems(self.getTitles())
        self.ui.getDataButton.clicked.connect(self.getDataCMD)
        self.ui.searchButton.clicked.connect(self.searchCMD)
        self.ui.moreInfoButton.clicked.connect(self.showMoreInfo)
        
        ## SETUP TABLE
        header = self.ui.resutlTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.ui.resutlTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.resutlTable.customContextMenuRequested.connect(self.on_customContextMenuRequested)

        ## get the current database title and set the "dataNameLable"
        self.get_current_db_title()

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

    def getDataCMD(self):
        """command that downloads the <title> torrnt info and writed it to a json file as a search reference"""

        with open(ref_Path, "r") as refernce_Fo:
            reference_dict = json.load(refernce_Fo)

        title = ""

        ## Check if there is any selected input method and input text
        if (self.ui.enterCheck.isChecked()) and (self.ui.titleEdit.text() != ""):
            title = self.ui.titleEdit.text()
        elif (self.ui.chooseCheck.isChecked()) and (self.ui.titleCombo.currentText() != "Select A Title..."):
            title = self.ui.titleCombo.currentText()
        else:
            self.ui.statusBar.showMessage("ERROR WITH THE SEARCH TITLE....Good Bye.", 2000)
            return

        ## Check if the search title is in the local refernce db
        searc_title = title.lower().replace(" ", "-")
        if searc_title in reference_dict:

            search_ez_id = int(reference_dict[searc_title][1])
            found_torrents_dict, found_torrents_count, ret_code = eztv_scraper.get_torrents(ez_id=search_ez_id)

            print(found_torrents_dict)

        else:
            found_torrents_dict, found_torrents_count, ret_code = eztv_scraper.get_torrents(movie_title=searc_title)

            print(found_torrents_dict)

        # self.ui.statusBar.showMessage("Starting the download... Please wait...")
        

        if ret_code == True:
            self.ui.dataNameLabel.setText(title)

            with open(resultPath, "w") as results_Fo:
                json.dump(found_torrents_dict, results_Fo, indent=2)

            QMessageBox.information(self, "Information!", f"Succsessfully downloaded database on \"{title.title()}\"\nThank Antony Later! #1960")
            self.ui.statusBar.showMessage("Done.", 2000)

        elif ret_code == False:
            QMessageBox.critical(self, "ERROR", "PLEASE CHECK YOUR INTERNET CONNECTION")
            self.ui.statusBar.showMessage(f"Error.. exit code >> {ret_code}", 2000)
  
    def displayResultOnTable(self, torrent_dictionary):

        table = self.ui.resutlTable

        rowPosition = table.rowCount()
        table.insertRow(rowPosition)

        ## Set column data
        table.setItem(rowPosition, 0, QTableWidgetItem(str(torrent_dictionary['title'])))
        table.setItem(rowPosition, 1, QTableWidgetItem(str(torrent_dictionary['size'])))
        table.setItem(rowPosition, 2, QTableWidgetItem(str(torrent_dictionary['seeds'])))
        table.setItem(rowPosition, 3, QTableWidgetItem(str(torrent_dictionary['magnet_link'])))

        ## Set text alignment
        table.item(rowPosition, 1).setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        table.item(rowPosition, 2).setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def searchCMD(self):

        season = self.ui.seasonSpin.text()
        episode = self.ui.episodeSpin.text()
        sort_value = self.ui.sortValueCombo.currentText().lower()

        resultDict = self.search_for(int(season), int(episode), sort_value=sort_value)

        # Clear all table rows and display results
        self.ui.resutlTable.setRowCount(0)
        for found_torrent_dict in resultDict:
            self.displayResultOnTable(found_torrent_dict[1])

    @pyqtSlot(QPoint)
    def on_customContextMenuRequested(self, pos):

        table = QApplication.focusWidget()
        tableName = table.objectName()

        if self.ui.resutlTable.rowCount() <= 0:
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

            webbrowser.open_new(magnet_link)

    def showMoreInfo(self):

        print("show more info")

        with open(resultPath, "r") as resultsFo:
           resultsDict = json.load(resultsFo)
           current_title = resultsDict["0"][0].lower().replace(" ", "-")
        
        with open(ref_Path, "r") as refFo:
           referenceDict = json.load(refFo)
           lis = referenceDict[current_title]
           title = current_title
           title_ID = lis[1]

        url = f"https://eztv.io/shows/{title_ID}/{title}/"
        image_url = f"https://eztv.io/ezimg/thumbs/{title}-{title_ID}.jpg"
        print(title_ID, title)

        webbrowser.open_new(url)
    
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

    def search_for(self, season=1, episode=1, sort_value='size', all=False):
        """ search for the season and episode in the results json file
            :returns: A List of touples with format (sort_value, torent_dictionary)
            sort_value ==> name=Name, size=Size, seeders=Seeders"""

        search_dictionary = OrderedDict()
        match_dictionary = OrderedDict()

        self.search_season = "{:02}".format(season)
        self.search_episode = "{:02}".format(episode)
        self.sort_value = sort_value
        self.all = all

        with open("./utils/resources/result.json", "r") as jsonFo:
            search_dictionary = json.load(jsonFo)

        counter = 1
        for _, ref_value in search_dictionary.items():

            ref_season = ref_value[6]
            ref_episode = ref_value[7]
            ref_name = ref_value[1]
            ref_size = ref_value[4]
            ref_seeds = ref_value[5]
            ref_magnet_link = ref_value[3]
            ref_torrent_link = ref_value[2]

            if "MB" in ref_size:
                mod_ref_size = float(ref_size.replace(" ", "").replace("MB", "").strip())
            elif "GB" in ref_size:
                mod_ref_size = float(ref_size.replace(" ", "").replace("GB", "").strip())
                mod_ref_size = mod_ref_size * 1e3
            else:
                mod_ref_size = float(ref_size)

            # Search to find if the searched <season> and <episode> are in an item's value
            if (ref_season == self.search_season) and (ref_episode == self.search_episode) and not self.all:
                # print("returning searched")
                "name=Name, size=Size, seeders=Seeders"
                if self.sort_value == "size":
                    match_dictionary[mod_ref_size + time.time()] = {"title": ref_name, "torrent_link": ref_torrent_link,
                                                                    "magnet_link": ref_magnet_link,
                                                                    "size": ref_size, "seeds": ref_seeds,
                                                                    "season": ref_season, "episode": ref_episode}
                elif self.sort_value == "name":
                    match_dictionary[ref_name] = {"title": ref_name, "torrent_link": ref_torrent_link,
                                                  "magnet_link": ref_magnet_link,
                                                  "size": ref_size, "seeds": ref_seeds, "season": ref_season,
                                                  "episode": ref_episode}
                elif self.sort_value == "seeders":
                    match_dictionary[float(ref_seeds) + float(time.time())] = {"title": ref_name,
                                                                               "torrent_link": ref_torrent_link,
                                                                               "magnet_link": ref_magnet_link,
                                                                               "size": ref_size, "seeds": ref_seeds,
                                                                               "season": ref_season,
                                                                               "episode": ref_episode}
                else:
                    match_dictionary[mod_ref_size + time.time()] = {"title": ref_name, "torrent_link": ref_torrent_link,
                                                                    "magnet_link": ref_magnet_link,
                                                                    "size": ref_size, "seeds": ref_seeds,
                                                                    "season": ref_season, "episode": ref_episode}

            if all:
                # print("returning all")
                if self.sort_value == "size":
                    match_dictionary[mod_ref_size + time.time()] = {"title": ref_name, "torrent_link": ref_torrent_link,
                                                                    "magnet_link": ref_magnet_link,
                                                                    "size": ref_size, "seeds": ref_seeds,
                                                                    "season": ref_season, "episode": ref_episode}
                elif self.sort_value == "name":
                    match_dictionary[ref_name] = {"title": ref_name, "torrent_link": ref_torrent_link,
                                                  "magnet_link": ref_magnet_link,
                                                  "size": ref_size, "seeds": ref_seeds, "season": ref_season,
                                                  "episode": ref_episode}
                elif self.sort_value == "seeders":
                    match_dictionary[float(ref_seeds) + float(time.time())] = {"title": ref_name,
                                                                               "torrent_link": ref_torrent_link,
                                                                               "magnet_link": ref_magnet_link,
                                                                               "size": ref_size, "seeds": ref_seeds,
                                                                               "season": ref_season,
                                                                               "episode": ref_episode}
                else:
                    match_dictionary[mod_ref_size + time.time()] = {"title": ref_name, "torrent_link": ref_torrent_link,
                                                                    "magnet_link": ref_magnet_link,
                                                                    "size": ref_size, "seeds": ref_seeds,
                                                                    "season": ref_season, "episode": ref_episode}

        # print(json.dumps(match_dictionary, sort_keys=True, indent=2))

        return sorted(match_dictionary.items())


if __name__ == "__main__":

    w = QApplication([])
    app = App()
    app.show()
    w.exec_()



















