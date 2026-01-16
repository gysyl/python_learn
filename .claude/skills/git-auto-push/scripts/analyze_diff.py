#!/usr/bin/env python3
"""
Git Diff 分析工具
分析 Git 变更并生成提交信息建议
"""

import re
import subprocess
from pathlib import Path


def run_command(cmd: list[str]) -> str:
    """运行 shell 命令并返回输出"""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


def get_status() -> dict[str, list[str]]:
    """获取 Git 状态"""
    output = run_command(["git", "status", "--porcelain"])
    status = {
        "added": [],
        "modified": [],
        "deleted": [],
        "renamed": [],
    }

    for line in output.strip().split("\n"):
        if not line:
            continue
        status_code, path = line[:2], line[3:]

        if status_code == "A " or status_code == "A":
            status["added"].append(path)
        elif status_code == "M " or status_code == "M":
            status["modified"].append(path)
        elif status_code == "D " or status_code == "D":
            status["deleted"].append(path)
        elif status_code.startswith("R"):
            status["renamed"].append(path)

    return status


def get_diff_summary(files: list[str]) -> str:
    """获取文件变更摘要"""
    if not files:
        return ""

    output = run_command(["git", "diff", "--stat", *files])
    return output


def infer_module(files: list[str]) -> str:
    """从文件路径推断模块名"""
    if not files:
        return ""

    # 提取第一级目录作为模块名
    first_file = files[0]
    parts = Path(first_file).parts

    if len(parts) >= 2:
        return parts[0]

    return "root"


def detect_change_type(status: dict[str, list[str]], diff_output: str) -> str:
    """
    检测变更类型

    Returns: feat, fix, docs, style, refactor, perf, test, chore
    """
    files = (
        status["added"] + status["modified"] + status["deleted"] + status["renamed"]
    )

    # 检查是否为测试文件
    test_patterns = ["test_", "_test.py", "/tests/", "/test/"]
    if any(re.search("|".join(test_patterns), f) for f in files):
        # 检查 diff 内容判断是新增还是修复
        if "fix" in diff_output.lower() or "bug" in diff_output.lower():
            return "fix"
        return "test"

    # 检查是否为文档
    doc_patterns = [".md", "README", "CHANGELOG", "/docs/", "/doc/"]
    if any(re.search("|".join(doc_patterns), f, re.IGNORECASE) for f in files):
        return "docs"

    # 检查是否为配置文件
    config_patterns = [
        ".yaml",
        ".yml",
        ".toml",
        ".json",
        ".ini",
        ".cfg",
        "Makefile",
        "Dockerfile",
    ]
    if any(re.search("|".join(config_patterns), f, re.IGNORECASE) for f in files):
        if status["added"]:
            return "feat"
        return "chore"

    # 分析 diff 内容关键词
    diff_lower = diff_output.lower()

    # fix 相关关键词
    fix_keywords = ["fix", "bug", "error", "issue", "修复", "错误", "异常"]
    if any(kw in diff_lower for kw in fix_keywords):
        return "fix"

    # refactor 相关关键词
    refactor_keywords = [
        "refactor",
        "rename",
        "simplify",
        "重构",
        "重命名",
        "简化",
    ]
    if any(kw in diff_lower for kw in refactor_keywords):
        return "refactor"

    # perf 相关关键词
    perf_keywords = ["optim", "cache", "speed", "performance", "优化", "缓存", "加速"]
    if any(kw in diff_lower for kw in perf_keywords):
        return "perf"

    # feat 相关关键词
    feat_keywords = ["add", "new", "implement", "feature", "新增", "添加", "实现"]
    if any(kw in diff_lower for kw in feat_keywords) or status["added"]:
        return "feat"

    # 默认
    if status["added"]:
        return "feat"
    return "chore"


def generate_commit_message(status: dict[str, list[str]], diff_output: str) -> str:
    """生成中文提交信息"""
    files = (
        status["added"] + status["modified"] + status["deleted"] + status["renamed"]
    )

    if not files:
        return "无变更"

    change_type = detect_change_type(status, diff_output)
    module = infer_module(files)

    # 类型中文映射
    type_cn = {
        "feat": "新增",
        "fix": "修复",
        "docs": "更新文档",
        "style": "调整格式",
        "refactor": "重构",
        "perf": "优化性能",
        "test": "完善测试",
        "chore": "更新配置",
    }

    # 获取主文件名（不含扩展名）
    main_file = Path(files[0]).stem

    # 构建提交信息
    if module and module != "root":
        commit_msg = f"{change_type}({module}): {type_cn[change_type]}{main_file}"
    else:
        commit_msg = f"{change_type}: {type_cn[change_type]}{main_file}"

    return commit_msg


def main():
    """主函数"""
    status = get_status()

    if not any(status.values()):
        print("✓ 当前工作目录干净，无需提交")
        return

    files = (
        status["added"] + status["modified"] + status["deleted"] + status["renamed"]
    )
    diff_output = get_diff_summary(files)

    print("📋 检测到变更：")
    for f in status["added"]:
        print(f"  A  {f}")
    for f in status["modified"]:
        print(f"  M  {f}")
    for f in status["deleted"]:
        print(f"  D  {f}")
    for f in status["renamed"]:
        print(f"  R  {f}")

    commit_msg = generate_commit_message(status, diff_output)
    print(f"\n📝 建议的提交信息：\n  {commit_msg}")


if __name__ == "__main__":
    main()
