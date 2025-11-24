"""
Selenium 抓取豆瓣 Top250（分页 + 显式等待 + CSV/JSONL 持久化）

特性
- 使用 Selenium + Chrome 自动化，逐页抓取 Top250 的电影标题。
- 显式等待页面元素渲染，提升稳定性；每页可配置延迟以降低风控风险。
- 支持 CSV 与 JSONL 两种持久化格式，均支持追加（append）模式与覆盖写入。
- 详细中文注释与 CLI 参数，方便直接运行或嵌入到项目里。

运行示例
- 默认（无头模式）：
    python -m scraping.selenium_douban_top250
- 显示浏览器界面：
    python -m scraping.selenium_douban_top250 --show
- 仅保存 JSONL 并追加：
    python -m scraping.selenium_douban_top250 --jsonl douban_top250.jsonl --append
- 自定义每页抓取延迟（秒）：
    python -m scraping.selenium_douban_top250 --delay 1.5

依赖
- selenium>=4.6.0（你当前已安装 4.38.0，完全兼容）。
- 已安装 Google Chrome（你的版本为 142.x），Selenium Manager 会自动匹配 chromedriver。
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from typing import Iterable, List, Optional, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


BASE_URL = "https://movie.douban.com/top250"


def init_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    """初始化 Chrome WebDriver。

    - 默认使用新的无头模式；可通过 CLI 切换到可视化。
    - 设置基础选项与超时，减少环境噪音导致的初始化失败。
    """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--lang=zh-CN")
    # 可选：自定义 UA，进一步贴近真实浏览器指纹
    # options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.7444.163 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    driver.implicitly_wait(5)
    return driver


def wait_titles(driver: webdriver.Chrome, timeout: int = 12) -> List[str]:
    """等待页面加载完成并提取该页的电影标题。

    - 使用显式等待直到列表元素出现，避免空列表或半渲染状态。
    - 选择器（XPath）定位到主标题 `span[1]`，与先前 XPath 版本保持一致。
    """
    # 等待页面主列表出现
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//ol[@class='grid_view']//li"))
    )

    # 提取标题（主标题通常在第一个 span）
    elements = driver.find_elements(
        By.XPATH, "//ol[@class='grid_view']//li//div[@class='info']//div[@class='hd']/a/span[1]"
    )
    titles = [el.text.strip() for el in elements if el.text.strip()]
    return titles


def crawl_top250(driver: webdriver.Chrome, delay_per_page: float = 1.2) -> List[str]:
    """分页抓取 Top250 全部标题。

    - 共有 10 页，每页 25 条；按照 `?start=0,25,...,225` 访问。
    - 每页抓取后可选择延迟，以降低频率和风控概率。
    - 对单页超时进行捕获并继续下页，最大程度保证整体完成。
    """
    all_titles: List[str] = []
    for start in range(0, 250, 25):
        url = f"{BASE_URL}?start={start}"
        driver.get(url)
        try:
            page_titles = wait_titles(driver, timeout=12)
            print(f"抓取第 {start//25 + 1} 页，获得 {len(page_titles)} 条")
            all_titles.extend(page_titles)
        except TimeoutException:
            print(f"[警告] 第 {start//25 + 1} 页等待超时，跳过该页")
        # 适度延迟，避免过快访问
        time.sleep(max(delay_per_page, 0.0))

    return all_titles


def _ensure_dir(filepath: str) -> None:
    """确保输出目录存在。"""
    directory = os.path.dirname(os.path.abspath(filepath))
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def _count_existing_rows_csv(filepath: str) -> int:
    """用于 append 模式下 CSV 的连续编号，读取现有行数。

    - 首行通常是表头，不计入数据行。
    """
    if not os.path.exists(filepath):
        return 0
    try:
        with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)
            if not rows:
                return 0
            # 去掉表头
            return max(len(rows) - 1, 0)
    except Exception:
        return 0


def save_titles_csv(titles: Iterable[str], filename: str, append: bool = False) -> str:
    """保存标题到 CSV 文件。

    - 默认编码 `utf-8-sig` 以便 Excel 兼容。
    - 追加模式下会读取现有行数，实现连续编号。
    - 返回文件的绝对路径。
    """
    _ensure_dir(filename)
    mode = "a" if append else "w"
    start_index = _count_existing_rows_csv(filename) if append else 0
    try:
        with open(filename, mode, encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            if not append:
                writer.writerow(["index", "title"])  # 写入表头
            for i, title in enumerate(titles, start=start_index + 1):
                writer.writerow([i, title])
        abs_path = os.path.abspath(filename)
        print(f"CSV 保存完成: {abs_path}")
        return abs_path
    except Exception as e:
        print("[错误] 写入 CSV 失败:", e)
        return ""


def save_titles_jsonl(titles: Iterable[str], filename: str, append: bool = False) -> str:
    """保存标题到 JSON Lines 文件。

    - 追加模式：直接在文件尾部追加一行一个 JSON 对象。
    - 覆盖模式：若文件存在将清空重新写入。
    - 为保持一致性，也写入连续编号（index）。
    """
    _ensure_dir(filename)
    mode = "a" if append else "w"
    # 读取已有条数以连续编号（可选，若失败则从 1 开始）
    start_index = 0
    if append and os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                start_index = sum(1 for _ in f)
        except Exception:
            start_index = 0

    try:
        with open(filename, mode, encoding="utf-8") as f:
            for i, title in enumerate(titles, start=start_index + 1):
                f.write(json.dumps({"index": i, "title": title}, ensure_ascii=False) + "\n")
        abs_path = os.path.abspath(filename)
        print(f"JSONL 保存完成: {abs_path}")
        return abs_path
    except Exception as e:
        print("[错误] 写入 JSONL 失败:", e)
        return ""


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="使用 Selenium 抓取豆瓣 Top250 标题并持久化")
    parser.add_argument("--show", action="store_true", help="显示浏览器界面（默认无头模式）")
    parser.add_argument("--delay", type=float, default=1.2, help="每页抓取后延迟秒数")
    parser.add_argument("--csv", type=str, default="scraping_output/douban_top250_titles_selenium.csv", help="CSV 输出文件路径")
    parser.add_argument("--jsonl", type=str, default="scraping_output/douban_top250_titles_selenium.jsonl", help="JSONL 输出文件路径")
    parser.add_argument("--append", action="store_true", help="以追加模式写入 CSV/JSONL")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    try:
        driver = init_chrome_driver(headless=not args.show)
    except WebDriverException as e:
        print("[错误] WebDriver 初始化失败:", e)
        print("排查建议: 确认 Chrome 已安装且版本为 142.x；检查网络以便 Selenium Manager 下载驱动；必要时在公司网络或开启代理后重试。")
        return 1

    try:
        print("开始分页抓取豆瓣 Top250...")
        titles = crawl_top250(driver, delay_per_page=args.delay)
        print(f"累计获取 {len(titles)} 条标题")

        # 持久化（两种格式均保存）
        csv_path = save_titles_csv(titles, filename=args.csv, append=args.append)
        jsonl_path = save_titles_jsonl(titles, filename=args.jsonl, append=args.append)

        print("完成。输出文件:")
        print("- CSV:", csv_path or args.csv)
        print("- JSONL:", jsonl_path or args.jsonl)
        return 0
    finally:
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())