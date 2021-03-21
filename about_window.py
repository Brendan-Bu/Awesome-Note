from PyQt5.Qt import *
from html_window import HtmlWindow
import os


class About(QWidget):
    def __init__(self, parent=None):
        super(About, self).__init__(parent)

        self.setWindowTitle('About')
        self.setObjectName("About")
        self.setWindowIcon(QIcon('image/app.png'))
        self.resize(400, 300)
        self.setStyleSheet("#About{background-color:white}")
        self.whole_v_layout = QVBoxLayout()

        self.information_bar = QWidget()
        self.information_bar_v_layout = QVBoxLayout(self.information_bar)

        self.app_name = QLabel(self.information_bar)
        self.app_name.setText("<p style='font-family:Trebuchet MS;font-size:15px'>"
                              "<img src='image/about/app.png' align='top' width='25' height='25' />"
                              " 软件名称:  Awesome Note</p>")
        self.information_bar_v_layout.addWidget(self.app_name)

        self.app_version = QLabel(self.information_bar)
        self.app_version.setText("<p style='font-family:Trebuchet MS;font-size:15px'>"
                                 "<img src='image/about/version.png' align='top' width='25' height='25' />"
                                 " 软件版本: 1.0.8</p>")
        self.information_bar_v_layout.addWidget(self.app_version)

        self.developer_name = QLabel(self.information_bar)
        self.developer_name.setText("<p style='font-family:Trebuchet MS;font-size:15px'>"
                                    "<img src='image/about/developer.png' align='top' width='25' height='25' />"
                                    " 开发人员: </p>"
                                    "<p>&nbsp;&nbsp;"
                                    "<img src='image/about/1.png' align='top' width='25' height='25' />李志豪&nbsp;"
                                    "<img src='image/about/2.png' align='top' width='25' height='25' />伍文征</p>"
                                    "<p>&nbsp;&nbsp;"
                                    "<img src='image/about/3.png' align='top' width='25' height='25' />卜贤达&nbsp;"
                                    "<img src='image/about/4.png' align='top' width='25' height='25' />谢玮勋</p>")
        self.information_bar_v_layout.addWidget(self.developer_name)

        self.button_box = QWidget()
        self.button_box_h_layout = QHBoxLayout(self.button_box)

        self.guide_book_button = QPushButton()
        self.guide_book_button.setObjectName("guide_button")
        self.guide_book_button.setStyleSheet("#guide_button{background-color:white}")
        self.guide_book_button.setText("用户手册")
        self.guide_book_button.setIcon(QIcon('image/about/guide.png'))
        self.guide_book_button.clicked.connect(self.open_guide_book)
        self.button_box_h_layout.addWidget(self.guide_book_button, 0, Qt.AlignLeft)

        self.md_button = QPushButton()
        self.md_button.setText("MD语法")
        self.md_button.setObjectName("md_button")
        self.md_button.setStyleSheet("#md_button{background-color:white}")
        self.md_button.setIcon(QIcon('image/about/md.png'))
        self.md_button.clicked.connect(self.open_md_book)
        self.button_box_h_layout.addWidget(self.md_button, 0, Qt.AlignRight)

        self.whole_v_layout.addWidget(self.information_bar)
        self.whole_v_layout.addWidget(self.button_box)

        self.setLayout(self.whole_v_layout)

    def open_guide_book(self):
        pass

    def open_md_book(self):
        md_book_path = "http://wow.kuapp.com/markdown/basic.html"
        self.md_book = HtmlWindow(md_book_path, title="Markdown语法", icon="image/about/md.png")
        self.md_book.show()
