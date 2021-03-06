import os
import sys
import time
import math
import traceback
import configparser
import matplotlib
matplotlib.use("TkAgg")     # This needs to happen before import any other things from matplotlib.
from random import randint
from sys import platform as _platform
import io
from PyQt5 import *
from PyQt5 import uic, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Modules import modules     # Names of all existing modules are stored in a separate file called "Modules.py".

import importlib

__thisversion__ = 0
darkthemeavailable = 1

try:
    import qdarkstyle
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    darkthemeavailable = 0

__version__ = "3.09" + "/" + "{:.2f}".format(__thisversion__)
__emailaddress__ = "pman3@uic.edu"


def resource_path(relative_path):   # Define function to import external files when using PyInstaller.
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


qtmainfile = resource_path("mainwindow.ui")  # GUI layout file.
Ui_main, QtBaseClass = uic.loadUiType(qtmainfile)
qtwelcomefile = resource_path("welcome.ui")
Ui_welcome, QtBaseClass = uic.loadUiType(qtwelcomefile)
qthelpfile = resource_path("help.ui")
Ui_help, QtBaseClass = uic.loadUiType(qthelpfile)
qtguessfile = resource_path("guessnumbers.ui")
Ui_guess, QtBaseClass = uic.loadUiType(qtguessfile)

config = configparser.ConfigParser()
config.read(resource_path('configuration.ini'))
colortheme = int(config["Settings"]["colortheme"])
fullscreenonstart = int(config["Mainwindow"]["fullscreenonstart"])

if darkthemeavailable == 1:
    if colortheme == 1:
        plt.rcParams.update({
            "lines.color": "white",
            "patch.edgecolor": "white",
            "text.color": "white",
            "axes.facecolor": "#31363b",
            "axes.edgecolor": "lightgray",
            "axes.labelcolor": "white",
            "xtick.color": "white",
            "ytick.color": "white",
            "grid.color": "lightgray",
            "figure.facecolor": "#31363b",
            "figure.edgecolor": "#31363b",
            "savefig.facecolor": "#31363b",
            "savefig.edgecolor": "#31363b"})
    elif colortheme == 2:
        plt.style.use('dark_background')  # Default Matplotlib theme.


class welcome_GUI(QWidget, Ui_welcome):
    """Welcome window."""

    def __init__(self):
        QWidget.__init__(self)
        Ui_welcome.__init__(self)
        self.setupUi(self)


class help_GUI(QWidget, Ui_help):
    """Documentation window."""

    def __init__(self):
        QWidget.__init__(self)
        Ui_help.__init__(self)
        self.setupUi(self)

        self.currentindex = 0
        self.numberofpages = 0

        self.stackedWidget.removeWidget(self.page_2)
        self.stackedWidget.setCurrentIndex(self.currentindex)

        self.shortcut1 = QShortcut(QtGui.QKeySequence(Qt.Key_Right), self)
        self.shortcut1.activated.connect(self.next)
        self.shortcut2 = QShortcut(QtGui.QKeySequence(Qt.Key_Left), self)
        self.shortcut2.activated.connect(self.previous)

        self.textEdit.setStyleSheet("background: rgba(0,0,255,0%)")

        self.load_all_help_files()

    def load_all_help_files(self):
        for module_name, window_type, module_title in modules:
            folder_name = ""
            for i in range(0, len(module_name)):
                if module_name[i] == ".":
                    folder_name = module_name[0:i]
                    break
            try:
                path = resource_path(os.path.join(folder_name, "help.txt"))
                textbox = QTextEdit()
                textbox.setStyleSheet("background: rgba(0,0,255,0%)")
                textbox.setReadOnly(True)
                f = open(path, "r", encoding='utf-8')
                text = f.readlines()
                for line in text:
                    textbox.append(line)
                f.close()
                textbox.verticalScrollBar().setValue(300)
                self.stackedWidget.addWidget(textbox)
                self.numberofpages += 1
            except FileNotFoundError:
                pass

    def next(self):
        if self.currentindex < self.numberofpages:
            self.currentindex += 1
            self.stackedWidget.setCurrentIndex(self.currentindex)

    def previous(self):
        if self.currentindex > 0:
            self.currentindex -= 1
            self.stackedWidget.setCurrentIndex(self.currentindex)


