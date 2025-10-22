import argparse
import os
from pathlib import Path


def rename_files(
    directory: Path, pattern: str, replacement: str, dry_run: bool = True
) -> int:
    count = 0
    for root, _, files in os.walk(directory):
        for name in files:
            if pattern in name:
                old_path = Path(root) / name
                new_name = name.replace(pattern, replacement)
                new_path = Path(root) / new_name
                if dry_run:
                    print(f"DRY-RUN: {old_path} -> {new_path}")
                else:
                    old_path.rename(new_path)
                    print(f"RENAMED: {old_path} -> {new_path}")
                count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description="批量重命名文件，支持 DRY-RUN")
    parser.add_argument("directory", type=Path, help="目标目录")
    parser.add_argument("pattern", type=str, help="匹配的子串")
    parser.add_argument("replacement", type=str, help="替换为的子串")
    parser.add_argument(
        "--apply", action="store_true", help="执行真实重命名（默认仅预览）"
    )
    args = parser.parse_args()

    count = rename_files(
        args.directory, args.pattern, args.replacement, dry_run=not args.apply
    )
    print(f"Total affected files: {count}")


if __name__ == "__main__":
    main()
