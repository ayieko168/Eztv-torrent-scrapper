
import os

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from src.design_files.ui_mainWindow import Ui_MainWindow
from src.ui_utils import *
from src.utils import *

# Global Variables
ROOT_DIR = f"{os.sep}".join(os.path.abspath(__file__).split(os.sep)[:-1])


## Global Functions
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainApp(QMainWindow):

    def __init__(self):

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## Variables
        self.settings = {}

        ## Setup functions
        self.setup_ui()
        self.initial_ui_setup()
        self.setup_ui_connections()

    def setup_ui(self):

        ## Setup the icons
        icon = QIcon()
        icon.addFile(resource_path("src/imgs/scrape.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.ui.start_scraping_button.setIcon(icon)
        icon.addFile(resource_path("src/imgs/stop.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.ui.stop_scraping_button.setIcon(icon)
        icon = QIcon()
        icon.addFile(resource_path("src/imgs/torrent_icon.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        ## Load the settings
        with open(resource_path("src/settings.json"), "r") as fo: self.settings = json.load(fo)

    def initial_ui_setup(self):

        ## Verify root path
        if not os.path.isdir(ROOT_DIR): show_error(self, "Could not get the root path. Report this as a bug and try Re-Installing the Application.")

        ## Remove focus from the keyword edit
        if self.settings['keywordFocus']: self.ui.start_scraping_button.setFocus()

        ## Clear the keyword and search term edits
        self.ui.keyword_edit.clear()
        self.ui.search_term_edit.clear()

        ## Set the default values for the season and episode spin boxes
        self.ui.season_spin.setValue(1)
        self.ui.episode_spin.setValue(1)

    def setup_ui_connections(self):

        self.ui.scrape_for_combo.currentIndexChanged.connect(self.change_scrapers_in_combo)

    def change_scrapers_in_combo(self):
        """This function changes the scraper options available for use when changing the 'scrape for' combo box options"""

        if self.ui.scrape_for_combo.currentText().lower() == "Tv-Shows".lower():
            log("[APPLICATION] Changed to the scrape for option to TV-Show")
            tv_scrapers = list(dict(self.settings['tv-scrapers']).keys())
            print(tv_scrapers)
            return
            self.ui.scraperCombo.clear()
            self.ui.scraperCombo.addItems(tv_scrapers)
            self.ui.titleEdit.setPlaceholderText("Enter Tv-Show Title")






















if __name__ == "__main__":

    w = QApplication([])

    app = MainApp()
    app.show()

    w.exec()


































