# https://contest.yandex.ru/contest/100803/run-report/168416129/

import sys
from dataclasses import dataclass

sys.setrecursionlimit(1000000)


@dataclass
class AvlNode:
    key: int
    left: "AvlNode | None" = None
    right: "AvlNode | None" = None
    height: int = 1


def get_height(node: AvlNode | None) -> int:
    return node.height if node else 0


def update_height(node: AvlNode) -> None:
    node.height = 1 + max(get_height(node.left), get_height(node.right))


def balance_factor(node: AvlNode) -> int:
    return get_height(node.right) - get_height(node.left)


def rotate_left(a: AvlNode) -> AvlNode:
    b = a.right
    a.right = b.left
    b.left = a
    update_height(a)
    update_height(b)
    return b


def rotate_right(a: AvlNode) -> AvlNode:
    b = a.left
    a.left = b.right
    b.right = a
    update_height(a)
    update_height(b)
    return b


def balance(v: AvlNode) -> AvlNode:
    update_height(v)
    b = balance_factor(v)

    if b == 2:
        u = v.right
        if balance_factor(u) >= 0:
            return rotate_left(v)
        else:
            v.right = rotate_right(u)
            return rotate_left(v)
    elif b == -2:
        u = v.left
        if balance_factor(u) <= 0:
            return rotate_right(v)
        else:
            v.left = rotate_left(u)
            return rotate_right(v)
    return v


def add(root: AvlNode | None, key: int) -> AvlNode:
    if root is None:
        return AvlNode(key)
    if key < root.key:
        root.left = add(root.left, key)
    elif key > root.key:
        root.right = add(root.right, key)
    else:
        return root
    return balance(root)


def find_min(root: AvlNode | None) -> AvlNode | None:
    current = root
    while current and current.left:
        current = current.left
    return current


def delete(root: AvlNode | None, key: int) -> AvlNode | None:
    if root is None:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        succ = find_min(root.right)
        assert succ is not None
        root.key = succ.key
        root.right = delete(root.right, succ.key)
    return balance(root) if root else None


def exists(root: AvlNode | None, key: int) -> bool:
    current = root
    while current:
        if key == current.key:
            return True
        elif key < current.key:
            current = current.left
        else:
            current = current.right
    return False


def next_key(root: AvlNode | None, key: int) -> int | None:
    current = root
    ans = None
    while current:
        if current.key >= key:
            ans = current.key
            current = current.left
        else:
            current = current.right
    return ans


def prev_key(root: AvlNode | None, key: int) -> int | None:
    current = root
    ans = None
    while current:
        if current.key <= key:
            ans = current.key
            current = current.right
        else:
            current = current.left
    return ans


def print_tree(root: AvlNode | None) -> str:
    res = []

    def build_avl(node):
        if node:
            res.append(node.key)
            build_avl(node.left)
            build_avl(node.right)

    build_avl(root)
    if not res:
        return "Empty"
    return " ".join(map(str, res))


def solution():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    q = int(input_data[0])
    root: "AvlNode | None" = None
    output = []
    for i in range(1, q + 1):
        if i >= len(input_data):
            break
        parts = input_data[i].split()
        cmd = parts[0]
        val = int(parts[1]) if len(parts) > 1 else 0

        if cmd == "add":
            root = add(root, val)
        elif cmd == "del":
            root = delete(root, val)
        elif cmd == "exists":
            output.append("YES" if exists(root, val) else "NO")
        elif cmd == "next":
            output.append(str(next_key(root, val)))
        elif cmd == "prev":
            output.append(str(prev_key(root, val)))
        elif cmd == "root":
            output.append(str(root.key if root else "Empty"))
        elif cmd == "height":
            output.append(str(get_height(root)))
        elif cmd == "print":
            output.append(print_tree(root))

    print("\n".join(output))


if __name__ == "__main__":
    solution()
