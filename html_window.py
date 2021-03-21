from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys


class HtmlWindow(QWidget):
    def __init__(self, url, icon="image/app.png", title="Awesome Note", parent=None):
        super(HtmlWindow, self).__init__(parent)
        self.setWindowTitle(title)
        self.setObjectName("html_window")
        self.setStyleSheet("#html_window{background-color:white}")
        self.setWindowIcon(QIcon(icon))
        self.browser = QWebEngineView()
        # 指定打开界面的 URL
        # self.browser.setUrl(QUrl(url))
        self.browser.load(QUrl(url))
        # 添加浏览器到窗口中
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.browser)
        self.setLayout(self.v_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = HtmlWindow(r'C:/Users/82140/Desktop/Awesome Note/summary/Markdown.html')
    win.show()
    sys.exit(app.exec_())

