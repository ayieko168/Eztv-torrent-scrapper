
import os

from src.design_files.ui_mainWindow import Ui_MainWindow
from src.ui_utils import *
from src.utils import *
from src.scrapers import *
from datetime import datetime

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
        self.movie_titles = []
        self.show_titles = []
        self.movies_and_shows = {}
        self.eztv_scraper = EZTV(self)
        self.threadpool = QThreadPool()

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

        ## Load the movie titles
        with open(resource_path("src/title_scrapers/yifi_movie_titles.json"), "r") as fo: self.movie_titles = list(json.load(fo).keys())
        with open(resource_path("src/title_scrapers/tvmaze_show_titles.json"), 'r') as fo: self.show_titles = list(json.load(fo).keys())
        suggestions_list = self.movie_titles + self.show_titles

        movie_completer = QCompleter(suggestions_list, self)
        movie_completer.setCaseSensitivity(Qt.CaseInsensitive)
        movie_completer.setMaxVisibleItems(10)
        movie_completer.setFilterMode(Qt.MatchContains)
        self.ui.keyword_edit.setCompleter(movie_completer)

        ## Load all the locally available movie and show titles
        with open(resource_path("src/title_scrapers/yifi_movie_titles.json"), "r") as fo: self.movies_and_shows.update(json.load(fo))
        with open(resource_path("src/title_scrapers/tvmaze_show_titles.json"), 'r') as fo: self.movies_and_shows.update(json.load(fo))

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

        ## Set the scraper combo values
        scrapers = list(dict(self.settings['tv-scrapers']).keys()) + ["All Sites"]
        self.ui.scrape_from_combo.setCurrentIndex(0)
        self.ui.scrape_from_combo.clear()
        self.ui.scrape_from_combo.addItems(scrapers)

        ## Set up the first page on stack
        self.ui.stackedWidget.setCurrentIndex(0)

        ## Initial search check state
        self.ui.search_term_check.setChecked(False)
        self.ui.search_term_edit.setEnabled(False)

        ## Reset the name of the more option button
        self.ui.more_information_button.setText("More Information")

        ## Setup the default auto scroll state
        self.ui.auto_scroll.setChecked(True)

    def setup_ui_connections(self):

        ## Combo Boxes
        self.ui.scrape_for_combo.currentIndexChanged.connect(self.change_scrapers_in_combo)

        ## buttons
        self.ui.back_button.clicked.connect(self.back_button_command)
        self.ui.display_all_data_check.clicked.connect(self.display_all_data_handler)
        self.ui.start_scraping_button.clicked.connect(self.start_scraping_operation)

        ## Combo box
        self.ui.show_status_check.toggled.connect(self.show_details_handler)

    def change_scrapers_in_combo(self):
        """This function changes the scraper options available for use when changing the 'scrape for' combo box options"""

        if self.ui.scrape_for_combo.currentText().lower() == "Tv-Shows".lower():
            log("[APPLICATION] Changed to the scrape for option to TV-Show")
            scrapers = list(dict(self.settings['tv-scrapers']).keys()) + ["All Sites"]
            self.ui.scrape_from_combo.clear()
            self.ui.scrape_from_combo.addItems(scrapers)

        elif self.ui.scrape_for_combo.currentText().lower() == "Movies".lower():
            log("[APPLICATION] Changed to the scrape for option to Movies")
            scrapers = list(dict(self.settings['movie-scrapers']).keys()) + ["All Sites"]
            self.ui.scrape_from_combo.clear()
            self.ui.scrape_from_combo.addItems(scrapers)

        elif self.ui.scrape_for_combo.currentText().lower() == "Subtitles".lower():
            log("[APPLICATION] Changed to the scrape for option to Subtitles")
            scrapers = list(dict(self.settings['subtitle-scrapers']).keys()) + ["All Sites"]
            self.ui.scrape_from_combo.clear()
            self.ui.scrape_from_combo.addItems(scrapers)

        elif self.ui.scrape_for_combo.currentText().lower() == "Soccer-Streams".lower():
            log("[APPLICATION] Changed to the scrape for option to Soccer-Streams")
            scrapers = list(dict(self.settings['soccer-scrapers']).keys()) + ["All Sites"]
            self.ui.scrape_from_combo.clear()
            self.ui.scrape_from_combo.addItems(scrapers)

        elif self.ui.scrape_for_combo.currentText().lower() == "Anime".lower():
            log("[APPLICATION] Changed to the scrape for option to Anime")
            scrapers = list(dict(self.settings['anime-scrapers']).keys()) + ["All Sites"]
            self.ui.scrape_from_combo.clear()
            self.ui.scrape_from_combo.addItems(scrapers)

        elif self.ui.scrape_for_combo.currentText().lower() == "General".lower():
            log("[APPLICATION] Changed to the scrape for option to General")
            scrapers = list(dict(self.settings['general-scrapers']).keys()) + ["All Sites"]
            self.ui.scrape_from_combo.clear()
            self.ui.scrape_from_combo.addItems(scrapers)

    def show_details_handler(self):

        if self.ui.show_status_check.isChecked():
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

    def back_button_command(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.show_status_check.setChecked(False)

    def display_all_data_handler(self):

        ## Disable the relevant widgets
        if self.ui.display_all_data_check.isChecked():
            self.ui.season_check.setEnabled(False)
            self.ui.season_spin.setEnabled(False)
            self.ui.episode_check.setEnabled(False)
            self.ui.episode_spin.setEnabled(False)

            ## TODO: Show all the data scraped in the table

        else:
            self.ui.season_check.setEnabled(True)
            self.ui.season_spin.setEnabled(True)
            self.ui.episode_check.setEnabled(True)
            self.ui.episode_spin.setEnabled(True)

            ## TODO: Clear all the data from the table

    def log_to_widget(self, message: str):

        log_text = f">>> [{datetime.now().strftime('%H:%M:%S')}] {str(message).title().strip()}\n"

        if self.ui.auto_scroll.isChecked():
            self.ui.log_text.moveCursor(QTextCursor.End)
            self.ui.log_text.insertPlainText(log_text)
        else:
            self.ui.log_text.insertPlainText(log_text)

    def tabulate_data(self, data: list):

        ## Clear the table
        self.ui.results_table.setRowCount(0)

        for item in data:

            ## poulate the data
            table = self.ui.results_table
            rowPosition = table.rowCount()
            table.insertRow(rowPosition)

            ## Set column data
            table.setItem(rowPosition, 0, QTableWidgetItem(str(item['title'])))  # Title
            table.setItem(rowPosition, 1, QTableWidgetItem(str(item['size_bytes'])))  # Size
            table.setItem(rowPosition, 2, QTableWidgetItem(str(item['seeds'])))  # Seeds
            table.setItem(rowPosition, 3, QTableWidgetItem(str(item['magnet_url'])))  # Magnet link

    def start_scraping_operation(self):

        ## Get the title
        search_keyword = self.ui.keyword_edit.text()
        search_imdb_id = self.movies_and_shows.get(search_keyword)

        ## Get the selected scraper
        scrape_from = self.ui.scrape_from_combo.currentText()
        print(scrape_from)

        ## Choose the right scraper
        if scrape_from == "EZTV":
            if search_imdb_id is not None:

                ## Move the page
                self.ui.show_status_check.toggle()

                ## Start the search queue
                worker = SigWorker(lambda sigs: self.eztv_scraper.get_show_by_imdb_id(search_imdb_id, sigs))
                worker.signals.message_signal.connect(put_toast)
                worker.signals.log_data.connect(self.log_to_widget)
                worker.signals.finished.connect(self.ui.show_status_check.toggle)
                worker.signals.finished_tabulate.connect(lambda table_data: self.tabulate_data(table_data))

                ## Disable the widgets
                self.ui.start_scraping_button.setEnabled(False)

                ## Start thread
                self.threadpool.start(worker)









class SigWorker(QRunnable):

    def __init__(self, func, *args, **kwargs):

        super(SigWorker, self).__init__()

        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        self.func(self.signals)








if __name__ == "__main__":

    w = QApplication([])

    app = MainApp()
    app.show()

    w.exec()


































