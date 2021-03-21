import hashlib


class TireNode:

    def __init__(self, char, parent):
        self.word = char  # 当前节点的内容
        self.parent_node = parent  # 用于寻找存储当前字的节点的上一个节点
        self.child_node = {}  # 键值对为 word - node
        self.file_path = []  # 存当前节点保存的文件路径

    def modify_parent_node(self, new_parent_node):
        self.parent_node = new_parent_node

    def add_file_path(self, new_file_path):
        if new_file_path in self.file_path:
            return
        self.file_path.append(new_file_path)

    def remove_file_path(self, old_file_path):
        if old_file_path in self.file_path:
            self.file_path.remove(old_file_path)
        else:
            return


# 遍历一遍文件夹树的时候就要生成好这个字典树
# 字典树（多叉树)
# 优点：模糊查询，速度也较快
# 字典树类型一
# 实际可调用功能：insert(添加笔记) , get_file_path(查询笔记) , delete(删除笔记) , modify_filename(修改笔记名称）
class Trie:

    def __init__(self):
        self.root_node = TireNode(None, None)

    # 将一个文件名 filename 更新到字典树中
    def insert(self, filename, file_path):
        curNode = self.root_node  # curNode指向一个字典树节点类型的数据
        for word in filename:
            if word not in curNode.child_node:  # 此处查询的是键值
                # 生成新的节点，该节点的后继由words后面的决定
                new_node = TireNode(word, curNode)
                curNode.child_node[word] = new_node  # 创建新的节点上下链接
                curNode = new_node  # 从新的节点往下
            else:
                curNode = curNode.child_node[word]  # 延续当前路径继续往下
        curNode.add_file_path(file_path)  # 到达最后的节点位置

    # 一个小模块，为后面遍历提供一些辅助
    # 功能：查找filename在书中的最后一个节点
    # 返回值：如果有数据结构这一笔记；查数据，可以返回最后含有据这个字的节点；如果查数学，则会返回None
    def search(self, filename, error=None):
        notHave = error
        curNode = self.root_node  # curNode指向一个字典树节点类型的数据
        for word in filename:
            if word not in curNode.child_node:
                return notHave
            curNode = curNode.child_node[word]
            # 无论当前是否终止于非叶子节点，都返回这个节点
        return curNode

    # 访问以root为树根的所有叶子节点(包括root自身这个节点)，并将叶子节点中的文件路径放置在path_list中
    # path_list要求是一个空列表
    def visit(self, root_node, path_list):  # 去掉重复的路径！！！
        if root_node.file_path not in path_list:
            path_list += root_node.file_path
        for word in root_node.child_node:  # 遍历字典中的键
            curNode = root_node.child_node[word]
            if len(curNode.child_node) != 0:
                self.visit(curNode, path_list)
            elif curNode.file_path not in path_list:  # 去掉重复的路径
                path_list += curNode.file_path

    # 实现前缀的模糊查找
    def get_file_path(self, filename, path_list):
        notFound = "无此文件前缀名或文件"
        curNode = self.search(filename)
        if curNode is None:
            print(notFound)
            return
        # 若当前终止于非叶子节点，遍历后面所有的叶子节点
        self.visit(curNode, path_list)
        # print(path_list)

    # 难题二：修改名称和删除操作
    # 这个只有在要修改时调用，通过filename必定能找到一个叶子节点
    # 找到存有filename地址的叶子节点
    def find_file_path_node(self, filename):
        curNode = self.search(filename)  # curNode指向叶子节点
        if curNode is None:
            return
        return curNode

    def delete(self, old_filename, old_file_path):
        curNode = self.find_file_path_node(old_filename)
        curNode.file_path.remove(old_file_path)  # 无论什么清空都要清空这个文件的路径
        i = len(old_filename)
        while len(curNode.child_node) == 0 and len(
                curNode.file_path) == 0 and curNode is not self.root_node and i > 0:  # 查询是否能删除改建点
            temp = curNode.parent_node
            del temp.child_node[curNode.word]
            i = i - 1
            curNode = temp

    # 修改文件名(调用的前提条件是old_filename必定存在，否则会出错！）
    def modify_filename(self, old_filename, old_file_path, new_filename):
        self.delete(old_filename, old_file_path)
        self.insert(new_filename, old_file_path)


