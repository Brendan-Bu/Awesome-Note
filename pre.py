from note import Tag, recent_list
from search import *


class NoteSystem:
    def __init__(self, tag, root_path):
        self.root_path = root_path
        self.tag = tag
        self.root = Tag(tag, root_path)
        self.trie_root = Trie()

    def span_tree(self):
        self.root.span_tree(self.trie_root)
        self.recent_list = recent_list
