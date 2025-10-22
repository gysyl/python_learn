from html.parser import HTMLParser


class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._capture = False
        self.titles: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2"):
            self._capture = True

    def handle_endtag(self, tag):
        if tag in ("h1", "h2"):
            self._capture = False

    def handle_data(self, data):
        if self._capture:
            text = data.strip()
            if text:
                self.titles.append(text)


def parse_titles(html: str) -> list[str]:
    parser = TitleParser()
    parser.feed(html)
    return parser.titles


if __name__ == "__main__":
    demo = "<html><body><h1>Demo Title</h1><h2>Sub Title</h2></body></html>"
    print(parse_titles(demo))
