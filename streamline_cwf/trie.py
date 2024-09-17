class TrieNode:
    def __init__(self):
        self.children = {}
        self.handler = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, path, handler):
        node = self.root
        for part in path.split('/'):
            if part not in node.children:
                node.children[part] = TrieNode()
            node = node.children[part]
        node.handler = handler

    def search(self, path):
        node = self.root
        for part in path.split('/'):
            if part in node.children:
                node = node.children[part]
            else:
                return None
        return node.handler
