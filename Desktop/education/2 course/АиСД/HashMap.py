import sys
from typing import Any, Optional


def hash_poly(s: str, m: int, p: int = 31) -> int:
    """Полиномиальный хеш для строки"""
    h = 0
    power = 1
    for ch in s:
        h = (h + ord(ch) * power) % m
        power = (power * p) % m
    return h


class HashMap:
    """Хеш-таблица"""

    def __init__(self, capacity: int = 8) -> None:
        assert capacity > 0
        self.capacity = capacity
        self._TOMB = object()
        self.slots: list[Any] = [None] * capacity
        self.size = 0
        self.filled = 0

    def _h(self, key: str) -> int:
        return hash_poly(key, self.capacity)

    def put(self, key: str, value: int) -> None:
        if self.filled >= self.capacity // 2:
            self._resize(self.capacity * 2)
        first_tomb: Optional[int] = None
        for j in range(self.capacity):
            i = (self._h(key) + j) % self.capacity
            cell = self.slots[i]

            if cell is None:
                dest = first_tomb if first_tomb is not None else i
                self.slots[dest] = (key, value)
                self.size += 1
                if dest == i:
                    self.filled += 1
                return

            if cell is self._TOMB:
                if first_tomb is None:
                    first_tomb = i
                continue

            k, _ = cell
            if k == key:
                self.slots[i] = (key, value)
                return

        if first_tomb is not None:
            self.slots[first_tomb] = (key, value)
            self.size += 1
            return

    def get(self, key: str) -> Optional[int]:
        for j in range(self.capacity):
            i = (self._h(key) + j) % self.capacity
            cell = self.slots[i]

            if cell is None:
                return None

            if cell is self._TOMB:
                continue

            k, v = cell
            if k == key:
                return v
        return None

    def delete(self, key: str) -> Optional[int]:
        for j in range(self.capacity):
            i = (self._h(key) + j) % self.capacity
            cell = self.slots[i]

            if cell is None:
                return None

            if cell is self._TOMB:
                continue

            k, v = cell
            if k == key:
                self.slots[i] = self._TOMB
                self.size -= 1
                return v
        return None

    def _resize(self, new_capacity: int) -> None:
        old_slots = self.slots
        self.capacity = new_capacity
        self.slots = [None] * self.capacity
        self.size = 0

        for cell in old_slots:
            if cell is not None and cell is not self._TOMB:
                k, v = cell
                self.put(k, v)


def solution() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    q = int(input_data[0])
    ht = HashMap(capacity=16)
    out = []

    i = 1
    for _ in range(q):
        cmd = input_data[i]
        if cmd == "put":
            key = input_data[i + 1]
            val = int(input_data[i + 2])
            ht.put(key, val)
            i += 3
        elif cmd == "get":
            key = input_data[i + 1]
            res = ht.get(key)
            if res is None:
                out.append("Error")
            else:
                out.append(str(res))
            i += 2
        elif cmd == "del":
            key = input_data[i + 1]
            res = ht.delete(key)
            if res is None:
                out.append("Error")
            else:
                out.append(str(res))
            i += 2
        elif cmd == "size":
            out.append(str(ht.size))
            i += 1

    print("\n".join(out))


if __name__ == "__main__":
    solution()
