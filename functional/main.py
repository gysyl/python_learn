from collections.abc import Callable, Iterable


def apply_pipeline(seq: Iterable, funcs: list[Callable]):
    """将若干函数依次作用于序列"""
    result = list(seq)
    for f in funcs:
        result = list(map(f, result))
    return result


if __name__ == "__main__":
    print(apply_pipeline([1, 2, 3], [lambda x: x * 2, lambda x: x + 1]))
