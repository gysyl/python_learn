from concurrency.main import run_in_threads


def test_run_in_threads_basic():
    out = run_in_threads(lambda x: x + 1, [1, 2, 3], max_workers=2)
    assert sorted(out) == [2, 3, 4]
