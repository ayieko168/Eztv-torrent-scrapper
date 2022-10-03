# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindowprOoCb.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFrame, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStackedWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1032, 728)
        icon = QIcon()
        icon.addFile(u"C:/Users/RoyalState/.designer/imgs/torrent_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionUpdate = QAction(MainWindow)
        self.actionUpdate.setObjectName(u"actionUpdate")
        self.actionReset_All = QAction(MainWindow)
        self.actionReset_All.setObjectName(u"actionReset_All")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFocusPolicy(Qt.StrongFocus)
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 140))
        self.groupBox.setMaximumSize(QSize(16777215, 150))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.keyword_edit = QLineEdit(self.groupBox)
        self.keyword_edit.setObjectName(u"keyword_edit")
        self.keyword_edit.setMinimumSize(QSize(350, 30))
        self.keyword_edit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.keyword_edit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_6)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.scrape_for_combo = QComboBox(self.groupBox)
        self.scrape_for_combo.addItem("")
        self.scrape_for_combo.addItem("")
        self.scrape_for_combo.addItem("")
        self.scrape_for_combo.addItem("")
        self.scrape_for_combo.addItem("")
        self.scrape_for_combo.addItem("")
        self.scrape_for_combo.setObjectName(u"scrape_for_combo")
        self.scrape_for_combo.setMinimumSize(QSize(120, 24))

        self.horizontalLayout_2.addWidget(self.scrape_for_combo)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.scrape_from_combo = QComboBox(self.groupBox)
        self.scrape_from_combo.setObjectName(u"scrape_from_combo")
        self.scrape_from_combo.setMinimumSize(QSize(120, 24))

        self.horizontalLayout_3.addWidget(self.scrape_from_combo)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.show_status_check = QCheckBox(self.groupBox)
        self.show_status_check.setObjectName(u"show_status_check")
        self.show_status_check.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_4.addWidget(self.show_status_check)

        self.start_scraping_button = QPushButton(self.groupBox)
        self.start_scraping_button.setObjectName(u"start_scraping_button")
        self.start_scraping_button.setMinimumSize(QSize(130, 26))
        icon1 = QIcon()
        icon1.addFile(u"C:/Users/RoyalState/.designer/imgs/scrape.png", QSize(), QIcon.Normal, QIcon.Off)
        self.start_scraping_button.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.start_scraping_button)

        self.stop_scraping_button = QPushButton(self.groupBox)
        self.stop_scraping_button.setObjectName(u"stop_scraping_button")
        self.stop_scraping_button.setMinimumSize(QSize(0, 24))
        self.stop_scraping_button.setMaximumSize(QSize(60, 16777215))
        icon2 = QIcon()
        icon2.addFile(u"C:/Users/RoyalState/.designer/imgs/stop.png", QSize(), QIcon.Normal, QIcon.Off)
        self.stop_scraping_button.setIcon(icon2)

        self.horizontalLayout_4.addWidget(self.stop_scraping_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.line_4 = QFrame(self.frame)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setMinimumSize(QSize(0, 20))
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_4)

        self.stackedWidget = QStackedWidget(self.frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_8 = QVBoxLayout(self.page)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(3, 3, 3, 3)
        self.groupBox_2 = QGroupBox(self.page)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.currnet_database_label = QLabel(self.groupBox_2)
        self.currnet_database_label.setObjectName(u"currnet_database_label")

        self.horizontalLayout_5.addWidget(self.currnet_database_label)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.more_information_button = QPushButton(self.groupBox_2)
        self.more_information_button.setObjectName(u"more_information_button")

        self.horizontalLayout_6.addWidget(self.more_information_button)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.groupBox_3 = QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_11 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_11.setSpacing(10)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.season_check = QCheckBox(self.groupBox_3)
        self.season_check.setObjectName(u"season_check")
        self.season_check.setChecked(True)

        self.horizontalLayout_9.addWidget(self.season_check)

        self.season_spin = QSpinBox(self.groupBox_3)
        self.season_spin.setObjectName(u"season_spin")
        self.season_spin.setMinimumSize(QSize(50, 0))
        self.season_spin.setMinimum(1)
        self.season_spin.setMaximum(999)

        self.horizontalLayout_9.addWidget(self.season_spin)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.episode_check = QCheckBox(self.groupBox_3)
        self.episode_check.setObjectName(u"episode_check")
        self.episode_check.setChecked(True)

        self.horizontalLayout_10.addWidget(self.episode_check)

        self.episode_spin = QSpinBox(self.groupBox_3)
        self.episode_spin.setObjectName(u"episode_spin")
        self.episode_spin.setMinimumSize(QSize(50, 0))
        self.episode_spin.setMinimum(1)
        self.episode_spin.setMaximum(999)

        self.horizontalLayout_10.addWidget(self.episode_spin)


        self.verticalLayout_5.addLayout(self.horizontalLayout_10)


        self.horizontalLayout_11.addLayout(self.verticalLayout_5)

        self.line_2 = QFrame(self.groupBox_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_11.addWidget(self.line_2)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.search_term_check = QCheckBox(self.groupBox_3)
        self.search_term_check.setObjectName(u"search_term_check")

        self.horizontalLayout_8.addWidget(self.search_term_check)

        self.search_term_edit = QLineEdit(self.groupBox_3)
        self.search_term_edit.setObjectName(u"search_term_edit")

        self.horizontalLayout_8.addWidget(self.search_term_edit)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.display_all_data_check = QCheckBox(self.groupBox_3)
        self.display_all_data_check.setObjectName(u"display_all_data_check")

        self.verticalLayout_6.addWidget(self.display_all_data_check)


        self.horizontalLayout_11.addLayout(self.verticalLayout_6)

        self.line_3 = QFrame(self.groupBox_3)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_11.addWidget(self.line_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_7.addWidget(self.label_5)

        self.sort_by_combo = QComboBox(self.groupBox_3)
        self.sort_by_combo.addItem("")
        self.sort_by_combo.addItem("")
        self.sort_by_combo.addItem("")
        self.sort_by_combo.setObjectName(u"sort_by_combo")
        self.sort_by_combo.setMinimumSize(QSize(120, 24))

        self.horizontalLayout_7.addWidget(self.sort_by_combo)


        self.horizontalLayout_11.addLayout(self.horizontalLayout_7)

        self.line_5 = QFrame(self.groupBox_3)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_11.addWidget(self.line_5)

        self.horizontalSpacer_5 = QSpacerItem(252, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_5)

        self.line_6 = QFrame(self.groupBox_3)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_11.addWidget(self.line_6)

        self.filter_button = QPushButton(self.groupBox_3)
        self.filter_button.setObjectName(u"filter_button")
        self.filter_button.setMinimumSize(QSize(100, 50))
        self.filter_button.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_11.addWidget(self.filter_button)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.groupBox_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.results_table = QTableWidget(self.groupBox_4)
        if (self.results_table.columnCount() < 4):
            self.results_table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.results_table.setObjectName(u"results_table")
        self.results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.results_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_7.addWidget(self.results_table)


        self.verticalLayout_4.addWidget(self.groupBox_4)


        self.verticalLayout_8.addWidget(self.groupBox_2)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_9 = QVBoxLayout(self.page_2)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.page_2)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, -1, 0, -1)
        self.log_text = QTextEdit(self.frame_2)
        self.log_text.setObjectName(u"log_text")
        self.log_text.setFrameShape(QFrame.NoFrame)
        self.log_text.setFrameShadow(QFrame.Plain)
        self.log_text.setReadOnly(True)

        self.horizontalLayout_12.addWidget(self.log_text)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setSpacing(12)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_2)

        self.back_button = QPushButton(self.frame_2)
        self.back_button.setObjectName(u"back_button")

        self.verticalLayout_10.addWidget(self.back_button)

        self.clear_button = QPushButton(self.frame_2)
        self.clear_button.setObjectName(u"clear_button")

        self.verticalLayout_10.addWidget(self.clear_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_10.addItem(self.verticalSpacer)

        self.auto_scroll = QCheckBox(self.frame_2)
        self.auto_scroll.setObjectName(u"auto_scroll")

        self.verticalLayout_10.addWidget(self.auto_scroll)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_3)


        self.horizontalLayout_12.addLayout(self.verticalLayout_10)


        self.verticalLayout_9.addWidget(self.frame_2)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_3.addWidget(self.stackedWidget)


        self.verticalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1032, 22))
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName(u"menuOptions")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuOptions.menuAction())
        self.menuOptions.addAction(self.actionSettings)
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.actionUpdate)
        self.menuOptions.addAction(self.actionReset_All)
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.actionExit)

        self.retranslateUi(MainWindow)
        self.season_check.toggled.connect(self.season_spin.setEnabled)
        self.episode_check.toggled.connect(self.episode_spin.setEnabled)
        self.search_term_check.toggled.connect(self.search_term_edit.setEnabled)

        self.start_scraping_button.setDefault(True)
        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"EZTV Torrent Scraper - Find Any Torrent!", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionUpdate.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.actionReset_All.setText(QCoreApplication.translate("MainWindow", u"Reset All", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Srape For Movie/Show/Subtitle/Socce-Streams/Anime Data", None))
#if QT_CONFIG(tooltip)
        self.keyword_edit.setToolTip(QCoreApplication.translate("MainWindow", u"Enter the keyword you want to search/scrape for.\n"
"You can, for example, enter Game Of thrones to get\n"
"all the torrents available for GOT and\n"
"then later filter the Sraped data for what you want exactly.", None))
#endif // QT_CONFIG(tooltip)
        self.keyword_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Keyword... Example: Game Of Thrones", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>HINT: Only search <span style=\" font-weight:700;\">ONCE</span> then use the filter option to filter what to download or use. Hover over buttons to get help.</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Scrape For : ", None))
        self.scrape_for_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"Tv-Shows", None))
        self.scrape_for_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"Movies", None))
        self.scrape_for_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"Subtitles", None))
        self.scrape_for_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"Soccer-Streams", None))
        self.scrape_for_combo.setItemText(4, QCoreApplication.translate("MainWindow", u"Anime", None))
        self.scrape_for_combo.setItemText(5, QCoreApplication.translate("MainWindow", u"General", None))

