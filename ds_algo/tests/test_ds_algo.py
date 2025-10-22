from ds_algo.main import binary_search


def test_binary_search_found():
    assert binary_search([1, 2, 3, 4, 5], 4) == 3


def test_binary_search_not_found():
    assert binary_search([1, 2, 3], 10) == -1


def test_binary_search_edge_cases():
    assert binary_search([], 1) == -1
    assert binary_search([5], 5) == 0
