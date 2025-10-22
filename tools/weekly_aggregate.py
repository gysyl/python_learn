import argparse
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

DAILY_DIR = Path(__file__).resolve().parent.parent / "daily"
WEEKLY_DIR = Path(__file__).resolve().parent.parent / "weekly"

CHECKBOX_DONE = re.compile(r"\[[xX]\]")
CHECKBOX_ANY = re.compile(r"\[(?:x|X|\s)\]")


def parse_date_from_name(name: str) -> date:
    y, m, d = map(int, name.split("-")[:3])
    return date(y, m, d)


def count_checkboxes(text: str) -> tuple[int, int]:
    total = len(CHECKBOX_ANY.findall(text))
    done = len(CHECKBOX_DONE.findall(text))
    return done, total


def read_text_safely(fp: Path) -> str:
    encodings = ["utf-8", "utf-8-sig", "gb18030", "cp936", "latin-1"]
    for enc in encodings:
        try:
            return fp.read_text(encoding=enc)
        except Exception:
            continue
    # Fallback to binary with replacement
    return fp.read_bytes().decode("utf-8", errors="replace")


def gather_daily() -> dict[tuple[int, int], list[dict]]:
    groups: dict[tuple[int, int], list[dict]] = defaultdict(list)
    if not DAILY_DIR.exists():
        return {}
    for fp in sorted(DAILY_DIR.glob("*.md")):
        dt = parse_date_from_name(fp.stem)
        iso = dt.isocalendar()  # year, week, weekday
        txt = read_text_safely(fp)
        done, total = count_checkboxes(txt)
        groups[(iso.year, iso.week)].append(
            {
                "date": dt,
                "path": fp,
                "rel": f"daily/{fp.name}",
                "done": done,
                "total": total,
            }
        )
    # sort entries per week by date
    for key in groups:
        groups[key].sort(key=lambda x: x["date"])
    return groups


def render_weekly(year: int, week: int, entries: list[dict]) -> str:
    header = f"# 周报 {year}-{week}\n\n"
    summary_done = sum(e["done"] for e in entries)
    summary_total = sum(e["total"] for e in entries)
    meta = (
        f"- 周内天数：{len(entries)}\n"
        f"- 完成勾选：{summary_done} / {summary_total}\n"
    )
    lines = [header, meta, "\n## 每日链接与完成情况\n"]
    for e in entries:
        lines.append(
            f"- {e['date']} — 完成 {e['done']} / {e['total']} — [{e['rel']}]({e['rel']})"
        )
    lines.append("\n## 备注\n- 可在 daily 文件中勾选任务为 [x]，周报自动汇总统计。\n")
    return "\n".join(lines) + "\n"


def write_weekly(groups: dict[tuple[int, int], list[dict]]) -> list[Path]:
    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for (year, week), entries in sorted(groups.items()):
        out = WEEKLY_DIR / f"{year}-{week}.md"
        out.write_text(render_weekly(year, week, entries), encoding="utf-8")
        outputs.append(out)
    return outputs


def write_index(groups: dict[tuple[int, int], list[dict]]) -> Path:
    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["# 周报索引\n"]
    for year, week in sorted(groups.keys()):
        rel = f"{year}-{week}.md"
        lines.append(f"- [{year}-{week}](./{rel})")
    out = WEEKLY_DIR / "index.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main():
    groups = gather_daily()
    if not groups:
        print("No daily files found.")
        return
    parser = argparse.ArgumentParser(
        description="Generate weekly reports from daily files"
    )
    parser.add_argument(
        "--current", action="store_true", help="Only generate current ISO week"
    )
    parser.add_argument("--year", type=int, help="Year of ISO week")
    parser.add_argument("--week", type=int, help="ISO week number")
    parser.add_argument(
        "--write-index", action="store_true", help="Write weekly index.md"
    )
    args = parser.parse_args()

    target = groups
    if args.current:
        iso = date.today().isocalendar()
        key = (iso.year, iso.week)
        target = {key: groups.get(key, [])}
    elif args.year and args.week:
        key = (args.year, args.week)
        target = {key: groups.get(key, [])}

    outputs = write_weekly(target)
    for p in outputs:
        print("Generated:", p)
    if args.write_index:
        idx = write_index(groups)
        print("Index:", idx)


if __name__ == "__main__":
    main()
