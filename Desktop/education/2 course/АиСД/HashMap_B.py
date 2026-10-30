# https://contest.yandex.ru/contest/102171/run-report/169309125/

import sys


def solution():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    k = int(input_data[1])
    u = [int(x) for x in input_data[2:]]
    counts = {}

    for i in range(k):
        val = u[i]
        counts[val] = counts.get(val, 0) + 1
    result = [str(len(counts))]

    for i in range(1, n - k + 1):
        left_val = u[i - 1]
        right_val = u[i + k - 1]

        counts[left_val] -= 1
        if counts[left_val] == 0:
            del counts[left_val]

        counts[right_val] = counts.get(right_val, 0) + 1
        result.append(str(len(counts)))

    print(" ".join(result))


if __name__ == "__main__":
    solution()
