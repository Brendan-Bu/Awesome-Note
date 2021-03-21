import datetime
import time
import os
import os.path
import shutil
import re

recent_list = []
list_length = 10
file_type = ['txt', 'docx', 'html', 'pdf', 'xmind', 'md', 'png', 'jpg']


# 节点类
class Node:
    def __init__(self, title, father=None):
        self.title = title
        self.children = []
        self.descendant = []
        self.father = father
        self.body = []
        self.depth = 0

    # 输入主体内容
    def input_body(self, body):
        self.body = body

    # 获取主体内容
    def get_body(self):
        return self.body

    # 添加父亲
    def append_father(self, father):
        self.father = father

    # 添加深度
    def append_depth(self, depth):
        self.depth = depth

    # 获取父亲
    def get_father(self):
        return self.father

    # 获取标题
    def get_title(self):
        return self.title

    # 添加子标题
    def append_child(self, child_title):
        child = Note(child_title)
        self.children.append(child)
        return child

    # 获取子标题个数
    def get_children_number(self):
        return len(self.children)

    # 获取所有子标题
    def get_children(self):
        return self.children

    # 获取子孙数目
    def get_descendants_number(self, number):
        if self.get_children_number() == 0:
            return number+1

        for child in self.get_children():
            number = child.get_descendants_number(number)

        return number+1

    # DFS
    def dfs(self, g):
        topic = g.addSubTopic()
        topic.setTitle(self.title)
        for body in self.body:
            topic_body = topic.addSubTopic()
            topic_body.setTitle(body)
        if self.get_children_number() > 0:
            for child in self.children:
                child.dfs(topic)


# 笔记类
class Note(Node):
    def __init__(self, title):
        super(Note, self).__init__(title=title)
        self.time = datetime.datetime.now()
        self.tag = []

    # 获取节点数量
    def get_node_number(self):
        number = self.get_descendants_number(number=0)
        return number

    # 获取创建时间
    def get_time(self):
        return self.time

    # 添加标签
    def append_tag(self, tag):
        self.tag.append(tag)

    # 获取标签
    def get_tag(self):
        return self.tag

    # 获取标签数量
    def get_tag_number(self):
        return len(self.tag)

    # 生成导图
    def transform(self, g):
        root = g.getRootTopic()
        root.setTitle(self.title)
        if self.get_children_number() > 0:
            for child in self.children:
                child.dfs(root)


# 标签类
class Tag:
    def __init__(self, tag, path, tag_type='folder'):
        self.tag = tag
        self.type = tag_type
        self.path = path
        self.children = []
        self.files = []
        self.descendant = []
        self.depth = 0
        self.father = None
        self.time = os.path.getmtime(path)
        self.transfer_time()

    # 转换时间格式
    def transfer_time(self):
        time_structure = time.localtime(self.time)
        self.time = time.strftime('%Y-%m-%d %H:%M:%S', time_structure)

    # 获取标签
    def get_tag(self):
        return self.tag

    # 添加标签子孙
    def append_child(self, child):
        self.children.append(child)

    # 添加子文件
    def append_file(self, file):
        self.files.append(file)

    # 获取子文件数目
    def get_file_num(self):
        return len(self.files)

    # 获取子标签数目
    def get_children_num(self):
        return len(self.children)

    # 获取子孙列表
    def get_children(self):
        return self.children

    # 添加父亲节点
    def append_father(self, father):
        self.father = father

    # 获取父亲节点
    def get_father(self):
        return self.father

    # 生成树
    def span_tree(self, trie_root):
        for filter_name in os.listdir(self.path):
            filter_path = os.path.join(self.path, filter_name)
            if os.path.isdir(filter_path):
                child_filter = Tag(filter_name, filter_path)
                self.append_child(child_filter)
                child_filter.append_father(self)
                child_filter.span_tree(trie_root)
            else:
                file_name = re.split('[.]', filter_name)[0]
                file_path = filter_path
                if self.tag == file_name:
                    self.type = "note"
                    child_file = NoteFile(file_name, file_path)
                    self.append_file(child_file)
                    self.append_father(self)
                    trie_root.insert(file_name, file_path)
                else:
                    try:
                        filter_path = os.path.join(self.path, file_name)
                        if not os.path.exists(filter_path):
                            os.makedirs(filter_path)
                        shutil.move(file_path, os.path.join(filter_path, filter_name))
                        child_filter = Tag(file_name, filter_path)
                        self.append_child(child_filter)
                        child_filter.append_father(self)
                        child_filter.type = "note"
                        child_filter.span_tree(trie_root)
                    except:
                        pass

    # 重命名子文件
    def rename_files(self):
        for file_name in os.listdir(self.path):
            file_path = os.path.join(self.path, file_name)
            new_file_name = self.tag + '.' + re.split('[.]', file_name)[-1]
            new_file_path = file_path.replace(file_name, new_file_name)
            os.rename(file_path, new_file_path)


# 笔记文件类
class NoteFile:
    def __init__(self, file_name, file_path):
        self.file_name = re.split('[.]', file_name)[0]
        self.file_path = file_path
        self.type = self.file_type()
        self.father = None
        self.time_data = os.path.getmtime(file_path)
        self.transfer_time()
        self.is_recent_note(self)

    # 判断文件类型
    def file_type(self):
        current_type = re.split('[.]', self.file_path)[-1]
        if current_type in file_type:
            return current_type
        else:
            return 'other'

    # 转换时间格式
    def transfer_time(self):
        time_structure = time.localtime(self.time_data)
        self.time = time.strftime('%Y-%m-%d %H:%M', time_structure)

    # 添加父亲节点
    def append_father(self, father):
        self.father = father

    @staticmethod
    def is_recent_note(note):
        global recent_list, list_length
        length = len(recent_list)
        if length == 0:
            recent_list.append(note)
        else:
            note.insert_sort(note)

    @staticmethod
    def insert_sort(note):
        global recent_list, list_length
        note_time = int(note.time_data)
        for i in range(len(recent_list)):
            item_time = int(recent_list[i].time_data)
            # print('note:' + note.file_name + note.type + ' ' + str(note_time))
            # print('item:' + recent_list[i].file_name + recent_list[i].type + ' ' + str(item_time))
            if note_time >= item_time:
                recent_list.insert(i, note)
                if len(recent_list) > list_length:
                    recent_list = recent_list[:list_length-1]
                break
            elif i == len(recent_list)-1 and len(recent_list) < list_length:
                recent_list.append(note)

        list_length = max(list_length, len(recent_list))
