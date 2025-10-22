from functional.main import apply_pipeline


def test_apply_pipeline_basic():
    assert apply_pipeline([1, 2, 3], [lambda x: x * 2, lambda x: x + 1]) == [3, 5, 7]


def test_apply_pipeline_empty_seq():
    assert apply_pipeline([], [lambda x: x]) == []


def test_apply_pipeline_no_funcs():
    assert apply_pipeline([1, 2], []) == [1, 2]