class guessnumbers_GUI(QDialog, Ui_guess):
    def __init__(self, root):
        QDialog.__init__(self, root)
        Ui_guess.__init__(self)
        self.setupUi(self)
        self.root = root
        self.listbox = self.root.listbox
        self.addlog = self.root.addlog
        self.digit = 4
        self.numberoftries = 10
        self.numberoftriesleft = self.numberoftries
        self.number = 0
        self.numberstring = ''
        self.myguess = ''
        self.As = 0
        self.Bs = 0
        self.exclude = []
        self.buttonstart.clicked.connect(self.startgame)
        self.buttonenter.clicked.connect(self.enternumber)
        self.shortcut = QShortcut(QtGui.QKeySequence(Qt.Key_Enter), self)
        self.shortcut.activated.connect(self.enternumber)

    def startgame(self):
        self.digit = int(self.entry_1.text())
        self.numberoftries = int(self.entry_2.text())
        self.numberoftriesleft = self.numberoftries
        self.randomnumber()
        self.addlog('Game begins!', 'orange')
        self.countdown.display(self.numberoftriesleft)
        self.buttonstart.setText("Restart")

    def enternumber(self):
        self.myguess = str(self.entry_3.text())
        self.As = 0
        self.Bs = 0
        self.exclude = []
        if len(self.numberstring) == 0:
            self.startgame()

        if len(self.myguess) != self.digit:
            self.addlog('Invalid input.')
            return
        for i in range(0, self.digit):
            if self.myguess[i] == self.numberstring[i]:
                self.As += 1
        if self.As == self.digit:
            self.numberoftriesleft -= 1
            self.countdown.display(self.numberoftriesleft)
            self.addlog('Bingo! The number is {}.'.format(self.numberstring), 'red')
            self.buttonstart.setText("Start")
            self.entry_3.setText("")
            self.numberstring = ''
            return
        for i in range(0, self.digit):
            for j in range(0, self.digit):
                if j not in self.exclude:
                    if self.myguess[j] == self.numberstring[i]:
                        self.Bs += 1
                        self.exclude.append(j)
                        break
        self.Bs -= self.As
        self.addlog('{}    {}A{}B'.format(self.myguess, self.As, self.Bs))
        self.numberoftriesleft -= 1
        self.countdown.display(self.numberoftriesleft)
        if self.numberoftriesleft <= 0:
            self.addlog('Game over! The number is {}'.format(self.numberstring), 'orange')
            self.numberstring = ''
            self.buttonstart.setText("Start")
        self.entry_3.setText("")

    def randomnumber(self):
        while True:
            oknumber = 1
            self.number = randint(0, math.pow(10, self.digit) - 1)
            self.numberstring = "%0{}d".format(self.digit) % self.number
            for i in range(0, self.digit):
                for j in range(0, self.digit):
                    if j != i:
                        if self.numberstring[j] == self.numberstring[i]:
                            oknumber = 0
            if oknumber == 1:
                break


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)