#if QT_CONFIG(tooltip)
        self.scrape_for_combo.setToolTip(QCoreApplication.translate("MainWindow", u"Here you the category of media your search is from.", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Server To Scrape From :", None))
#if QT_CONFIG(tooltip)
        self.scrape_from_combo.setToolTip(QCoreApplication.translate("MainWindow", u"Here you select the popular websites from where you\n"
"want to scrape the data from.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.show_status_check.setToolTip(QCoreApplication.translate("MainWindow", u"Keep this option checked to see the scraper working.", None))
#endif // QT_CONFIG(tooltip)
        self.show_status_check.setText(QCoreApplication.translate("MainWindow", u"Show Scrape Status", None))
#if QT_CONFIG(tooltip)
        self.start_scraping_button.setToolTip(QCoreApplication.translate("MainWindow", u"This button starts the scraping process and will search for\n"
"the Keyword in the selected site and return the found data.", None))
#endif // QT_CONFIG(tooltip)
        self.start_scraping_button.setText(QCoreApplication.translate("MainWindow", u"Start Scraping", None))
#if QT_CONFIG(tooltip)
        self.stop_scraping_button.setToolTip(QCoreApplication.translate("MainWindow", u"This button will stop the scraping process.", None))
#endif // QT_CONFIG(tooltip)
        self.stop_scraping_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Filter The Data You Have Scraped", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Current Database : ", None))
        self.currnet_database_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700; color:#313131;\">Game Of Thones</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.more_information_button.setToolTip(QCoreApplication.translate("MainWindow", u"This button will try to get more details of the KEYWORD and display it in your browser.", None))
#endif // QT_CONFIG(tooltip)
        self.more_information_button.setText(QCoreApplication.translate("MainWindow", u"More Information on <Movie Name>", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Filter Options: ", None))
#if QT_CONFIG(tooltip)
        self.season_check.setToolTip(QCoreApplication.translate("MainWindow", u"In case you are scraping for a Tv-Show\n"
"this will only filter in the season you set here.", None))
#endif // QT_CONFIG(tooltip)
        self.season_check.setText(QCoreApplication.translate("MainWindow", u"Season  ", None))
#if QT_CONFIG(tooltip)
        self.season_spin.setToolTip(QCoreApplication.translate("MainWindow", u"In case you are scraping for a Tv-Show\n"
"this will only filter in the season you set here.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.episode_check.setToolTip(QCoreApplication.translate("MainWindow", u"In case you are scraping for a Tv-Show\n"
"this will only filter in the episode you set here.", None))
#endif // QT_CONFIG(tooltip)
        self.episode_check.setText(QCoreApplication.translate("MainWindow", u"Episode", None))
#if QT_CONFIG(tooltip)
        self.episode_spin.setToolTip(QCoreApplication.translate("MainWindow", u"In case you are scraping for a Tv-Show\n"
"this will only filter in the episode you set here.", None))
#endif // QT_CONFIG(tooltip)
        self.search_term_check.setText(QCoreApplication.translate("MainWindow", u"Search Term: ", None))
        self.display_all_data_check.setText(QCoreApplication.translate("MainWindow", u"Display All Data", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Sort Results By: ", None))
        self.sort_by_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"Name or Title", None))
        self.sort_by_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"Seeders", None))
        self.sort_by_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"Torrent Size", None))

#if QT_CONFIG(tooltip)
        self.filter_button.setToolTip(QCoreApplication.translate("MainWindow", u"Filter the scraped data for what you want according to the set filter options.\n"
"This can be done more than once.", None))
#endif // QT_CONFIG(tooltip)
        self.filter_button.setText(QCoreApplication.translate("MainWindow", u"FIlter", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Filter Results : ", None))
        ___qtablewidgetitem = self.results_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Torrent Name", None));
        ___qtablewidgetitem1 = self.results_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Torrent Size", None));
        ___qtablewidgetitem2 = self.results_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Seeders", None));
        ___qtablewidgetitem3 = self.results_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Magnet Link", None));
        self.back_button.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.clear_button.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.auto_scroll.setText(QCoreApplication.translate("MainWindow", u"Auto Scroll", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi

