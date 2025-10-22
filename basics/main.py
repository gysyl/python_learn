"""
Basics 脚本骨架：提供一个示例函数与 CLI 入口
"""

import argparse
import re


def normalize_text(
    s: str,
    preserve_case: bool = False,
    collapse_spaces: bool = True,
    collapse_crossline_only: bool = False,
) -> str:
    """基础字符串规范化：strip + lower(可选) + 折叠空白(可选)

    - preserve_case: 为 True 时保留原大小写；默认 False 转小写
    - collapse_spaces: 为 True 时进行空白折叠
    - collapse_crossline_only: 仅折叠跨行空白（含 \r\n），保留行内多空白
    """
    s = s.strip()
    if collapse_spaces:
        if collapse_crossline_only:
            # 折叠跨行空白（含 Windows 的 \r\n），并吞掉邻近的空格/制表符
            s = re.sub(r"[ \t]*(?:\r?\n)+[ \t]*", " ", s)
        else:
            s = re.sub(r"\s+", " ", s)
    if not preserve_case:
        s = s.lower()
    return s


def main():
    parser = argparse.ArgumentParser(description="Basics demo")
    parser.add_argument("text", nargs="?", default="  Hello   World\nPython  ")
    parser.add_argument(
        "--preserve-case", action="store_true", help="保留大小写，不转换为小写"
    )
    parser.add_argument(
        "--no-collapse-spaces", action="store_true", help="不折叠连续空白"
    )
    parser.add_argument(
        "--collapse-crossline-only",
        action="store_true",
        help="仅折叠跨行空白（保留行内多空白）",
    )
    parser.add_argument("--demo", action="store_true", help="展示规范化示例输出")
    args = parser.parse_args()

    if args.demo:
        samples = [
            "  Hello   World\nPython  ",
            "\tMix\ted   CASE   ",
            "   ",
            "Foo\nBar\tBaz",
            "A\r\nB   C",
        ]
        print("== Demo: 默认(小写+折叠空白) ==")
        for s in samples:
            print(repr(s), "=>", normalize_text(s))
        print("\n== Demo: 保留大小写 + 折叠空白 ==")
        for s in samples:
            print(repr(s), "=>", normalize_text(s, preserve_case=True))
        print("\n== Demo: 保留大小写 + 不折叠空白 ==")
        for s in samples:
            print(
                repr(s),
                "=>",
                normalize_text(s, preserve_case=True, collapse_spaces=False),
            )
        print("\n== Demo: 保留行内多空白 + 仅折叠跨行空白 ==")
        for s in samples:
            print(
                repr(s),
                "=>",
                normalize_text(s, preserve_case=True, collapse_crossline_only=True),
            )
    else:
        result = normalize_text(
            args.text,
            preserve_case=args.preserve_case,
            collapse_spaces=(not args.no_collapse_spaces),
            collapse_crossline_only=args.collapse_crossline_only,
        )
        print(result)


if __name__ == "__main__":
    main()