class mainwindow(QMainWindow, Ui_main):
    """Main window of the Toolbox."""

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_main.__init__(self)
        self.setupUi(self)
        if colortheme == 2:
            self.setStyleSheet("background: rgba(0,0,0,100%) ")

        if _platform == "darwin":
            self.setWindowIcon(QIcon(resource_path('icon.icns')))
        else:
            self.setWindowIcon(QIcon(resource_path('icon.ico')))
        self.splitter.setSizes([800, 100])
        self.setStatusBar(self.statusbar)
        self.subwindowlist = []
        self.clipboard = QLabel()  # In order to transfer info between subwindows, create a null label as clipboard.
        self.clipboard.setParent(self)
        self.clipboard.hide()

        for i in range(0, 30):  # Set 30 subwindows max.
            sub = QMdiSubWindow()
            sub.setAttribute(Qt.WA_DeleteOnClose)  # Important for closing tabs properly.
            sub.setWindowIcon(QIcon())  # Remove the icon for each sub window.
            self.subwindowlist.append(sub)

        self.gui0 = welcome_GUI()
        self.subwindowlist[0].setWidget(self.gui0)
        self.subwindowlist[0].setWindowTitle("Welcome.")
        self.subwindowlist[0].aboutToActivate.connect(self.Normalstatus)
        self.mdi.addSubWindow(self.subwindowlist[0])
        self.subwindowlist[0].showMaximized()
        self.subwindowlist[0].show()

        self.numberofgui = 0

        self.initialmenuitems("help", 1)
        self.Load_Available_Modules()

        if _platform == "darwin":
            self.status1.setText("﻿Welcome to the Toolbox. Press ⌘+M to see document/help.")
        self.status2.setText('v{}'.format(__version__))
        self.statusbar.addWidget(self.authorLabel)

        self.statusbar.addWidget(self.progressbar)
        self.progressbar.hide()
        self.statusbar.addWidget(self.status1)
        self.statusbar.addPermanentWidget(self.status2)

        self.authorLabel.mousePressEvent = self.addguess

        self.shortcut0 = QShortcut(QtGui.QKeySequence(Qt.Key_Escape), self)
        self.shortcut0.activated.connect(self.quitfullscreen)

        # System Tray
        if _platform == "darwin":
            self.trayIcon = QSystemTrayIcon(QIcon(resource_path('icon.icns')), self)
        else:
            self.trayIcon = QSystemTrayIcon(QIcon(resource_path('icon.ico')), self)
        self.menu = QMenu()
        self.exitAction = self.menu.addAction("Exit")

        def quitmainwindow():
            self.close()

        self.exitAction.triggered.connect(quitmainwindow)
        self.trayIcon.setContextMenu(self.menu)

        if _platform != "darwin":
            def __icon_activated(reason):
                if reason == QSystemTrayIcon.DoubleClick:
                    self.showFullScreen()  # Currently not working.
                    self.show()

            self.trayIcon.activated.connect(__icon_activated)

        self.trayIcon.show()

    def initialmenuitems(self, item, available):
        if available == 1:
            try:
                getattr(self, "open{}".format(item)).triggered.connect(getattr(self, "add{}".format(item)))
            except AttributeError:
                getattr(self, "open{}".format(item)).setDisabled(True)
        else:
            getattr(self, "open{}".format(item)).setDisabled(True)

    def Load_Available_Modules(self):

        """Import all available modules into the mainwindow."""

        global __thisversion__, __version__  # allows access to global variable in this function

        keyboard_shortcut_index = 1
        first_non_module_action = self.menuAdd.actions()[0]  # We will put the new menu actions before this one
        for module_name, window_type, module_title in modules:

            try:
                module = importlib.import_module(module_name)  # For example: import MCT_calculator_class_v3
                __thisversion__ += float(module.__version__)  # Toolbox version is the sum of its components
                # module_available.append( True )

                module_window = getattr(module, window_type)

                openAct = QAction(module_title, self)
                if keyboard_shortcut_index <= 9:
                    openAct.setShortcuts(QKeySequence("Ctrl+" + str(keyboard_shortcut_index)))
                else:
                    openAct.setShortcuts(QKeySequence("Alt+Ctrl+" + str(keyboard_shortcut_index-9)))
                # openAct.setStatusTip( "Tool tip message" )
                openAct.triggered.connect(lambda ignore, module_version=module.__version__, module_window=module_window,
                                                 module_title=module_title: self.addModule(module_version,
                                                                                           module_window,
                                                                                           module_title))
                self.menuAdd.insertAction(first_non_module_action,
                                          openAct)  # insert openAct before first_non_module_action

            except Exception as e:
                # module_available.append( False )
                print(e)
                blank_action = QAction(module_title, self)
                blank_action.setDisabled(True)
                self.menuAdd.insertAction(first_non_module_action,
                                          blank_action)  # insert blank_action before first_non_module_action

            keyboard_shortcut_index += 1

        __version__ = "3.09" + "/" + "{:.2f}".format(__thisversion__)

    def addhelp(self):
        self.numberofgui += 1
        gui = help_GUI()
        self.subwindowlist[self.numberofgui].setWidget(gui)
        self.subwindowlist[self.numberofgui].setWindowTitle("Document")
        self.subwindowlist[self.numberofgui].aboutToActivate.connect(self.Normalstatus)
        self.mdi.addSubWindow(self.subwindowlist[self.numberofgui])
        self.subwindowlist[self.numberofgui].showMaximized()
        self.subwindowlist[self.numberofgui].show()

    def addguess(self, event):
        window = guessnumbers_GUI(self)
        window.show()
        window.exec_()

    def addModule(self, module_version, window_type, module_title):
        self.numberofgui += 1
        gui = window_type(self.subwindowlist[self.numberofgui], self)
        self.setupsubwindow(gui, module_title, module_version)

    def setupsubwindow(self, gui, name, version):
        self.subwindowlist[self.numberofgui].setWidget(gui)
        self.subwindowlist[self.numberofgui].setWindowTitle("{} v{}".format(name, version))

        if name == "FTIR Fitting Tool":
            self.subwindowlist[self.numberofgui].aboutToActivate.connect(self.FTIRstatus)
        else:
            self.subwindowlist[self.numberofgui].aboutToActivate.connect(self.Normalstatus)

        self.mdi.addSubWindow(self.subwindowlist[self.numberofgui])
        self.subwindowlist[self.numberofgui].showMaximized()
        self.subwindowlist[self.numberofgui].show()

        self.addinitiallog(name)

    def Normalstatus(self):
        if _platform == "darwin":
            self.status1.setText("﻿Welcome to the Toolbox. Press ⌘+M to see document/help.")
        else:
            self.status1.setText("﻿Welcome to the Toolbox. Press Ctrl+M to see document/help.")

    def FTIRstatus(self):
        if _platform == "darwin":
            self.status1.setText("Welcome to FTIR Fitting Tool. Press ⌘+P for help.")
        else:
            self.status1.setText("Welcome to FTIR Fitting Tool. Press Ctrl+P for help.")

    def addinitiallog(self, name):
        self.addlog('-' * 160, "blue")
        self.addlog('Welcome to {}.'.format(name), "blue")
        self.addlog("This is the log file.", "blue")
        self.addlog('-' * 160, "blue")

    def quitfullscreen(self):
        if self.isFullScreen():
            self.showNormal()

    def addlog_with_button(self, string, buttontext, fg="default", bg="default"):

        """Add a line to the log file with some description and a button.
        This function will return the button so it can be click.connect to functions."""

        item = QListWidgetItem()
        # Create widget
        widget = QWidget()
        widgetText = QLabel("<font size=3>"+string+"</font>")
        if fg is not "default":
            widgetText.setForeground(QColor(fg))
        if bg is not "default":
            widgetText.setBackground(QColor(bg))
        widgetText.setFixedHeight(17)
        widgetText.setWindowFlags(Qt.FramelessWindowHint)
        widgetText.setAttribute(Qt.WA_TranslucentBackground)
        widgetButton = QPushButton(buttontext)
        widgetButton.setFixedHeight(17)
        widgetButton.setStyleSheet("padding: 1px;")
        widgetLayout = QHBoxLayout()
        widgetLayout.setContentsMargins(5, 0, 5, 0)
        widgetLayout.addWidget(widgetText)
        widgetLayout.addWidget(widgetButton)
        widgetLayout.addStretch()

        widgetLayout.setSizeConstraint(QLayout.SetFixedSize)
        widget.setLayout(widgetLayout)
        widget.setFixedHeight(17)
        widget.setWindowFlags(Qt.FramelessWindowHint)
        widget.setAttribute(Qt.WA_TranslucentBackground)
        item.setSizeHint(widget.sizeHint())

        # Add widget to QListWidget
        self.listbox.addItem(item)
        self.listbox.setItemWidget(item, widget)
        self.listbox.scrollToItem(item)
        self.listbox.show()

        return widgetButton

    def addlog(self, string, fg="default", bg="default"):

        """Add a simple text log to the log frame."""

        item = QListWidgetItem(string)
        if fg is not "default":
            item.setForeground(QColor(fg))
        if bg is not "default":
            item.setBackground(QColor(bg))
        self.listbox.addItem(item)
        self.listbox.scrollToItem(item)
        self.listbox.show()

        return item


