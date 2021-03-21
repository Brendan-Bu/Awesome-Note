import sys
import os
import configparser as parser
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from about_window import About

QTextCodec.setCodecForLocale(QTextCodec.codecForName("UTF-8"))
CONFIG_FILE_PATH = "notepad.ini"
image_path = "image/notepad/"
icon_list = {
    "check": image_path+'check',
    "check_no": image_path+'check_no',
    "new": image_path+'new',
    "open": image_path+'open',
    "save": image_path+'save',
    "save_as": image_path+'save_as',
    "print": image_path+'print',
    "exit": image_path+'exit',
    "undo": image_path+'undo',
    "cut": image_path+'cut',
    "copy": image_path+'copy',
    "paste": image_path+'paste',
    "clear": image_path+'clear',
    "delete": image_path+'delete',
    "search": image_path+'search',
    "replace": image_path+'replace',
    "select_all": image_path+'select_all',
    "font": image_path+'font',
    "reset": image_path+'reset',
    "about": image_path+'about',
    "tool": image_path+'tool',
}


class Notepad(QMainWindow):
    def __init__(self, title="untitled"):
        self.read_config_file()
        """全局变量"""
        # 剪切板
        self.clipboard = QApplication.clipboard()
        # 上一次搜索内容
        self.last_search_text = ""
        # 上一次替换内容
        self.last_replace_search_text = ""
        # 是否重置
        self.reset = False
        # 配置文件
        self.config = parser.ConfigParser()
        self.config.read(CONFIG_FILE_PATH)

        QMainWindow.__init__(self)

        self.title = title
        self.init_ui()

    # 读取配置文件
    def read_config_file(self):
        if not os.path.exists(CONFIG_FILE_PATH):
            f = open(CONFIG_FILE_PATH, mode="w", encoding="UTF-8")
            f.close()

    # 窗口初始化
    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon("image/app.png"))
        self.init_edit()
        self.create_action()
        self.create_statusbar()
        self.create_menubar()
        self.create_toolbar()
        self.reading_settings()
        self.text.document().contentsChanged.connect(self.document_modified)
        self.set_current_file('')

    # 编辑区初始化
    def init_edit(self):
        self.text = QPlainTextEdit()
        self.text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.custom_context_menu)
        self.setCentralWidget(self.text)

    # 右键菜单栏
    def custom_context_menu(self):
        menu = QMenu(self)
        menu.addAction(self.undo_action)
        menu.addSeparator()
        menu.addAction(self.cut_action)
        menu.addAction(self.copy_action)
        menu.addAction(self.paste_action)
        menu.addAction(self.delete_action)
        menu.addSeparator()
        menu.addAction(self.select_all_action)
        menu.exec_(QCursor.pos())

        return menu

    # 创建状态栏
    def create_statusbar(self):
        self.statusBar().showMessage("准备就绪")

    # 创建菜单栏
    def create_menubar(self):
        file = self.menuBar().addMenu("文件")
        file.addAction(self.new_action)
        file.addAction(self.open_action)
        file.addAction(self.save_action)
        file.addSeparator()
        file.addAction(self.print_action)
        file.addSeparator()
        file.addAction(self.exit_action)

        edit = self.menuBar().addMenu("编辑")
        edit.addAction(self.undo_action)
        edit.addSeparator()
        edit.addAction(self.cut_action)
        edit.addAction(self.copy_action)
        edit.addAction(self.paste_action)
        edit.addAction(self.clear_action)
        edit.addAction(self.delete_action)
        edit.addSeparator()
        edit.addAction(self.find_action)
        edit.addAction(self.find_next_action)
        edit.addAction(self.replace_action)
        edit.addSeparator()
        edit.addAction(self.select_all_action)

        style = self.menuBar().addMenu("格式")
        style.addAction(self.auto_wrap_action)
        style.addAction(self.font_action)

        view = self.menuBar().addMenu("查看")
        view.addAction(self.toolbar_action)
        view.addAction(self.reset_action)

        help = self.menuBar().addMenu("帮助")
        help.addAction(self.about_action)

    # 创建工具栏
    def create_toolbar(self):
        self.toolbar = self.addToolBar("")
        self.toolbar.addAction(self.new_action)
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.save_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.cut_action)
        self.toolbar.addAction(self.copy_action)
        self.toolbar.addAction(self.paste_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.clear_action)

    # 读取设置
    def reading_settings(self):
        # 宽度 高度
        width = 1080
        height = 720
        size = QSize(int(width), int(height))
        self.resize(size)

        # 屏幕位置
        screen = QDesktopWidget().screenGeometry()
        screen_size = self.geometry()
        pos_x = (screen.width() - screen_size.width()) / 2
        pos_y = (screen.height() - screen_size.height()) / 2
        self.move(pos_x, pos_y)

        # 是否显示工具栏
        toolbar = get_config(self.config, "Display", "toolbar", "True")

        # 是否自动换行
        wrap_mode = get_config(self.config, "TextEdit", "wrapmode", "True")

        # 字体
        font_family = get_config(self.config, "TextEdit", "font", "Consolas")
        font_size = get_config(self.config, "TextEdit", "size", 14)
        fonts = QFont(font_family, int(font_size))

        if "True" == wrap_mode:
            self.auto_wrap_action.setIcon(QIcon(icon_list['check']))
            wrap_mode = QPlainTextEdit.WidgetWidth
        else:
            self.auto_wrap_action.setIcon(QIcon(icon_list['check_no']))
            wrap_mode = QPlainTextEdit.NoWrap

        if "True" == toolbar:
            self.toolbar.show()
            self.toolbar_action.setIcon(QIcon(icon_list['check']))
        else:
            self.toolbar.hide()
            self.toolbar_action.setIcon(QIcon(icon_list['check_no']))

        self.text.setLineWrapMode(wrap_mode)
        self.text.setFont(fonts)

    # 重置设置
    def reset_settings(self):
        # 宽度、高度
        write_config(self.config, "Display", "width", "1000")
        write_config(self.config, "Display", "height", "600")
        # 位置
        screen = QDesktopWidget().screenGeometry()
        write_config(self.config, "Display", "x", str((screen.width() - 1000) // 2))
        write_config(self.config, "Display", "y", str((screen.height() - 600) // 2))
        # 工具栏
        write_config(self.config, "Display", "toolbar", "True")
        # 自动换行
        write_config(self.config, "TextEdit", "wrapmode", "True")
        # 字体
        write_config(self.config, "TextEdit", "font", "Consolas")
        # 大小
        write_config(self.config, "TextEdit", "size", "14")

        # 回写
        self.config.write(open(CONFIG_FILE_PATH, "w"))

        QMessageBox.information(self, "Awesome Note", "重置成功，请重启软件！")
        self.reset = True
        self.close()

    # 写入设置
    def write_settings(self):
        # 宽度、高度
        write_config(self.config, "Display", "height", str(self.size().height()))
        write_config(self.config, "Display", "width", str(self.size().width()))
        # 位置
        write_config(self.config, "Display", "x", str(self.pos().x()))
        write_config(self.config, "Display", "y", str(self.pos().y()))
        # 工具栏
        write_config(self.config, "Display", "toolbar", str(not self.toolbar.isHidden()))
        # 自动换行
        write_config(self.config, "TextEdit", "wrapmode",
                    str(self.text.lineWrapMode() == QPlainTextEdit.WidgetWidth))
        # 字体
        write_config(self.config, "TextEdit", "font", self.text.font().family())
        # 大小
        write_config(self.config, "TextEdit", "size", str(self.text.font().pointSize()))

        # 回写
        self.config.write(open(CONFIG_FILE_PATH, "w"))

    def strip_name(self, full_file_name):
        return QFileInfo(full_file_name).fileName()

    # 设置当前文件
    def set_current_file(self, filename):
        self.current_file = filename
        self.text.document().setModified(False)
        self.setWindowModified(False)

        if self.current_file:
            show_name = self.strip_name(self.current_file)
        else:
            show_name = 'untitled.txt'

        self.setWindowTitle("%s[*] - Awesome Note" % show_name)

    def document_modified(self):
        self.setWindowModified(self.text.document().isModified())
        if "" != self.text.toPlainText():
            self.find_action.setEnabled(True)
            self.find_next_action.setEnabled(True)
        else:
            self.find_action.setEnabled(False)
            self.find_next_action.setEnabled(False)

    # 确认是否保存
    def may_save(self):
        if self.text.document().isModified():
            ret = self.tip()

            if 0 == ret:
                return self.save()
            if 2 == ret:
                return False
        return True

    # 保存
    def save(self):
        if self.current_file:
            return self.save_file(self.current_file)
        else:
            return self.save_as()

    # 另存为
    def save_as(self):
        filename, _ = QFileDialog.getSaveFileName(self)
        if filename:
            return self.save_file(filename)
        return False

    # 保存文件
    def save_file(self, filename):
        file = QFile(filename)
        # 打开失败
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Awesome Note", "文件%s不能被写入:\n%s." % (filename, file.errorString()))
            return False

        out_file = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out_file << self.text.toPlainText()
        QApplication.restoreOverrideCursor()

        self.set_current_file(filename)
        print(filename)
        self.statusBar().showMessage("写入文件成功", 2000)
        return True

    # 创建新文件
    def new_file(self):
        if self.may_save():
            self.text.clear()

    # 打印文件
    def print_text(self):
        document = self.text.document()
        printer = QPrinter()

        dialog = QPrintDialog(printer, self)
        if dialog.exec_() != QDialog.Accepted:
            return

        document.print_(printer)

        self.statusBar().showMessage("打印成功", 2000)

    # 打开文件
    def open_file_event(self):
        # 读取失败
        if self.may_save():
            filename, _ = QFileDialog.getOpenFileName(self)
            file = QFile(filename)
            if not file.open(QFile.ReadOnly | QFile.Text):
                QMessageBox.warning(self, "Awesome Note", "文件%s不能被读取:\n%s." % (filename, file.errorString()))
                return

        in_file = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.text.setPlainText(in_file.readAll())
        QApplication.restoreOverrideCursor()

        self.set_current_file(filename)
        self.statusBar().showMessage("文件读取成功", 2000)

    # 外部打开文件
    def open_out_file(self, file_name, file_path):
        file = QFile(file_path)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Awesome Note", "文件%s不能被读取:\n%s." % (file_name, file.errorString()))
            return

        in_file = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.text.setPlainText(in_file.readAll())
        QApplication.restoreOverrideCursor()

        self.set_current_file(file_path)
        self.statusBar().showMessage("文件读取成功", 2000)

    # 关闭事件
    def closeEvent(self, event):
        if not self.may_save():
            event.ignore()
        else:
            if not self.reset:
                self.write_settings()
            event.accept()

    # 清空剪切板
    def clear_clipboard(self):
        self.clipboard.clear()
        self.paste_action.setEnabled(False)
        self.clear_action.setEnabled(False)

    # 删除文本
    def delete(self):
        cursor = self.text.textCursor()
        if not cursor.isNull():
            cursor.removeSelectedText()
            self.statusBar().showMessage("删除成功", 2000)

    # 查找文本
    def find_text(self):
        self.display_find_dialog()

    # 查找下一处文本
    def find_next_text(self):
        if "" == self.last_search_text:
            self.display_find_dialog()
        else:
            self.search_text()

    # 查询提示框
    def display_find_dialog(self):
        self.find_dialog = QDialog(self)

        label = QLabel("查找内容:")
        self.line_edit = QLineEdit()
        self.line_edit.setText(self.last_search_text)
        label.setBuddy(self.line_edit)

        self.find_button = QPushButton("查找下一个")
        self.find_button.setDefault(True)
        self.find_button.clicked.connect(self.search_text)

        button_box = QDialogButtonBox(Qt.Vertical)
        button_box.addButton(self.find_button, QDialogButtonBox.ActionRole)

        top_left_layout = QHBoxLayout()
        top_left_layout.addWidget(label)
        top_left_layout.addWidget(self.line_edit)

        left_layout = QVBoxLayout()
        left_layout.addLayout(top_left_layout)

        main_layout = QGridLayout()
        main_layout.setSizeConstraint(QLayout.SetFixedSize)
        main_layout.addLayout(left_layout, 0, 0)
        main_layout.addWidget(button_box, 0, 1)
        main_layout.setRowStretch(2, 1)
        self.find_dialog.setLayout(main_layout)

        self.find_dialog.setWindowTitle("查找")
        self.find_dialog.show()
        
    def search_text(self):
        # 获取光标位置
        # 从光标位置处开始搜索
        cursor = self.text.textCursor()
        find_index = cursor.anchor()
        text = self.line_edit.text()
        content = self.text.toPlainText()
        length = len(text)

        self.last_search_text = text
        index = content.find(text, find_index)

        if -1 == index:
            error_dialog = QMessageBox(self)
            error_dialog.addButton("取消", QMessageBox.ActionRole)

            error_dialog.setWindowTitle("Awesome Note")
            error_dialog.setText("找不到\"%s\"." % text)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.exec_()
        else:
            start = index

            cursor = self.text.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, start + length)
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, length)
            cursor.selectedText()
            self.text.setTextCursor(cursor)

    # 替换
    def replace_text(self):
        replace_dialog = QDialog(self)

        replace_label = QLabel("替换内容:")
        self.replace_text = QLineEdit()
        self.replace_text.setText(self.last_replace_search_text)
        replace_label.setBuddy(self.replace_text)

        replace_to_label = QLabel("替换为  :")
        self.replace_to_text = QLineEdit()
        replace_to_label.setBuddy(self.replace_to_text)

        find_next_button = QPushButton("查找下一个")
        find_next_button.setDefault(True)
        replace_button = QPushButton("替换")
        replace_all_button = QPushButton("全部替换")
        cancel_all_button = QPushButton("取消")

        # 按钮事件绑定
        find_next_button.clicked.connect(lambda: self.replace_or_search(False))
        cancel_all_button.clicked.connect(replace_dialog.close)
        replace_button.clicked.connect(lambda: self.replace_or_search(True))
        replace_all_button.clicked.connect(self.replace_all_text)

        button_box = QDialogButtonBox(Qt.Vertical)
        button_box.addButton(find_next_button, QDialogButtonBox.ActionRole)
        button_box.addButton(replace_button, QDialogButtonBox.ActionRole)
        button_box.addButton(replace_all_button, QDialogButtonBox.ActionRole)
        button_box.addButton(cancel_all_button, QDialogButtonBox.ActionRole)

        top_left_layout1 = QHBoxLayout()

        top_left_layout1.addWidget(replace_label)
        top_left_layout1.addWidget(self.replace_text)

        top_left_layout2 = QHBoxLayout()
        top_left_layout2.addWidget(replace_to_label)
        top_left_layout2.addWidget(self.replace_to_text)

        left_layout = QVBoxLayout()
        left_layout.addLayout(top_left_layout1)
        left_layout.addLayout(top_left_layout2)

        main_layout = QGridLayout()
        main_layout.setSizeConstraint(QLayout.SetFixedSize)
        main_layout.addLayout(left_layout, 0, 0)
        main_layout.addWidget(button_box, 0, 1)
        main_layout.setRowStretch(2, 1)
        replace_dialog.setLayout(main_layout)

        replace_dialog.setWindowTitle("替换")
        replace_dialog.show()

    def replace_or_search(self, is_replaced):
        # 获取光标位置
        # 从光标位置处开始搜索
        cursor = self.text.textCursor()
        find_index = cursor.anchor()
        text = self.replace_text.text()
        content = self.text.toPlainText()
        length = len(text)
        index = content.find(text, find_index)
        self.last_replace_search_text = text
        if -1 == index:
            error_dialog = QMessageBox(self)
            error_dialog.addButton("取消", QMessageBox.ActionRole)

            error_dialog.setWindowTitle("Awesome Note")
            error_dialog.setText("找不到\"%s\"." % text)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.exec_()
        else:
            start = index
            if is_replaced:
                to_replace_text = self.replace_to_text.text()
                prefix = content[0:start]
                postfix = content[start + length:]
                new_text = prefix + to_replace_text + postfix
                self.text.setPlainText(new_text)
                length = len(to_replace_text)
                self.text.document().setModified(True)

            cursor = self.text.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, start + length)
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, length)
            cursor.selectedText()
            self.text.setTextCursor(cursor)

    # 替换所有
    def replace_all_text(self):
        text = self.replace_text.text()
        content = self.text.toPlainText()
        to_replace_text = self.replace_to_text.text()
        content = content.replace(text, to_replace_text)
        self.text.setPlainText(content)
        self.text.document().setModified(True)
    
    # 设置自动换行
    def set_wrap(self):
        mode = self.text.lineWrapMode()
        if 1 == mode:
            # 自动换行
            self.text.setLineWrapMode(QPlainTextEdit.NoWrap)
            self.auto_wrap_action.setIcon(QIcon(icon_list['check_no']))
        else:
            # 不自动换行
            self.text.setLineWrapMode(QPlainTextEdit.WidgetWidth)
            self.auto_wrap_action.setIcon(QIcon(icon_list['check']))

    # 设置字体
    def set_font(self):
        font, ok = QFontDialog.getFont(QFont(self.text.toPlainText()), self)
        if ok:
            self.text.setFont(font)

    # 工具栏状态
    def toggle_toolbar(self):
        if self.toolbar.isHidden():
            self.toolbar.show()
            self.toolbar_action.setIcon(QIcon(icon_list['check']))
        else:
            self.toolbar.hide()
            self.toolbar_action.setIcon(QIcon(icon_list['check_no']))

    # 重置设置
    def reset_settings(self):
        # 宽度、高度
        write_config(self.config, "Display", "width", "1000")
        write_config(self.config, "Display", "height", "600")
        # 位置
        screen = QDesktopWidget().screenGeometry()
        write_config(self.config, "Display", "x", str((screen.width() - 1000) // 2))
        write_config(self.config, "Display", "y", str((screen.height() - 600) // 2))
        # 工具栏
        write_config(self.config, "Display", "toolbar", "True")
        # 自动换行
        write_config(self.config, "TextEdit", "wrapmode", "True")
        # 字体
        write_config(self.config, "TextEdit", "font", "Consolas")
        # 大小
        write_config(self.config, "TextEdit", "size", "14")

        # 回写
        self.config.write(open(CONFIG_FILE_PATH, "w"))

        QMessageBox.information(self, "Awesome Note", "重置成功，请重启软件！")
        self.reset = True
        self.close()

    # “关于”界面
    def about(self):
        self.about_window = About()
        self.about_window.show()

    # 创建动作
    def create_action(self):
        self.new_action = QAction(QIcon(icon_list['new']), '&新建', self, shortcut=QKeySequence.New,
                                  statusTip='创建文件', triggered=self.new_file)
        self.open_action = QAction(QIcon(icon_list['open']), '&打开...', self, shortcut=QKeySequence.Open,
                                   statusTip='打开文件', triggered=self.open_file_event)
        self.save_action = QAction(QIcon(icon_list['save']), '&保存', self, shortcut=QKeySequence.Save,
                                   statusTip='保存文件', triggered=self.save)
        self.save_as_action = QAction(QIcon(icon_list['save_as']), '另存为...', self, shortcut=QKeySequence.SaveAs,
                                      statusTip="另存为文件", triggered=self.save_as)
        self.print_action = QAction(QIcon(icon_list['print']), '打印', self, shortcut=QKeySequence.Print,
                                    statusTip="打印文件", triggered=self.print_text)
        self.exit_action = QAction(QIcon(icon_list['exit']), '退出', self, shortcut="Ctrl+Q", statusTip="退出程序",
                                   triggered=self.close)
        self.undo_action = QAction(QIcon(icon_list['undo']), '撤销', self, shortcut=QKeySequence.Undo,
                                   statusTip="撤销编辑", triggered=self.text.undo)
        self.cut_action = QAction(QIcon(icon_list['cut']), '剪切', self, shortcut=QKeySequence.Cut,
                                  statusTip="剪切选中的文本", triggered=self.text.cut)
        self.copy_action = QAction(QIcon(icon_list['copy']), '复制', self, shortcut=QKeySequence.Copy,
                                   statusTip="复制选中的文本", triggered=self.text.copy)
        self.paste_action = QAction(QIcon(icon_list['paste']), '粘贴', self, shortcut=QKeySequence.Paste,
                                    statusTip="粘贴剪切板的文本", triggered=self.text.paste)
        self.clear_action = QAction(QIcon(icon_list['clear']), '清空剪切版', self, statusTip="清空剪辑版",
                                    triggered=self.clear_clipboard)
        self.delete_action = QAction(QIcon(icon_list['delete']), '删除', self, statusTip="删除选中的文本",
                                     triggered=self.delete)
        self.find_action = QAction(QIcon(icon_list['search']), '查找', self, shortcut=QKeySequence.Find,
                                   statusTip="查找文本", triggered=self.find_text)
        self.find_next_action = QAction(QIcon(icon_list['search']), '查找下一个', self, shortcut=QKeySequence.FindNext,
                                        statusTip="查找文本", triggered=self.find_next_text)
        self.replace_action = QAction(QIcon(icon_list['replace']), '替换', self, statusTip="替换文本",
                                      triggered=self.replace_text, shortcut=QKeySequence.Replace)
        self.select_all_action = QAction(QIcon(icon_list['select_all']), '全选', self, shortcut=QKeySequence.SelectAll,
                                         statusTip="全选", triggered=self.text.selectAll)
        self.auto_wrap_action = QAction(QIcon(icon_list['check']), '自动换行', self, statusTip="设置自动换行",
                                        triggered=self.set_wrap)
        self.font_action = QAction(QIcon(icon_list['font']), '字体', self, statusTip="打印文件", triggered=self.set_font)
        self.toolbar_action = QAction(QIcon(icon_list['check']), '工具栏', self, statusTip="工具栏",
                                      triggered=self.toggle_toolbar)
        self.reset_action = QAction(QIcon(icon_list['reset']), '重置', self, statusTip="重置所有属性",
                                    triggered=self.reset_settings)
        self.about_action = QAction(QIcon(icon_list['about']), '关于', self, triggered=self.about)

        self.undo_action.setEnabled(False)
        self.cut_action.setEnabled(False)
        self.copy_action.setEnabled(False)
        self.delete_action.setEnabled(False)
        if "" == self.clipboard.text():
            self.paste_action.setEnabled(False)
            self.clear_action.setEnabled(False)
        if "" == self.text.toPlainText():
            self.find_action.setEnabled(False)
            self.find_next_action.setEnabled(False)

        self.text.undoAvailable.connect(self.undo_action.setEnabled)
        self.text.copyAvailable.connect(self.cut_action.setEnabled)
        self.text.copyAvailable.connect(self.copy_action.setEnabled)
        self.text.copyAvailable.connect(self.delete_action.setEnabled)

        self.clipboard.dataChanged.connect(self.enabled_some_action_by_clipboard)

    def enabled_some_action_by_clipboard(self):
        if "" != self.clipboard.text():
            self.paste_action.setEnabled(True)
            self.clear_action.setEnabled(True)

    def tip(self, content="文件已被修改，是否保存？"):
        alert_box = QMessageBox(self)
        save_button = alert_box.addButton("保存", QMessageBox.ActionRole)
        un_save_button = alert_box.addButton("不保存", QMessageBox.ActionRole)
        cancel_button = alert_box.addButton("取消", QMessageBox.ActionRole)

        alert_box.setWindowTitle(self.title)
        alert_box.setText(content)
        alert_box.exec_()
        click_event = alert_box.clickedButton()

        if save_button == click_event:
            return 0
        elif un_save_button == click_event:
            return 1
        elif cancel_button == click_event:
            return 2
        else:
            return -1


# 读取配置文件
def get_config(config, selection, option, default=""):
    if config is None:
        return default
    else:
        try:
            return config.get(selection, option)
        except:
            return default


# 写入配置
def write_config(config, selection, option, value):
    if not config.has_section(selection):
        config.add_section(selection)

    config.set(selection, option, value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad = Notepad()
    notepad.show()
    app.exec_()
