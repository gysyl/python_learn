from oop.main import Counter


def test_counter_increment_and_reset():
    c = Counter()
    assert c.increment() == 1
    assert c.increment(2) == 3
    c.reset()
    assert c.value == 0
