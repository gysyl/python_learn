import argparse
from pathlib import Path

import pandas as pd


def build_report(input_path: Path, output_path: Path):
    df = pd.read_excel(input_path)
    summary = df.describe(include="all")
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="raw", index=False)
        summary.to_excel(writer, sheet_name="summary")
    print(f"Report written to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="读取 Excel 并生成汇总报表")
    parser.add_argument("input", type=Path, help="输入 Excel 文件")
    parser.add_argument(
        "output", type=Path, nargs="?", help="输出报表文件（默认：report.xlsx）"
    )
    args = parser.parse_args()

    output = args.output or Path("report.xlsx")
    build_report(args.input, output)


if __name__ == "__main__":
    main()
