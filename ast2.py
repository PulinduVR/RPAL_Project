class ASTNode:
    def __init__(self, label):
        self.label = label
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def print_tree(self, level=0):
        print('.' * level + self.label)
        for child in self.children:
            child.print_tree(level + 1)
