"""
Basics 脚本骨架：提供一个示例函数与 CLI 入口

本文件包含：
- 文本规范化函数 `normalize_text`，用于去除首尾空白、可选折叠空白、可选保留大小写。
- 命令行入口 `main`，展示函数的使用方式与演示输出。

快速使用示例：
- 作为模块调用：
    >>> normalize_text("  Hello   World\nPython  ")
    'hello world python'
- 命令行：
    python basics/main.py --demo
    python basics/main.py "Hello  \nWorld" --collapse-crossline-only --preserve-case

参数与实现细节：
- 正则模式详解见函数内注释：
  - r"\\s+": 折叠任意空白字符（空格、制表符、换行等）。
  - r"[ \t]*(?:\r?\n)+[ \t]*": 仅折叠跨行空白，且吞掉换行两侧的空格/制表符。
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

    参数说明：
    - s: 待处理的原始字符串。
    - preserve_case: 为 True 时保留原大小写；默认 False 转小写，便于比较与搜索。
    - collapse_spaces: 为 True 时进行空白折叠；为 False 保留原始空白结构。
    - collapse_crossline_only: 为 True 且 `collapse_spaces` 为 True 时，仅折叠跨行空白（含 \r\n），保留行内多个空格/制表符。

    行为总结：
    - 一律先执行 `strip()` 去除首尾空白。
    - 当 `collapse_spaces` 为 True：
      - 若 `collapse_crossline_only` 为 True：仅把跨行的空白替换为一个空格，同时吞掉换行两侧的空格/\t；行内多空格原样保留。
      - 否则：使用 r"\\s+" 把所有连续空白折叠为单个空格。
    - 当 `preserve_case` 为 False：统一转换为小写。

    示例：
    - normalize_text("Foo\nBar\tBaz") -> "foo bar baz"（默认折叠所有空白并转小写）
    - normalize_text("A\r\nB   C", preserve_case=True, collapse_crossline_only=True)
      -> "A B   C"（仅把跨行空白变为一个空格，保留行内多空格，保留大小写）
    """
    # 去除首尾空白，避免开头/结尾出现多余空格影响展示或比较。
    s = s.strip()

    if collapse_spaces:
        if collapse_crossline_only:
            # 仅折叠跨行空白：
            # - 非捕获组 (?:\r?\n)+ 匹配一个或多个换行（兼容 Windows 的 \r\n 与 *nix 的 \n）。
            # - 两侧 [ \t]* 匹配可选的空格/制表符，用于“吞掉”换行邻近的行尾/行首空白。
            # - 整体效果：把跨行边界及其两侧空白折叠为一个空格，保留行内多空格不动。
            s = re.sub(r"[ \t]*(?:\r?\n)+[ \t]*", " ", s)
        else:
            # 折叠任意空白字符（空格、制表符、换行等）为单个空格。
            # r"\\s+" 覆盖了大多数空白场景，适合做通用规范化。
            s = re.sub(r"\s+", " ", s)

    if not preserve_case:
        # 统一转为小写，减少大小写差异带来的比较/检索问题。
        s = s.lower()

    return s


def main() -> None:
    """命令行入口：解析参数并调用 `normalize_text`。

    支持参数：
    - text（可选位置参数）：要规范化的字符串；若省略则使用内置示例。
    - --preserve-case：保留大小写，不转换为小写。
    - --no-collapse-spaces：不折叠连续空白（保留原始空白结构）。
    - --collapse-crossline-only：仅折叠跨行空白，保留行内多空白（需与折叠开关配合）。
    - --demo：展示一组示例的规范化输出，便于理解各参数效果。

    典型用法：
    - python basics/main.py "Hello   World"  # 默认：折叠空白+转小写
    - python basics/main.py --demo            # 查看参数组合的行为差异
    """
    parser = argparse.ArgumentParser(description="Basics demo")

    # 位置参数：要处理的文本，省略时使用一个包含多种空白形式的默认示例。
    parser.add_argument("text", nargs="?", default="  Hello   World\nPython  ")

    # 是否保留大小写（默认会转为小写）。
    parser.add_argument(
        "--preserve-case", action="store_true", help="保留大小写，不转换为小写"
    )

    # 是否关闭空白折叠（默认开启折叠）。
    parser.add_argument(
        "--no-collapse-spaces", action="store_true", help="不折叠连续空白"
    )

    # 是否仅折叠跨行空白，同时保留行内的多个空格/制表符。
    parser.add_argument(
        "--collapse-crossline-only",
        action="store_true",
        help="仅折叠跨行空白（保留行内多空白）",
    )

    # 演示模式：打印多组规范化结果，帮助直观对比参数效果。
    parser.add_argument("--demo", action="store_true", help="展示规范化示例输出")

    args = parser.parse_args()

    if args.demo:
        # 一组包含不同空白与大小写的示例，便于展示各参数组合的行为差异。
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
        # 正常模式：根据命令行参数调用规范化函数并输出结果。
        result = normalize_text(
            args.text,
            preserve_case=args.preserve_case,
            collapse_spaces=(not args.no_collapse_spaces),
            collapse_crossline_only=args.collapse_crossline_only,
        )
        print(result)


if __name__ == "__main__":
    # 作为脚本运行时进入命令行逻辑；被其他模块导入时不会执行。
    main()
