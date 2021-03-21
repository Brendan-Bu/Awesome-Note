import sys
import time
import datetime
import os
import shutil
from PyQt5.Qt import *
from PyQt5.QtCore import *
from notepad import Notepad
from pre import *
from map import draw_map
from note import NoteFile
from documents import *
from about_window import About


image_path = "image/home/"
icon_list = {
    'app': "image/app",
    'cover': 'image/cover.jpg',
    'xmind': image_path+'map',
    'txt': image_path+'txt',
    'pdf': image_path+'pdf',
    'html': image_path+'html',
    'png': image_path+'png',
    'jpg': image_path+'jpg',
    'docx': image_path+'doc',
    'doc': image_path+'doc',
    'md': image_path+'md',
    'folder': image_path+'folder',
    'root': image_path+'root',
    'settings': image_path+'settings',
    'new': image_path+'plus',
    'note': image_path+'note',
    'search': image_path+'search',
    'about': image_path+'about',
    'other': image_path+'other',
}


class UpdateData(QThread):
    update = pyqtSignal(str)

    def run(self):
        cnt = 0
        while True:
            cnt += 1
            self.update.emit(str(cnt))
            time.sleep(1)


# 主界面（管理界面）
class Home(QWidget):
    def __init__(self, parent=None):
        super(Home, self).__init__(parent)
        self.notepad = []
        self.search_window = None
        self.manager = None
        self.update_thread = UpdateData()

        self.init_ui()

    # 初始化
    def init_ui(self):
        self.setWindowTitle('Awesome Note')
        self.setObjectName("Home")
        self.resize(1080, 720)
        self.center()
        self.setWindowIcon(QIcon(icon_list['app']))
        self.setStyleSheet("#Home{background-color:white}")
        self.create_actions()
        self.note_tree = NoteSystem('NoteSystem', root_path="NoteSystem")
        self.note_tree.span_tree()

        whole_v_layout = QVBoxLayout(self)
        # left 栏
        self.left_box = QFrame()
        self.left_box.setMinimumWidth(200)
        self.left_box.setFrameShape(QFrame.StyledPanel)
        self.left_box.setObjectName("最近编辑")
        # label
        left_v_layout = QVBoxLayout(self.left_box)
        left_label1 = QLabel(self.left_box)
        left_label1.setText("<h4><img src='image/home/recent.png' align='top' width='25' height='25' />最近编辑</h4>")
        left_label1.setAlignment(Qt.AlignTop)
        left_v_layout.addWidget(left_label1)
        # 最近编辑栏
        self.left_list = QListWidget(self.left_box)
        self.left_list.setMinimumHeight(200)
        self.add_recent_notes()
        left_v_layout.addWidget(self.left_list)
        # 搜索栏
        self.left_search = QWidget(self.left_box)
        self.left_search.setMinimumHeight(200)
        self.left_search.setObjectName("搜索")
        self.left_search_h_layout = QHBoxLayout()
        self.left_search_v_layout = QVBoxLayout()
        self.search_box_h_layout = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("输入搜索内容...")
        self.search_box_h_layout.addWidget(self.search_bar)

        search_button = QPushButton()
        search_button.setObjectName("search_button")
        search_button.setStyleSheet("#search_button{background-color:white}")
        search_button.setText("搜索")
        search_button.setIcon(QIcon(icon_list['search']))
        search_button.clicked.connect(self.on_search_click)
        self.search_box_h_layout.addWidget(search_button)

        self.search_box = QWidget()
        self.search_box.setLayout(self.search_box_h_layout)

        self.search_result = QListWidget()

        self.left_search_v_layout.addWidget(self.search_box)
        self.left_search_v_layout.addWidget(self.search_result)

        self.left_search.setLayout(self.left_search_v_layout)

        left_v_layout.addWidget(self.left_search)

        # right 笔记索引栏
        self.right_box = QFrame()
        self.right_box.setMinimumWidth(200)
        self.right_box.setFrameShape(QFrame.StyledPanel)
        self.right_box.setObjectName("笔记索引")
        right_v_layout = QVBoxLayout(self.right_box)
        right_label1 = QLabel(self.right_box)
        right_label1.setText("<h4><img src='image/home/note_tree.png' align='top' width='25' height='25' />笔记索引</h4>")
        right_label1.setAlignment(Qt.AlignTop)
        right_v_layout.addWidget(right_label1)
        self.right_tree = QTreeWidget()
        self.build_note_tree()
        right_v_layout.addWidget(self.right_tree)
        # Slitter
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.left_box)
        splitter1.addWidget(self.right_box)
        splitter1.setSizes([500, 580])
        # Bottom 底部按钮
        self.bottom_box = QWidget()
        self.bottom_box.setMaximumHeight(50)
        bottom_layout = QHBoxLayout(self.bottom_box)
        create_button = QPushButton('新建')
        create_button.setObjectName("create_button")
        create_button.setStyleSheet("#create_button{background-color:white}")
        create_button.clicked.connect(self.open_notepad)
        create_button.setIcon(QIcon(icon_list['new']))
        bottom_layout.addWidget(create_button, 0, Qt.AlignLeft)
        about_button = QPushButton('关于')
        about_button.setObjectName("about_button")
        about_button.setStyleSheet("#about_button{background-color:white}")
        about_button.clicked.connect(self.open_about_window)
        about_button.setIcon(QIcon(icon_list['about']))
        bottom_layout.addWidget(about_button, 0, Qt.AlignRight)
        # add to v_layout
        whole_v_layout.addWidget(splitter1)
        whole_v_layout.addWidget(self.bottom_box)

        self.setLayout(whole_v_layout)

    # 居中显示
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    # 添加最近编辑笔记
    def add_recent_notes(self):
        tplt = "{0:<20}{1:>20}"
        for recent_note in self.note_tree.recent_list:
            note_item = QListWidgetItem(self.left_list)
            note_item.setText(tplt.format(recent_note.file_name + '.' + recent_note.type, recent_note.time))
            note_item.setIcon(QIcon(icon_list[recent_note.type]))
            note_item.file = recent_note
        self.left_list.itemDoubleClicked.connect(self.on_recent_list_double_click)

    # 响应列表双击
    def on_recent_list_double_click(self):
        item = self.left_list.currentItem()
        if item.file.type == 'txt' or item.file.type == 'md':
            self.notepad.append(None)
            self.notepad[-1] = Notepad()
            self.notepad[-1].open_out_file(item.file.file_name, item.file.file_path)
            self.notepad[-1].show()
        else:
            os.popen(item.file.file_path)

    # 笔记管理
    def build_note_tree(self):
        self.right_tree.setColumnCount(3)
        self.right_tree.setHeaderLabels(['name', 'value', 'time'])
        self.right_tree.setColumnWidth(0, 250)

        self.note_tree_root = QTreeWidgetItem(self.right_tree)
        self.note_tree_root.setText(0, self.note_tree.tag)
        self.note_tree_root.setText(1, "System")
        self.note_tree_root.setIcon(0, QIcon(icon_list['root']))
        self.note_tree_root.tag = self.note_tree.root
        self.append_folder(self.note_tree.root, self.note_tree_root)
        self.right_tree.addTopLevelItem(self.note_tree_root)
        self.right_tree.expandItem(self.note_tree_root)
        self.right_tree.itemDoubleClicked.connect(self.on_tree_double_click)
        self.right_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.right_tree.customContextMenuRequested.connect(self.on_tree_right_click)

    # 响应树状列表右键弹出菜单
    def on_tree_right_click(self):
        pop_menu = QMenu(self)
        new_menu = QMenu(self)
        transform_menu = QMenu(self)
        new_menu.setTitle("新建")
        transform_menu.setTitle("生成")

        item = self.right_tree.currentItem()

        if not item:
            pop_menu.setEnabled(False)
            return pop_menu

        if item.text(1) == 'txt' or item.text(1) == 'md':
            self.rename_action.setEnabled(False)
            self.open_action.setEnabled(True)
            self.file_to_map_action.setEnabled(True)
            self.txt_to_html_action.setEnabled(True)
            self.html_to_word_action.setEnabled(True)
            self.delete_action.setEnabled(True)
            new_menu.setEnabled(False)
        elif item.text(1) == 'xmind':
            self.rename_action.setEnabled(False)
            self.open_action.setEnabled(True)
            transform_menu.setEnabled(False)
            self.file_to_map_action.setEnabled(False)
            self.delete_action.setEnabled(True)
            new_menu.setEnabled(False)
        elif item.text(1) == 'pdf':
            self.rename_action.setEnabled(False)
            self.open_action.setEnabled(True)
            self.file_to_map_action.setEnabled(False)
            self.delete_action.setEnabled(True)
            new_menu.setEnabled(False)
        elif item.text(1) == 'html':
            self.rename_action.setEnabled(False)
            self.open_action.setEnabled(True)
            self.file_to_map_action.setEnabled(False)
            self.txt_to_html_action.setEnabled(False)
            self.delete_action.setEnabled(True)
            new_menu.setEnabled(False)
        elif item.text(1) == 'docx' or item.text(1) == 'doc':
            self.rename_action.setEnabled(False)
            self.open_action.setEnabled(True)
            self.file_to_map_action.setEnabled(False)
            self.delete_action.setEnabled(True)
            transform_menu.setEnabled(False)
            new_menu.setEnabled(False)
        elif item.text(1) == 'Note':
            self.rename_action.setEnabled(True)
            self.open_action.setEnabled(False)
            self.file_to_map_action.setEnabled(False)
            self.delete_action.setEnabled(True)
            new_menu.setEnabled(False)
            transform_menu.setEnabled(False)
        elif item.text(1) == 'Folder':
            self.rename_action.setEnabled(True)
            self.open_action.setEnabled(False)
            transform_menu.setEnabled(False)
            self.delete_action.setEnabled(True)
            new_menu.setEnabled(True)
            self.new_folder_action.setEnabled(True)
            self.new_file_action.setEnabled(True)
        elif item.text(1) == 'System':
            self.rename_action.setEnabled(False)
            self.open_action.setEnabled(False)
            transform_menu.setEnabled(False)
            self.delete_action.setEnabled(False)
            new_menu.setEnabled(True)
            self.new_folder_action.setEnabled(True)
            self.new_file_action.setEnabled(True)
        elif item.text(1) == 'other':
            self.rename_action.setEnabled(False)
            self.open_action.setEnabled(False)
            transform_menu.setEnabled(False)
            self.delete_action.setEnabled(True)
            new_menu.setEnabled(False)
            self.new_folder_action.setEnabled(False)
            self.new_file_action.setEnabled(False)

        pop_menu.addAction(self.open_action)
        pop_menu.addAction(self.rename_action)
        pop_menu.addMenu(new_menu)
        new_menu.addAction(self.new_file_action)
        new_menu.addAction(self.new_folder_action)
        pop_menu.addMenu(transform_menu)
        transform_menu.addAction(self.file_to_map_action)
        transform_menu.addAction(self.txt_to_html_action)
        transform_menu.addAction(self.html_to_word_action)
        pop_menu.addSeparator()
        pop_menu.addAction(self.delete_action)

        pop_menu.exec_(QCursor.pos())

        return pop_menu
    
    # 响应树状列表双击
    def on_tree_double_click(self):
        item = self.right_tree.currentItem()
        if item.text(1) and item.text(1) != 'Note' and item.text(1) != 'Folder':
            if item.file.type == 'txt' or item.file.type == 'md':
                self.notepad.append(None)
                self.notepad[-1] = Notepad()
                self.notepad[-1].open_out_file(item.file.file_name, item.file.file_path)
                self.notepad[-1].show()
            else:
                os.popen(item.file.file_path)

    # 创建动作
    def create_actions(self):
        self.open_action = QAction("&打开", self, triggered=self.open_note)
        self.file_to_map_action = QAction("&思维导图", self, triggered=self.file_to_map)
        self.txt_to_html_action = QAction("&html", self, triggered=self.txt_to_html)
        self.html_to_word_action = QAction("&word", self, triggered=self.html_to_word)
        self.delete_action = QAction("&删除", self, triggered=self.delete_file)
        self.new_file_action = QAction("&新建笔记", self, triggered=self.new_note_file)
        self.new_folder_action = QAction("&新建文件夹", self, triggered=self.new_folder)
        self.rename_action = QAction("&重命名", self, triggered=self.rename)

    # 重命名
    def rename(self):
        item = self.right_tree.currentItem()
        father = item.parent()
        former_name = item.text(0)
        former_path = item.tag.path
        new_name = self.new_file_dialog('rename')
        if new_name:
            new_path = former_path.replace(former_name, new_name)
            if os.path.exists(new_path):
                print("ex")
                return
            else:
                os.rename(former_path, new_path)
            print(new_path)
            try:
                father.removeChild(item)
                father.tag = Tag(father.tag.tag, father.tag.path)
                new_item = QTreeWidgetItem(father)
                new_item.setText(0, new_name)
                new_item.setText(1, item.text(1))
                if item.text(1) == 'Folder':
                    new_item.setIcon(0, QIcon(icon_list['folder']))
                    new_item.tag = Tag(new_name, new_path)
                    new_item.tag.span_tree(self.note_tree.trie_root)
                    self.append_folder(new_item.tag, new_item)
                elif item.text(1) == 'Note':
                    new_item.setIcon(0, QIcon(icon_list['note']))
                    new_item.tag = Tag(new_name, new_path, tag_type='note')
                    new_item.tag.rename_files()
                    new_item.tag.span_tree(self.note_tree.trie_root)
                    self.append_file(new_item.tag, new_item)
            except:
                print('error')
                self.close()

    # 文本转html
    def txt_to_html(self):
        item = self.right_tree.currentItem()
        html_name = item.file.file_name
        html_path = txt2html(item.file.file_path)
        html_file = NoteFile(html_name, html_path)

        father = item.parent()
        number = father.childCount()
        if number:
            for i in range(number):
                child = father.child(i)
                if child.text(0) == html_name and child.text(1) == 'html':
                    father.removeChild(child)
                    break

        html_item = QTreeWidgetItem(father)
        html_item.setText(0, html_name)
        html_item.setText(1, 'html')
        html_item.setText(2, html_file.time)
        html_item.setIcon(0, QIcon(icon_list['html']))
        html_item.file = html_file
        self.note_tree.trie_root.insert(html_name, html_path)

    # html转docx
    def html_to_word(self):
        item = self.right_tree.currentItem()
        word_name = item.file.file_name

        html_exist = True
        if item.file.type == 'txt' or item.file.type == 'md':
            html_path = os.path.join(item.parent().tag.path, word_name+'.html')
            if not os.path.exists(html_path):
                html_path = txt2html(item.file.file_path)
                html_exist = False
        elif item.file.type == 'html':
            html_path = item.file.file_path

        father = item.parent()
        number = father.childCount()
        if number:
            for i in range(number):
                child = father.child(i)
                if child.text(0) == word_name and child.text(1) == 'docx':
                    father.removeChild(child)
                    break

        word_path = html2word(html_path)
        word_name = item.file.file_name
        word_file = NoteFile(word_name, word_path)
        word_item = QTreeWidgetItem(father)
        word_item.file = word_file
        word_item.setText(0, word_name)
        word_item.setText(1, 'docx')
        word_item.setText(2, word_file.time)
        word_item.setIcon(0, QIcon(icon_list['docx']))
        self.note_tree.trie_root.insert(word_name, word_path)

        if not html_exist:
            os.remove(html_path)

    # 新建笔记
    def new_note_file(self):
        item = self.right_tree.currentItem()
        print(item.tag.path)
        note_name = self.new_file_dialog('note')
        if note_name:
            note_folder_path = os.path.join(item.tag.path, note_name)
            print(note_folder_path)
            os.mkdir(note_folder_path)
            folder_item = QTreeWidgetItem(item)
            folder_item.setText(0, note_name)
            folder_item.setText(1, 'Note')
            folder_item.setIcon(0, QIcon(icon_list['note']))
            folder_item.tag = Tag(note_name, note_folder_path, 'note')
            note_path = os.path.join(note_folder_path, note_name+'.txt')
            note_txt = open(note_path, mode='w', encoding='utf-8')
            note_txt.close()
            note_item = QTreeWidgetItem(folder_item)
            note_item.setText(0, note_name)
            note_item.setText(1, 'txt')
            note_item.setIcon(0, QIcon(icon_list['txt']))
            note_item.file = NoteFile(note_name, note_path)
            self.note_tree.trie_root.insert(note_name, note_path)

    # 新建文件提示框
    def new_file_dialog(self, mold):
        try:
            if mold == 'note':
                name, ok = QInputDialog.getText(self, "Awesome Note", "笔记名称：")
            elif mold == 'folder':
                name, ok = QInputDialog.getText(self, "Awesome Note", "文件夹名称：")
            elif mold == 'rename':
                name, ok = QInputDialog.getText(self, "Awesome Note", "名称：")
            if ok:
                return name
        except:
            pass

    # 新建文件夹
    def new_folder(self):
        item = self.right_tree.currentItem()
        print(item.tag.path)
        folder_name = self.new_file_dialog('folder')
        if folder_name:
            folder_path = os.path.join(item.tag.path, folder_name)
            if os.path.exists(folder_path):
                print('ex')
                return
            print(folder_path)
            os.mkdir(folder_path)
            folder_item = QTreeWidgetItem(item)
            folder_item.setText(0, folder_name)
            folder_item.setText(1, 'Folder')
            folder_item.setIcon(0, QIcon(icon_list['folder']))
            folder_item.tag = Tag(folder_name, folder_path)

    # 重新加载
    def reload(self):
        new_home = Home(self.root, self.recent_notes)
        new_home.show()

    # 删除
    def delete_file(self):
        item = self.right_tree.currentItem()
        ret = self.confirm_delete_window(item.text(0))
        if ret:
            if item.text(1) == 'Folder' or item.text(1) == 'Note':
                shutil.rmtree(item.tag.path)
            else:
                os.remove(item.file.file_path)

            try:
                item.parent().removeChild(item)
            except:
                pass
        else:
            pass

    # 确认删除
    def confirm_delete_window(self, name):
        content = "确认删除“" + name + "”吗？"
        alert_box = QMessageBox(self)
        confirm_button = alert_box.addButton("确定", QMessageBox.ActionRole)
        cancel_button = alert_box.addButton("取消", QMessageBox.ActionRole)

        alert_box.setWindowTitle("Awesome Note")
        alert_box.setWindowIcon(QIcon("image/app.png"))
        alert_box.setText(content)
        alert_box.exec_()

        click_event = alert_box.clickedButton()
        if confirm_button == click_event:
            return 1
        elif cancel_button == click_event:
            return 0

    # 响应搜索按钮
    def on_search_click(self):
        self.search_result.clear()
        search_key = self.search_bar.text()
        search_results = []
        if search_key:
            self.note_tree.trie_root.get_file_path(search_key, search_results)
            if len(search_results):
                for result in search_results:
                    if os.path.exists(result):
                        item_name = re.split('[\\\]', result)[-1]
                        item_file = NoteFile(item_name, result)
                        item = QListWidgetItem(self.search_result)
                        item.setText(item_name)
                        item.setIcon(QIcon(icon_list[item_file.type]))
                        item.file = item_file
        else:
            print('None')

        self.search_result.itemDoubleClicked.connect(self.on_search_result_double_click)

    # 双击打开搜索结果
    def on_search_result_double_click(self):
        item = self.search_result.currentItem()
        if item.file.type == 'txt' or item.file.type == 'md':
            self.notepad.append(None)
            self.notepad[-1] = Notepad()
            self.notepad[-1].open_out_file(item.file.file_name, item.file.file_path)
            self.notepad[-1].show()
        else:
            os.popen(item.file.file_path)

    # 打开笔记
    def open_note(self):
        item = self.right_tree.currentItem()
        if item.file.type == 'txt' or item.file.type == 'md':
            self.notepad.append(None)
            self.notepad[-1] = Notepad()
            self.notepad[-1].open_out_file(item.file.file_name, item.file.file_path)
            self.notepad[-1].show()
        else:
            os.popen(item.file.file_path)

    # 笔记转换为思维导图
    def file_to_map(self):
        item = self.right_tree.currentItem()
        start_time = datetime.datetime.now()
        xmind_name, xmind_path = draw_map(item.file.file_name, item.file.file_path)
        end_time = datetime.datetime.now()
        print(end_time - start_time)
        file = NoteFile(xmind_name, xmind_path)
        print(sys.getsizeof(file))
        father = item.parent()
        number = father.childCount()
        if number:
            for i in range(number):
                child = father.child(i)
                if child.text(0) == xmind_name and child.text(1) == 'xmind':
                    father.removeChild(child)
                    break

        xmind = QTreeWidgetItem(item.parent())
        xmind.setText(0, file.file_name)
        xmind.setText(1, file.type)
        xmind.setText(2, file.time)
        xmind.file = file
        xmind.setIcon(0, QIcon(icon_list[file.type]))
        self.note_tree.trie_root.insert(xmind_name, xmind_path)

    # 添加文件夹子类
    def append_folder(self, father_tag, father_node):
        for child_tag in father_tag.children:
            child = QTreeWidgetItem(father_node)
            child.setText(0, child_tag.tag)
            child.tag = child_tag
            if child_tag.type == "note":
                child.setText(1, "Note")
            else:
                child.setText(1, "Folder")
            child.setIcon(0, QIcon(icon_list[child_tag.type]))
            if child_tag.get_children_num:
                self.append_folder(child_tag, child)
            if child_tag.get_file_num:
                self.append_file(child_tag, child)

    # 添加笔记子类
    def append_file(self, father_tag, father_node):
        for child_file in father_tag.files:
            child = QTreeWidgetItem(father_node)
            child.setText(0, child_file.file_name)
            child.setText(1, child_file.type)
            child.setText(2, child_file.time)
            child.file = child_file
            child.setIcon(0, QIcon(icon_list[child_file.type]))

    # 新建Notepad界面
    def open_notepad(self):
        self.notepad.append(None)
        self.notepad[-1] = Notepad()
        self.notepad[-1].show()

    def open_about_window(self):
        self.about_window = About()
        self.about_window.show()


def splash():
    splash_window = QSplashScreen(QPixmap(icon_list['cover']))
    splash_window.setWindowOpacity(0.9)
    splash_window.show()
    time.sleep(4)
    splash_window.close()


def run():
    app = QApplication(sys.argv)
    splash()
    home = Home()
    home.show()
    sys.exit(app.exec_())
