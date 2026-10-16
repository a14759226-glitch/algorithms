import sys
from dataclasses import dataclass

sys.setrecursionlimit(1000000)

@dataclass  # автоматически генерирует __init__ для класса
class AvlNode:
  key: int
  left: "AvlNode | None" = None
  right: "AvlNode | None"= None
  height: int = 1

def get_height(node: AvlNode | None) -> int:
  """Функция для получения высоты узла"""
  return node.height if node else 0

def update_height(node: AvlNode) -> None:
  """Функция пересчета высоты узла"""
  node.height = 1 + max(get_height(node.left), get_height(node.right))

def balance_factor(node: AvlNode) -> int:
  """Вычисление баланса узнала"""
  return get_height(node.right) - get_height(node.left)

def rotate_left(a: AvlNode) -> AvlNode:
  """Выполнение левого поворота вокруг узла a"""
  b = a.right
  a.right = b.left 
  b.left = a
  update_height(a) 
  update_height(b)
  return b # возвращаем новый корень поддерева
    
def rotate_right(a: AvlNode) -> AvlNode:
  """Выполнение правого поворота вокруг узла a"""
  b = a.left
  a.left = b.right
  b.right = a
  update_height(a)
  update_height(b)
  return b

def balance(v: AvlNode) -> AvlNode:
  """Балансировка узла"""
  update_height(v)
  b = balance_factor(v)

  if b == 2: # если правое поддерево слишком высокое
    # работаем относительно правых потомков
    u = v.right
    if balance_factor(u) >= 0: # перевешен вправо или сбалансирован
      return rotate_left(v)
    else: # перевешен влево 
      v.right = rotate_right(u)
      return rotate_left(v)
  elif b == -2: # если левое поддерево слишком высокое
    # работаем относительно левых потомков
    u = v.left
    if balance_factor(u) <= 0:  # сбалансирован или перевешен влево
      return rotate_right(v)
    else: # перевешен вправо
      v.left = rotate_left(u)
      return rotate_right(v)
  return v # если баланс в норме, возвращаем узел без изменений
    
def add(root: AvlNode | None, key: int) -> AvlNode:
  """Рекурсивная функция вставки ключа в дерево"""
  if root is None:
    return AvlNode(key) # дошли до пустого места => создаем и возвращаем новый узел
  if key < root.key:
    root.left = add(root.left, key) # вставляемый ключ меньше текущего => идем влево
  elif key > root.key:
    root.right = add(root.right, key) # ключ больше текущего => идем вправо
  else:
    return root # если ключ уже существует, просто возвращаем текущий корень
  return balance(root)

def find_min(root: AvlNode | None) -> AvlNode | None:
  """Поиска узла с минимальным ключом в поддереве"""
  current = root
  while current and current.left:
    current = current.left
  return current

def delete(root: AvlNode | None, key: int) -> AvlNode | None:
  """Функция удаления ключа из дерева"""
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
  return balance(root) if root else None # балансируем после удаления

def exists(root: AvlNode | None, key: int) -> bool:
  """Проверка наличия ключа в дереве"""
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
  """Поиск наименьшего ключа, который больше или равен заданному"""
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
  """Поиск наибольшего ключа, который меньше или равен заданному"""
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
  """Функция для обхода дерева"""
  res = []
  def build_avl(node):
    if node:
      res.append(node.key)
      build_avl(node.left) # обходим левое поддерево
      build_avl(node.right) # обходим правое поддерево

  build_avl(root) # начинаем обход с корня
  if not res:
    return "Empty"
  return " ".join(map(str, res))

def solution():
  input_data = sys.stdin.read().splitlines()  # считываем введеные данные построчно
  if not input_data:
    return
  q = int(input_data[0]) # количество запросов
  root: "AvlNode | None" = None # инициализизация пустого дерева
  output = []
  for i in range(1, q+1):
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
