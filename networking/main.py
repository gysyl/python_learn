from urllib.parse import parse_qs, urlencode, urlparse


def build_url(base: str, params: dict) -> str:
    qs = urlencode(params)
    return f"{base}?{qs}" if params else base


def parse_params(url: str) -> dict:
    parsed = urlparse(url)
    return {k: v[0] for k, v in parse_qs(parsed.query).items()}


if __name__ == "__main__":
    u = build_url("https://example.com", {"q": "python", "page": 1})
    print(u)
    print(parse_params(u))
