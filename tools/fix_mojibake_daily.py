from pathlib import Path

DAILY_DIR = Path(__file__).resolve().parent.parent / "daily"
SUMMARY_HEADER = "## 打卡总结模板"

MOJIBAKE_CHARS = set("åæçéíïÂ¼´µºÃÑ×°Ä")


def is_mojibake_line(s: str) -> bool:
    # Heuristic: line contains multiple mojibake indicators
    hits = sum(1 for ch in s if ch in MOJIBAKE_CHARS)
    return hits >= 2


def fix_line(s: str) -> str:
    try:
        return s.encode("latin-1", errors="ignore").decode("utf-8", errors="ignore")
    except Exception:
        return s


def dedupe_summary(text: str) -> str:
    # Keep only the last occurrence of SUMMARY_HEADER
    idxs = []
    start = 0
    while True:
        i = text.find(SUMMARY_HEADER, start)
        if i == -1:
            break
        idxs.append(i)
        start = i + len(SUMMARY_HEADER)
    if len(idxs) <= 1:
        return text
    # Remove earlier occurrences leaving the last
    last = idxs[-1]
    # Remove everything between earlier headers and the last header
    parts = []
    pos = 0
    for i in idxs[:-1]:
        parts.append(text[pos:i])
        # skip until next header or last header
        # Find next header after i
        j = text.find(SUMMARY_HEADER, i + len(SUMMARY_HEADER))
        if j == -1:
            j = last
        pos = j
    parts.append(text[pos:])
    return "".join(parts)


def fix_file(fp: Path) -> bool:
    orig = fp.read_text(encoding="utf-8", errors="replace")
    lines = orig.splitlines()
    changed = False
    fixed_lines = []
    for ln in lines:
        if is_mojibake_line(ln):
            new_ln = fix_line(ln)
            if new_ln != ln:
                changed = True
                ln = new_ln
        fixed_lines.append(ln)
    text = "\n".join(fixed_lines) + "\n"
    # Deduplicate summary blocks
    de_text = dedupe_summary(text)
    if de_text != text:
        changed = True
        text = de_text
    if changed:
        fp.write_text(text, encoding="utf-8")
    return changed


def main():
    if not DAILY_DIR.exists():
        print("No daily directory found:", DAILY_DIR)
        return
    changed_count = 0
    for md in sorted(DAILY_DIR.glob("*.md")):
        if fix_file(md):
            changed_count += 1
            print("Fixed:", md)
    print(
        f"Processed {len(list(DAILY_DIR.glob('*.md')))} files, fixed {changed_count}."
    )


if __name__ == "__main__":
    main()
