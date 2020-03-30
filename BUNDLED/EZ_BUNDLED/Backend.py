import urllib.request
from bs4 import BeautifulSoup
import json
from ast import literal_eval
import operator, webbrowser
from PyQt5.QtCore import QPoint, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QMessageBox, QTableWidgetItem, QApplication, QMenu
from utils.design_files.MainDesign import *



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
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.ui.resutlTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.resutlTable.customContextMenuRequested.connect(self.on_customContextMenuRequested)

        ## get the current database title and set the "dataNameLable"
        try:
            with open("utils\\resources\\result.json") as titlesOb:
                currentTitle = json.load(titlesOb)["0"][0]
                self.ui.dataNameLabel.setText(currentTitle)
        except:
            self.ui.dataNameLabel.setText(None)

    def getTitles(self):
        """get the titles available from the 'titles' database"""

        with open("utils/resources/EZTV_RFERENCE_DICTIONARY.json") as titlesOb:
            data = json.load(titlesOb)
            titles = [k.replace("-", " ").title() for k,v in data.items()]
            titles.insert(0, "Select A Title...")
        
        return titles

    def getDataCMD(self):
        """command that downloads the TITLE's data ie call the download data for method"""

        title = ""

        if (self.ui.enterCheck.isChecked()) and (self.ui.titleEdit.text() != ""):
            title = self.ui.titleEdit.text()
        elif (self.ui.chooseCheck.isChecked()) and (self.ui.titleCombo.currentText() != "Select A Title..."):
            title = self.ui.titleCombo.currentText()
        else:
            self.ui.statusBar.showMessage("ERROR WITH THE SEARCH TITLE....Good Bye.", 2000)
            return

        # self.ui.statusBar.showMessage("Starting the download... Please wait...")
        
        ret = downloadDataFor(title)

        if ret:
            self.ui.dataNameLabel.setText(title)
            QMessageBox.information(self, "Information!", f"Succsessfully downloaded database on \"{title.title()}\"\nThank Antony Later! #1960")
            self.ui.statusBar.showMessage("Done.", 2000)
        elif ret == 402:
            QMessageBox.critical(self, "ERROR", "PLEASE CHECK YOUR INTERNET CONNECTION")
            self.ui.statusBar.showMessage(f"Error.. exit code >> {ret}", 2000)
  
    def displayResultOnTable(self, values):

        table = self.ui.resutlTable

        rowPosition = table.rowCount()
        table.insertRow(rowPosition)
        
        pos = 0
        for value in values:
            table.setItem(rowPosition, pos, QTableWidgetItem(str(value)))
            pos+=1

    def searchCMD(self):

        season = self.ui.seasonSpin.text()
        episode = self.ui.episodeSpin.text()
        sortvalue = self.ui.sortValueCombo.currentText()

        if sortvalue == "Size":
            sv=4
        elif sortvalue ==  "Name":
            sv=1
        elif sortvalue == "Seeders":
            sv=6
        else:
            sv=4
        
        resultDict = search_for(int(season), int(episode), sortValue=sv)

        # Clear all table rows and display results
        self.ui.resutlTable.setRowCount(0)
        for title, values in resultDict.items():
            vals = [title, *values]
            self.displayResultOnTable(vals)

    @pyqtSlot(QPoint)
    def on_customContextMenuRequested(self, pos):

        table = QApplication.focusWidget()
        tableName = table.objectName()

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
        _open = menu.addAction("Open in uTorrent")
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

        with open("utils\\resources\\result.json", "r") as resultsFo:
           resultsDict = json.load(resultsFo)
           current_title = resultsDict["0"][0].lower().replace(" ", "-")
        
        with open("utils\\resources\\ref_.json", "r") as refFo:
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


def downloadDataFor(movieTitle):
    """create a json file containing the EZYV torrents result of 'movieTitle' """
    with open("utils\\resources\\ref_.json", "r")as f0:
        refDict = json.load(f0)

    movie_result_dictionary = {}
    movie = str(movieTitle)
    url = "https://eztv.io/search/{}".format(movie)
    count = 0

    try:
        hdr = {"User-Agent": "Mozila/5.0"}
        req = urllib.request.Request(url, headers=hdr)
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page, "html.parser")
    except Exception as e:
        # print(e.args)
        # print("CHECK YOUR INTERNET CONNECTION")
        return 402

    # returns a list of all the <tr> tags under class forum_header_border
    tr_tags = soup.find_all("tr", {"class": "forum_header_border", "name": "hover"})

    for tr_elements in tr_tags:

        # print(count)

        tb_tags = tr_elements.find_all("td")

        title = tb_tags[1].find("a").get("title")
        try:
            torrent1 = tb_tags[2].find("a", {"class": "download_1"}).get("href")  # torrent file
        except:
            torrent1 = None
        try:
            torrent2 = tb_tags[2].find("a", {"class": "magnet"}).get("href")  # torrent magnet
        except:
            torrent2 = None
        size = tb_tags[3].text
        releaseDate = tb_tags[4].text
        seeds = tb_tags[5].text

        try:
            for se in title.split(" "):
                try:
                    if (se.startswith("S")) and (se.index("E") == 3) and (type(literal_eval(se[2]))):
                        x = se
                except:
                    pass

            Se, Ep = x.replace("S", "").split("E")
        except:
            Se, Ep = None, None

        movie_result_dictionary[count] = [movieTitle.title(), title, torrent1, torrent2, size, releaseDate, seeds, Se, Ep]

        count += 1

        with open("utils\\resources\\result.json", "w") as resultFo:
            json.dump(movie_result_dictionary, resultFo, indent=2)

    # print("Done\n")
    return 1

def search_for(Se=1, Ep=1, sortValue=4):
    """search for the season and episode in the results json
        sortValue ==> 1=Name, 4=Size, 6=Seeders"""
    dic = {}
    resulstDict = {}

    Se = "{:02}".format(Se)
    Ep = "{:02}".format(Ep)


    with open("utils\\resources\\result.json", "r") as jsonFo:
        resultDictionary = json.load(jsonFo)

    x = 0
    for k in resultDictionary.values():
        if (k[-2] == Se) and (k[-1] == Ep):
            # print(k)
            # print("title:{}\nsize:{}\nseeders:{}\ntorrent_link:{}\n".format(k[1], k[4], k[6], k[3]))  # print the result, returns a list of values
            # print("\n")
            x += 1
            # sort by k[value]
            dic[k[sortValue]] = [k[1], k[4], k[6], k[3]]

    # return a sorted list sorted by the index of the desired value ie 4=size"
    for k2, v in sorted(dic.items()):
        # print(v)
        resulstDict[v[0]] = (v[1], v[2], v[3])
        # print("title:{}\nsize:{}\nseeders:{}\ntorrent_link:{}\n".format(v[0], v[1], v[2], v[3]))
        # print("\n")
    
    # print(x, " torrents found")

    return resulstDict





















