from iter_gen.main import squares


def test_squares_basic():
    assert list(squares(5)) == [0, 1, 4, 9, 16]


def test_squares_zero():
    assert list(squares(0)) == []


def test_squares_negative():
    assert list(squares(-3)) == []
