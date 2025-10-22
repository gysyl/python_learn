class Counter:
    def __init__(self, start: int = 0):
        self.value = start

    def increment(self, step: int = 1) -> int:
        self.value += step
        return self.value

    def reset(self) -> None:
        self.value = 0


if __name__ == "__main__":
    c = Counter()
    print(c.increment())
    print(c.increment(2))
    c.reset()
    print(c.value)
