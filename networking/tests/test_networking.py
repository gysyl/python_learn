from networking.main import build_url, parse_params


def test_build_and_parse_url():
    u = build_url("https://example.com", {"q": "python", "page": 1})
    assert parse_params(u) == {"q": "python", "page": "1"}


def test_build_url_no_params():
    assert build_url("https://example.com", {}) == "https://example.com"
