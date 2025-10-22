from pathlib import Path

from systems.main import read_text_file


def test_read_text_file(tmp_path: Path):
    p = tmp_path / "a.txt"
    p.write_text("abc", encoding="utf-8")
    assert read_text_file(p) == "abc"