def main():
    app = QApplication(sys.argv)
    splash_pix = QPixmap(resource_path('bg.png'))
    logo = QPixmap(resource_path('MPL_UIC.png'))
    logo = logo.scaled(150, 46, transformMode=Qt.SmoothTransformation)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())

    vbox = QVBoxLayout()
    vbox.setContentsMargins(15, 190, 15, 50)
    font = QFont("Helvetica", 20)
    lb00 = QLabel("Toolbox v{}".format(__version__[0:4]))
    lb00.setAlignment(Qt.AlignCenter)
    lb00.setFont(font)
    lb01 = QLabel("The only one you need.")
    lb01.setAlignment(Qt.AlignCenter)
    lb02 = QLabel()
    lb02.setAlignment(Qt.AlignCenter)
    lb02.setPixmap(logo)
    vbox.addWidget(lb00)
    vbox.addWidget(lb01)
    vbox.addWidget(lb02)
    splash.setLayout(vbox)

    splash.show()
    app.processEvents()

    # Simulate something that takes time
    #time.sleep(2) #why was this here?

    window = mainwindow()
    window.setWindowTitle("Toolbox v{}".format(__version__))
    if fullscreenonstart == 1:
        window.showFullScreen()
    else:
        window.showMaximized()
    if colortheme + darkthemeavailable == 2 or colortheme + darkthemeavailable == 3:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window.show()
    splash.finish(window)

    # Override excepthook to prevent program crashing and create feekback log.

    def excepthook(excType, excValue, tracebackobj):
        """
        Global function to catch unhandled exceptions in main thread ONLY.

        @param excType exception type
        @param excValue exception value
        @param tracebackobj traceback object
        """
        separator = '-' * 80
        logFile = time.strftime("%m_%d_%Y_%H_%M_%S") + ".log"
        notice = \
            """An unhandled exception occurred. \n""" \
            """Please report the problem via email to <%s>.\n""" \
            """A log has been written to "%s".\n\nError information:\n""" % \
            (__emailaddress__, logFile)
        timeString = time.strftime("%m/%d/%Y, %H:%M:%S")

        tbinfofile = io.StringIO()
        traceback.print_tb(tracebackobj, None, tbinfofile)
        tbinfofile.seek(0)
        tbinfo = tbinfofile.read()
        errmsg = '%s: \n%s' % (str(excType), str(excValue))
        sections = [separator, timeString, separator, errmsg, separator, tbinfo]
        msg = '\n'.join(sections)
        try:
            f = open(logFile, "w")
            f.write(msg)
            f.write("Version: {}".format(__version__))
            f.close()
        except IOError:
            pass
        errorbox = QMessageBox()
        errorbox.setText(str(notice) + str(msg) + "Version: " + __version__)
        errorbox.exec_()

    sys.excepthook = excepthook

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
