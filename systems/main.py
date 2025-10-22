from pathlib import Path


def read_text_file(path: Path) -> str:
    return Path(path).read_text(encoding="utf-8")


if __name__ == "__main__":
    demo = Path(__file__).parent / "demo.txt"
    demo.write_text("hello systems", encoding="utf-8")
    print(read_text_file(demo))
