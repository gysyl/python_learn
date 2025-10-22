from scraping.main import parse_titles


def test_parse_titles_basic():
    html = "<h1>Hello</h1><p>x</p><h2>World</h2>"
    assert parse_titles(html) == ["Hello", "World"]


def test_parse_titles_no_titles():
    html = "<p>no titles</p>"
    assert parse_titles(html) == []