# 文件名-文件路径——哈希表
# 优点：查找速度快
# 缺点：还不能模糊查找，且只能查叶节点的笔记
# 在slots列表中查找到filename的下标后，在data列表对应的相同位置的数据项file_path即为关联数据
class FileHashTable:
    # 创建空映射slots - data
    def __init__(self):
        # 假设系统同时最多存储499个笔记类，因此设定哈希表大小最大为499（素数）
        # 创建时实际大小actual_size为 0 ,相同文件名称的但文件路径不同的笔记只占一个大小
        self.size = 499
        self.actual_size = 0
        # slots插槽列表用于保存filename
        self.slots = [None] * self.size

        # data列表用于保存数据项file_path
        self.data = [None] * self.size

    # 哈希函数；可能还不太完美，可以后续优化此函数
    def hash_function(self, filename):
        # filename可能带有中文字，需要转码
        string_16 = hashlib.md5(filename.encode("utf-8")).hexdigest()
        return int(string_16, 16) % self.size

    # 对于冲突，重新设置hash_value
    def rehash(self, old_hash):
        return (old_hash + 1) % self.size

    # 生成键对
    # index代表这个键对在哈希表里的下标，从0开始
    # key 键
    # data 数值
    def create_key_data(self, index, key, data):
        self.slots[index] = key
        self.data[index] = data
        self.actual_size += 1

    # 创建新的键对(filename - file path)，返回布尔值确定是否创建成功
    def put(self, filename, file_path):
        hash_value = self.hash_function(filename)
        Success = True
        # 难题一出现了
        # 文件特异性在于文件名，其次是路径
        # 二种情况：
        # 1）当前插槽中不存在键值
        # 2）在其他一切操作合法的情况下，不同路径下，可以出现同名文件(hash_value一样)
        # 3）当前插槽中已经存在了一个不同键对(不同：filename 不同)
        # 4）一般不考虑的情况，同名同路径的文件，这种情况就可以直接忽视
        # 对于（1）：无冲突，直接创建
        if self.slots[hash_value] is None:
            self.create_key_data(hash_value, filename, file_path)
        else:
            # 对于（2）：我们额外添加一个路径进去,最后查找时会将全部路径显示
            if self.slots[hash_value] == filename and self.data[hash_value] != file_path:
                temp_path = self.data[hash_value]
                temp_path.append(file_path)
                self.data[hash_value] = temp_path

            # 对于(3)：出现冲突，寻找下一个合适的插槽
            elif self.slots[hash_value] != filename:
                hash_value = self.rehash(hash_value)
                while self.slots[hash_value] is not None and self.slots[hash_value] != filename:
                    hash_value = self.rehash(hash_value)
                # 哈希回来起点，说明哈希表满了，报错??这里需要和其他模块的同学讨论一下
                if self.slots[hash_value] == filename:
                    return not Success
                else:
                    self.create_key_data(hash_value, filename, file_path)
        return Success

    # 通过给定的文件名file(key)，找到对应的文件路径file_path(value)的下标（实现查询功能）
    def get_index(self, filename):
        hash_value = self.hash_function(filename)
        NotFound = -1
        if self.slots[hash_value] == filename:
            return hash_value
        else:
            save = hash_value
            hash_value += 1
            while self.slots[hash_value] != filename and hash_value != save:
                hash_value += 1
                if hash_value == self.size:
                    hash_value = 0
            if hash_value == save:
                return NotFound
            else:
                return hash_value

    def get_file_path(self, filename):
        index = self.get_index(filename)
        NotFound = "无此笔记或储存空间已满"
        if index != -1:
            return self.data[index]
        else:
            return NotFound

    # 删除键对，最终结果就是哈希表里没有这个键对（原哈希表里可能有这个键对也可能没这个键对）
    def delete(self, filename):
        index = self.get_index(filename)
        if index == -1:
            return
        self.create_key_data(index, None, None)

    def len(self):
        return self.actual_size

    # 在用户进行文件名修改的时候需要使用到
    # 新的文件路径使用
    def modify_filename(self, old_filename, new_filename):
        hash_value = self.get_index(old_filename)
        self.create_key_data(hash_value, new_filename, self.data[hash_value])
