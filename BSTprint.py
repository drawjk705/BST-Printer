import random
import math


class Node(object):
    """docstring for Node"""

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)


def get_balance(node):

    if node is None:
        return 0

    return height(node.left) - height(node.right)


def height(node):
    if node is None:
        return 0
    else:
        return node.height


def contains(root, key):
    if root is None:
        return False

    if key > root.key:
        return contains(root.right, key)
    elif key < root.key:
        return contains(root.left, key)
    else:
        return True


def left_rotate(node):
    right = node.right
    r_l_children = right.left

    right.left = node
    node.right = r_l_children

    node.height = 1 + max(height(node.left), height(node.right))
    right.height = 1 + max(height(right.left), height(right.right))

    return right


def right_rotate(node):
    left = node.left
    l_r_children = left.right

    left.right = node
    node.left = l_r_children

    node.height = 1 + max(height(node.left), height(node.right))
    left.height = 1 + max(height(left.left), height(left.right))

    return left


def insert_node(root, key):
    if contains(root, key):
        return root

    if root is None:
        return Node(key)

    if key < root.key:
        root.left = insert_node(root.left, key)
    elif key > root.key:
        root.right = insert_node(root.right, key)

    root.height = 1 + max(height(root.left), height(root.right))

    balance = get_balance(root)

    if balance > 1:
        if key < root.left.key:
            # R
            return right_rotate(root)

        if key > root.left.key:
            # LR
            root.left = left_rotate(root.left)
            return right_rotate(root)

    elif balance < -1:
        if key > root.right.key:
            # L
            return left_rotate(root)

        if key < root.right.key:
            # RL
            root.right = right_rotate(root.right)
            return left_rotate(root)

    return root


def max_left(root):
    if root is None:
        return None
    if root.right is None:
        return root
    return max_left(root.right)


def min_right(root):
    if root.left is None:
        return root
    return min_right(root.left)


def delete_node(root, key):

    if not contains(root, key):
        return root

    if key > root.key:
        root.right = delete_node(root.right, key)
    elif key < root.key:
        root.left = delete_node(root.left, key)
    else:
        to_swap = max_left(root.left)
        if to_swap is None:
            to_swap = min_right(root.right)
            # will only have right children,
            # since nothing else can be lesser
            root.right = to_swap.right
        else:
            # will only have left children,
            # since nothing else can be greater
            root.left = to_swap.left
        if to_swap is None:
            # delete self
            root = None
        else:
            root.key = to_swap.key
            # delete self now
            to_swap = None

    if root is None:
        return root

    root.height = 1 + max(height(root.left), height(root.right))

    balance = get_balance(root)

    if balance > 1:
        if get_balance(root.left) >= 0:
            root.left = left_rotate(root.left)
            return right_rotate(root)

        elif get_balance(root.left) < 0:
            return right_rotate(root)

    elif balance < -1:

        if get_balance(root.right) > 0:
            root.right = right_rotate(root.right)
            return left_rotate(root)

        elif get_balance(root.right) <= 0:
            return left_rotate(root)

    return root


def pre_order(root):
    if root is None:
        return

    print(root)
    pre_order(root.left)
    pre_order(root.right)


def get_levels(root):
    levels = [[] for x in range(root.height)]

    queue = []

    queue.append(root)

    index = 0
    while len(queue) > 0 and index < root.height:
        current = queue.pop(0)
        levels[index].append(current)
        if len(levels[index]) == pow(2, index):
            index += 1
        if current is not None:
            queue.append(current.left)
            queue.append(current.right)
        else:
            queue.append(None)
            queue.append(None)

    for i in levels:
        print(i)

    return levels


def print_tree(root, levels, index=0):

    # print(levels[index])

    max_height = len(levels)
    height = max_height - index

    dist_from_side = pow(2, height) - 2
    slash_depth = pow(2, height - 1) - 1

    space_bw_nodes = pow(2, height + 1) - 1

    print(' ' * dist_from_side, end='')

    # print appropriate number of nodes
    for i in range(len(levels[index])):
        length = 0
        if levels[index][i] is not None:
            length = len(str(levels[index][i])) - 1
            print(levels[index][i], end='')
        else:
            print(" ", end='')
        print(" " * (space_bw_nodes - length), end='')
    print()

    space_bw_slash_sibs = 1
    space_bw_slash_rels = space_bw_nodes - 2

    if slash_depth > 3:

        space_bw_slash_sibs += (2 * (slash_depth - 1))
        space_bw_slash_rels -= 2 * (slash_depth - 2)
        dist_from_side -= 1 * (slash_depth - 2)

        dist_from_side -= 1
        print(' ' * dist_from_side, end='')

        dash_count = int(math.floor(space_bw_slash_sibs / 2))

        for node in levels[index]:
            if node is not None:
                if node.left is not None:
                    print('-' * dash_count, end='')
                else:
                    print(' ' * dash_count, end='')

                print('^', end='')

                if node.right is not None:
                    print('-' * dash_count, end='')
                else:
                    print(' ' * dash_count, end='')

            print(' ' * space_bw_slash_rels, end='')
        print()
        slash_depth = 1
        space_bw_slash_rels -= 2

    for i in range(slash_depth):

        dist_from_side -= 1

        print(' ' * dist_from_side, end='')
        for node in levels[index]:
            if node is None:
                print(' ', end='')
                print(' ' * space_bw_slash_sibs, end='')
                print(' ', end='')
            elif node is not None:
                if node.left is not None:
                    print('/', end='')
                else:
                    print(' ', end='')
                print(' ' * space_bw_slash_sibs, end='')
                if node.right is not None:
                    print('\\', end='')
                else:
                    print(' ', end='')
            print(' ' * space_bw_slash_rels, end='')
        print()
        space_bw_slash_sibs += 2
        space_bw_slash_rels -= 2

    next = None
    if index + 1 < len(levels):
        for x in levels[index + 1]:
            if x is not None:
                next = x
                break
        if next is not None:
            print_tree(next, levels, index + 1)


def main():
    root = insert_node(None, 6)

    root = insert_node(root, 7)

    for i in range(32):
        rand = random.randint(1, 100)
        root = insert_node(root, rand)

    levels = get_levels(root)

    print_tree(root, levels)

    # root = insert_node(root, 49)

    # root = insert_node(root, 23)

    # root = insert_node(root, 2)

    # root = insert_node(root, 9)

    # root = insert_node(root, 13)

    # root = insert_node(root, 1)

    # pre_order(root)

    # levels = get_levels(root)

    # print_tree(root, levels)


if __name__ == '__main__':
    main()
