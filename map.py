from note import *
import xmind
import re


# 思维导图
class Map:
    def __init__(self, title, txt_path):
        self.title = title
        self.txt_path = txt_path
        self.xmind_path = re.split('[.]', txt_path)[0] + '.xmind'
        self.note = Note(self.title)

    # 提取所有标题生成树
    def find_title(self):
        node = self.note
        # 按行扫描文件
        for line in open(self.txt_path, mode='r', encoding='utf-8'):
            line = line.replace('\n', '')
            number = 0
            # 扫描‘#’的数量
            for word in line:
                if word == '#':
                    number += 1
                else:
                    break
            # 如果是标题
            if number > 0:
                title = line[number:]
            else:
                node.body.append(line)
                print(node.title + ': ' + node.body[-1])
                continue
            # 定位
            for i in range(node.depth+1-number):
                node = node.father
            # 添加节点
            print(title)
            child = node.append_child(title)
            child.append_father(node)
            child.append_depth(number)
            node = child

    # 画图
    def draw(self):
        if os.path.exists(self.xmind_path):
            os.remove(self.xmind_path)
        mind_map = xmind.load(self.xmind_path)
        sheet = mind_map.getPrimarySheet()
        sheet.setTitle(self.title)
        self.note.transform(sheet)

        xmind.save(mind_map)


def draw_map(file_name, file_path):
    mind_map = Map(file_name, file_path)
    mind_map.find_title()
    mind_map.draw()
    return mind_map.title, mind_map.xmind_path
