from pathlib import Path

DAILY_DIR = Path(__file__).resolve().parent.parent / "daily"

SUMMARY_HEADER = "## 打卡总结模板"
SUMMARY_BLOCK = (
    "\n\n" + SUMMARY_HEADER + "\n"
    "- 学到的 3 点：\n"
    "  - [ ] 1\n"
    "  - [ ] 2\n"
    "  - [ ] 3\n"
    "- 遇到的 2 个坑：\n"
    "  - [ ] 1\n"
    "  - [ ] 2\n"
    "- 明天计划 1 点：\n"
    "  - [ ] 1\n"
)


def read_text_safely(fp: Path) -> str:
    encodings = ["utf-8", "utf-8-sig", "gb18030", "cp936", "latin-1"]
    for enc in encodings:
        try:
            return fp.read_text(encoding=enc)
        except Exception:
            continue
    return fp.read_bytes().decode("utf-8", errors="replace")


def ensure_summary(fp: Path) -> bool:
    text = read_text_safely(fp)
    if SUMMARY_HEADER in text:
        return False  # already present
    # append block
    new_text = text.rstrip() + SUMMARY_BLOCK
    fp.write_text(new_text + "\n", encoding="utf-8")
    return True


def main():
    if not DAILY_DIR.exists():
        print("No daily directory found:", DAILY_DIR)
        return
    changed = 0
    for md in sorted(DAILY_DIR.glob("*.md")):
        if ensure_summary(md):
            changed += 1
            print("Appended:", md)
    print(f"Processed {len(list(DAILY_DIR.glob('*.md')))} files, appended {changed}.")


if __name__ == "__main__":
    main()
