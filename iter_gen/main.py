def squares(n: int):
    """生成 0..n-1 的平方序列"""
    for i in range(max(0, n)):
        yield i * i


if __name__ == "__main__":
    print(list(squares(5)))
