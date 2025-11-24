"""
豆瓣 Top250 电影爬虫（使用 XPath 解析，含详细注释）

概览
- 目标：抓取 https://movie.douban.com/top250 的电影中文主标题，共 10 页，每页 25 条。
- 与 `douban_top250_spider.py` 的区别：解析器改用 XPath（依赖 `lxml`）。
- 反爬说明：若使用默认 `User-Agent`，可能返回简化结构导致选择器失效，因此需设置常见浏览器请求头。
- 速率控制：每页之间 `sleep(1)`，降低限流/封禁风险。

依赖
- 需要安装 `lxml`：`pip install lxml`
- XPath 的优势：选择器语法规范、性能较好，且能更精确地选取目标节点。

结构
- `fetch_page(start)`：按分页参数请求页面并返回已解析的 HTML 文档节点。
- `parse_titles(doc)`：使用 XPath 从页面提取中文主标题（取第一个 `span`）。
- `main()`：遍历分页、处理异常、汇总并打印结果。
"""

import os
import csv
import json
import time
import requests
from lxml import etree


BASE_URL = "https://movie.douban.com/top250"
HEADERS = {
    # User-Agent：模拟常见桌面浏览器，避免返回“空结构”页面
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0 Safari/537.36"
    ),
    # Referer：指明来源，提高请求可信度；部分站点依赖该头判断来源合法性
    "Referer": BASE_URL,
    # Accept-Language：偏好中文，部分页面会根据该头返回更符合本地化的内容
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def fetch_page(start: int) -> etree._Element:
    """按分页参数请求页面并返回解析后的 HTML 文档根节点。

    参数
    - start: 分页起始位置（0, 25, 50 ... 225），每页 25 条。

    请求/解析说明
    - 通过查询字符串 `?start=<n>` 控制分页。
    - 使用浏览器风格请求头以提升抓取成功率。
    - `timeout=10` 设置合理超时，避免网络异常挂死；生产环境建议结合重试策略。
    - `raise_for_status()`：响应码非 2xx 时抛出 `HTTPError`，便于上层统一处理。
    - 使用 `lxml.etree.HTML` 将文本解析为可进行 XPath 查询的文档树。
    """
    resp = requests.get(
        BASE_URL,
        params={"start": start},
        headers=HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    return etree.HTML(resp.text)


def parse_titles(doc: etree._Element) -> list[str]:
    """使用 XPath 从页面中提取每个条目的中文主标题。

    选择器说明（按层级）
    - `//div[@class='item']`：每个电影条目的容器。
    - `//div[@class='info']//div[@class='hd']/a`：信息区的标题链接。
    - `span[1]/text()`：标题链接中的第一个 `span` 文本，通常是中文主标题；
      第二个 `span`（若有）往往为外文名，可能造成重复，这里刻意只取第一个。

    如页面结构更新导致选择器失效，可查看网页结构并调整 XPath。
    """
    texts: list[str] = doc.xpath("//div[@class='item']//div[@class='info']//div[@class='hd']/a/span[1]/text()")
    return [t.strip() for t in texts if t and t.strip()]


def main():
    """抓取任务的总入口与调度逻辑（XPath 版）。

    流程说明
    - 遍历分页参数 `start=0..225`（步长 25），逐页请求并以 XPath 解析标题。
    - 每页的标题列表累加到 `all_titles`，最后统一按序号输出。
    - 请求之间使用 `sleep(1)` 做速率控制，降低被限流/封禁风险。

    异常处理策略
    - `requests.HTTPError`：由 `fetch_page()` 内的 `resp.raise_for_status()` 抛出，
      当响应码非 2xx（如 403/404/5xx）时出现；通常与权限、反爬或服务端故障相关。
      这里选择打印错误并继续处理下一页，以提高整体完成率。
    - `requests.RequestException`：requests 的通用基类异常，涵盖连接/读取超时、
      DNS 解析失败、连接被拒绝、SSL 错误、代理异常等网络层问题。处理方式同上。

    生产建议
    - 建议增加重试（指数退避）、失败持久化日志、指标上报与告警；
      对特定状态码（如 429/403）可做差异化策略（延时、切代理、人工确认等）。
    """

    all_titles: list[str] = []  # 存放所有页的标题汇总
    for start in range(0, 250, 25):  # 豆瓣每页 25 条，start 从 0 到 225
        try:
            doc = fetch_page(start)  # 请求并解析该页；非 2xx 时在此抛出 HTTPError
            titles = parse_titles(doc)  # 使用 XPath 提取中文主标题列表
            print(f"[页 start={start}] 抓到 {len(titles)} 条")  # 便于观察每页有效结果
            all_titles.extend(titles)  # 汇总当前页结果到总列表
            time.sleep(1)  # 友好等待，避免过快请求导致限流
        except requests.HTTPError as e:
            # 说明：非 2xx 状态码（如 403/404/5xx）；可根据 e.response.status_code 定制处理
            print(f"请求失败(HTTP): {e}")
        except requests.RequestException as e:
            # 说明：网络相关异常（超时、连接失败、SSL、代理等）；不中断整体流程，继续下一页
            print(f"请求失败: {e}")

    # 输出总结果（若存在失败页，数量可能小于 250）
    print(f"共抓到 {len(all_titles)} 部电影：")
    for idx, title in enumerate(all_titles, 1):
        print(f"{idx:03d}. {title}")

    # 将结果持久化到 CSV（追加写入）与 JSONL（追加写入）
    csv_path = save_titles_csv(all_titles, append=True)
    jsonl_path = save_titles_jsonl(all_titles, append=True)
    if csv_path:
        print(f"CSV 已保存到: {csv_path}")
    else:
        print("CSV 保存失败：未生成文件")
    if jsonl_path:
        print(f"JSONL 已保存到: {jsonl_path}")
    else:
        print("JSONL 保存失败：未生成文件")


if __name__ == "__main__":
    main()


def save_titles_csv(titles: list[str], filename: str | None = None, append: bool = False) -> str:
    """将标题列表保存为 CSV 文件，返回保存路径。

    设计说明
    - 默认保存到脚本同级目录 `douban_top250_titles_xpath.csv`。
    - CSV 两列：`index`（从 1 开始的序号）、`title`（中文主标题）。
    - 使用 `utf-8-sig` 编码，保证在 Excel 中打开不会乱码。
    - 支持追加写入：在已有文件末尾追加，不重复写入表头；索引递增。

    参数
    - titles: 标题列表（已按抓取顺序排列）。
    - filename: 指定保存文件名（可选）。若为空，则使用默认路径。
    - append: 是否追加写入（True 追加；False 覆盖）。

    返回
    - 成功时返回保存的文件绝对路径；失败时返回空字符串。
    """
    try:
        if filename is None:
            base_dir = os.path.dirname(__file__)  # 脚本同级目录
            filename = os.path.join(base_dir, "douban_top250_titles_xpath.csv")

        file_exists = os.path.exists(filename)
        mode = "a" if append else "w"

        # 计算追加时的起始索引，尽量保持连续编号
        start_index = 1
        write_header = True
        if append and file_exists:
            write_header = os.path.getsize(filename) == 0
            # 尝试读取最后的索引值；如果失败则退化为逐行计数
            try:
                with open(filename, "r", encoding="utf-8-sig", newline="") as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                    # 如果有表头，去掉一行
                    if rows and rows[0] == ["index", "title"]:
                        data_rows = rows[1:]
                    else:
                        data_rows = rows
                    if data_rows:
                        last_idx = int(data_rows[-1][0])
                        start_index = last_idx + 1
                    else:
                        start_index = 1
            except Exception:
                # 任何解析失败情况，退化为按行数+1
                try:
                    with open(filename, "r", encoding="utf-8-sig") as f:
                        line_count = sum(1 for _ in f)
                    # 若存在表头，索引从行数开始；否则从行数+1开始
                    start_index = max(1, line_count)
                except Exception:
                    start_index = 1
        else:
            write_header = True

        with open(filename, mode, newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["index", "title"])  # 写入表头
            for offset, title in enumerate(titles, 0):
                writer.writerow([start_index + offset, title])

        return os.path.abspath(filename)
    except OSError as e:
        # 文件写入相关异常（权限、路径不存在、磁盘问题等）
        print(f"保存文件失败: {e}")
        return ""


def save_titles_jsonl(titles: list[str], filename: str | None = None, append: bool = True) -> str:
    """将标题列表保存为 JSON Lines（.jsonl），返回保存路径。

    设计说明
    - 默认保存到脚本同级目录 `douban_top250_titles_xpath.jsonl`。
    - 每行一个 JSON 对象：`{"index": <int>, "title": <str>}`。
    - 采用 JSONL 格式便于追加写入与流式处理；编码使用 `utf-8`。
    - 索引在追加模式下会尝试连续递增：根据已有行数或最后一行计算起始值。

    参数
    - titles: 标题列表（已按抓取顺序排列）。
    - filename: 指定保存文件名（可选）。若为空，则使用默认路径。
    - append: 是否追加写入（True 追加；False 覆盖）。

    返回
    - 成功时返回保存的文件绝对路径；失败时返回空字符串。
    """
    try:
        if filename is None:
            base_dir = os.path.dirname(__file__)
            filename = os.path.join(base_dir, "douban_top250_titles_xpath.jsonl")

        file_exists = os.path.exists(filename)
        mode = "a" if append else "w"

        # 计算追加时的起始索引
        start_index = 1
        if append and file_exists and os.path.getsize(filename) > 0:
            try:
                # 尝试读取最后一行的 index
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                # 从最后一行向上找到非空行
                for line in reversed(lines):
                    line = line.strip()
                    if not line:
                        continue
                    obj = json.loads(line)
                    if isinstance(obj, dict) and "index" in obj:
                        start_index = int(obj["index"]) + 1
                        break
                else:
                    # 没找到可用行，则按行数+1
                    start_index = len([l for l in lines if l.strip()]) + 1
            except Exception:
                # 回退为按行数+1
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        start_index = sum(1 for l in f if l.strip()) + 1
                except Exception:
                    start_index = 1

        with open(filename, mode, encoding="utf-8") as f:
            for offset, title in enumerate(titles, 0):
                obj = {"index": start_index + offset, "title": title}
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")

        return os.path.abspath(filename)
    except OSError as e:
        print(f"保存 JSONL 失败: {e}")
        return ""