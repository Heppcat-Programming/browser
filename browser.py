from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from urllib.parse import urlparse
import qdarkstyle
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2", os.path.abspath("."))

    return os.path.join(base_path, relative_path)

def urlConv(url, uri_type='netloc_only'):
    parsed_uri = urlparse(url)
    if uri_type == 'both':
        return '{uri.scheme}://{uri.netloc}{uri.path}{qry}{uri.query}'.format(uri=parsed_uri,qry="" if parsed_uri.query == "" else "?")
    elif uri_type == 'netloc_only' and parsed_uri.path == '/':
        return '{uri.netloc}{qry}{uri.query}'.format(uri=parsed_uri,qry="" if parsed_uri.query == "" else "?")
    elif uri_type == 'netloc_only':
        return '{uri.netloc}{uri.path}{qry}{uri.query}'.format(uri=parsed_uri,qry="" if parsed_uri.query == "" else "?")

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        try:
            import pyi_splash
            pyi_splash.update_text('UI Loaded ...')
            pyi_splash.close()
        except:
            pass
        self.ui=uic.loadUi(resource_path('ui.ui'), self)
        self.setWindowIcon(QtGui.QIcon(resource_path('icon.ico')))
        self.setWindowTitle("Heppcat Browsing")
        self.tb.addWidget(self.backward)
        self.backward.clicked.connect(lambda: self.tabs.currentWidget().back())
        self.tb.addWidget(self.forward)
        self.forward.clicked.connect(lambda: self.tabs.currentWidget().forward())
        self.tb.addWidget(self.reload)
        self.reload.clicked.connect(lambda: self.tabs.currentWidget().reload())
        self.tb.addWidget(self.url)
        self.url.returnPressed.connect(self.navigate_to_url)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setCornerWidget(self.newtab)
        self.newtab.clicked.connect(lambda: self.add_new_tab())
        self.add_new_tab()
        self.show()
    
    def navigate_to_url(self):
  
        # get the line edit text
        # convert it to QUrl object
        q = QtCore.QUrl(self.url.text())
  
        # if scheme is blank
        if q.scheme() == "":
            q = QtCore.QUrl(f"https://www.google.com/search?q={self.url.text().replace(' ', '+')}")
  
        # set the url
        self.tabs.currentWidget().setUrl(q)

    def add_new_tab(self, qurl = None, label ="Blank"):
  
        # if url is blank
        if qurl is None:
            # creating a google url
            qurl = QtCore.QUrl('http://www.google.com')
  
        # creating a QWebEngineView object
        browser = QWebEngineView()
  
        # setting url to browser
        browser.setUrl(qurl)
  
        # setting tab index
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
  
        # adding action to the browser when url is changed
        # update the url
        browser.urlChanged.connect(lambda qurl, browser = browser:
                                   self.update_urlbar(qurl, browser))
  
        # adding action to the browser when loading is finished
        # set the tab title
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                     self.tabs.setTabText(i, browser.page().title()))                    
        browser.iconChanged.connect(lambda _, i = i, browser = browser:
                                     self.tabs.setTabIcon(i, browser.icon()))
    def current_tab_changed(self, i):
  
        # get the curl
        qurl = self.tabs.currentWidget().url()
  
        self.update_urlbar(qurl, self.tabs.currentWidget())
  
        # update the title
    def update_urlbar(self, q, browser = None):
  
        # If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
  
            return
  
        # set text to the url bar
        self.url.setText(urlConv(q.toString()))
  
        # set cursor position
        self.url.setCursorPosition(0)
        
app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet())
window = Ui()
app.exec_()