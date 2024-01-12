from typing import List


class TreeNode:

    def __init__(self, val: str, parent=None):
        self.val = val
        self.parent = parent
        self.children = []
        if self.parent is not None and self.parent.children is not None:
            self.parent.children.append(self)

    def get_child(self, val):
        result = list(filter(lambda x: x.val == val, self.children))
        if not result:
            return None
        else:
            return result[0]

    def get_parent(self):
        return self.parent

    def has_child(self, val):
        return self.get_child(val) is None

    def is_stella(self):
        return self.val == '*'

    def __str__(self):
        return self.val


@staticmethod
def generate_tree(data: List[str], split: str = ".") -> TreeNode:
    result = TreeNode('')
    for key in data:
        paths = key.split(split)
        cursor = result
        for path in paths:
            if cursor.has_child(path):
                child = TreeNode(path, cursor)
                cursor = child
            else:
                cursor = cursor.get_child(path)
    return result


if __name__ == '__main__':
    result = generate_tree(['test.*'])
    print('ok')
