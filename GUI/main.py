import urllib.request
from bs4 import BeautifulSoup
import json
from ast import literal_eval
import operator, webbrowser
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from MainDesign import *


class App(QMainWindow):

    def __init__(self):

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.titleCombo.addItems(self.getTitles())
        self.ui.getDataButton.clicked.connect(self.getDataCMD)
        self.ui.searchButton.clicked.connect(self.searchCMD)
        
        ## SETUP TABLE
        header = self.ui.resutlTable.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)

        self.ui.resutlTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.resutlTable.customContextMenuRequested.connect(self.on_customContextMenuRequested)


    def getTitles(self):

        with open("EZTV_titles.json") as titlesOb:
            data = json.load(titlesOb)
            titlesList = data["titles"]
            titlesList.insert(0, "Select A Title...")
        
        return titlesList

    def getDataCMD(self):

        title = ""

        if (self.ui.enterCheck.isChecked()) and (self.ui.titleEdit.text() != ""):
            title = self.ui.titleEdit.text()
        
        elif (self.ui.chooseCheck.isChecked()) and (self.ui.titleCombo.currentText() != "Select A Title..."):
            title = self.ui.titleCombo.currentText()
        else:
            print("ERROR WITH THE SEARCH TITLE")
            print("Good Bye.")
            return

        downloadDataFor(title)

    def displayResultOnTable(self, values):

        table = self.ui.resutlTable

        rowPosition = table.rowCount()
        table.insertRow(rowPosition)
        
        pos = 0
        for value in values:
            table.setItem(rowPosition, pos, QtGui.QTableWidgetItem(str(value)))
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
            

def downloadDataFor(movieTitle):
    """create a json file containing the EZYV torrents result of 'movieTitle' """
    with open("ref_.json", "r")as f0:
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
        print(e.args)
        print("CHECK YOUR INTERNET CONNECTION")
        return

    # returns a list of all the <tr> tags under class forum_header_border
    tr_tags = soup.find_all("tr", {"class": "forum_header_border", "name": "hover"})

    for tr_elements in tr_tags:

        print(count)

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
            x = [se for se in title.split(" ") if se.startswith("S") and se.index("E") == 3][0]
            Se, Ep = x.replace("S", "").split("E")
        except:
            Se, Ep = None, None

        movie_result_dictionary[count] = [movieTitle.title(), title, torrent1, torrent2, size, releaseDate, seeds, Se, Ep]

        count += 1

        with open("result.json", "w") as resultFo:
            json.dump(movie_result_dictionary, resultFo, indent=2)

    print("Done\n")

def search_for(Se=1, Ep=1, sortValue=4):
    """search for the season and episode in the results json
        sortValue ==> 1=Name, 4=Size, 6=Seeders"""
    dic = {}
    resulstDict = {}

    Se = "{:02}".format(Se)
    Ep = "{:02}".format(Ep)


    with open("result.json", "r") as jsonFo:
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



if __name__ == "__main__":

    w = QApplication([])
    app = App()
    app.show()
    w.exec_()


















