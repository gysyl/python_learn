"""
豆瓣 Top250 电影爬虫（带请求头与分页）

概览
- 目标：抓取 https://movie.douban.com/top250 的电影标题，共 10 页，每页 25 条。
- 反爬说明：若使用 requests 默认的 `User-Agent`，豆瓣可能返回“简化/空”页面结构，导致选择器选不到任何标题。
- 解决方案：在请求头中显式添加常见浏览器 UA、`Referer` 与 `Accept-Language`，尽量让服务端认为是正常浏览访问。
- 解析器选择：这里使用内置的 `html.parser`，无需额外依赖；若想更快、更严格，可改用 `lxml` 并安装对应库。
- 速率控制：每页之间 `sleep(1)`，降低请求频率，减少被限流的概率。

结构
- `fetch_page(start)`：按分页参数拉取页面并返回 BeautifulSoup 对象。
- `parse_titles(soup)`：使用 CSS 选择器从页面提取中文主标题（避免提取外文标题重复）。
"""
import time
import requests
from bs4 import BeautifulSoup

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


def fetch_page(start: int) -> BeautifulSoup:
    """按分页参数请求页面并返回解析后的 Soup。

    参数
    - start: 分页起始位置（0, 25, 50 ... 225），每页 25 条。

    说明
    - `params` 通过查询字符串传递分页参数，例如 `?start=0`。
    - `headers` 使用上方定义的浏览器风格请求头，提升抓取成功率。
    - `timeout` 设置合理超时，避免网络异常挂死；生产中还应配合重试策略。
    - `raise_for_status()` 会在响应码非 2xx 时抛出 `HTTPError`，便于上层统一处理。
    - 解析器这里使用 `html.parser`（内置）；若安装了 `lxml`，可改为 `"lxml"` 以提升解析性能。
    """
    resp = requests.get(
        BASE_URL,
        params={"start": start},
        headers=HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_titles(soup: BeautifulSoup) -> list[str]:
    """从页面中提取每个条目的中文主标题。

    选择器说明（按层级）
    - `div.item`：每个电影条目的容器。
    - `div.info div.hd a`：信息区的标题链接。
    - `span:nth-of-type(1)`：标题链接中的第一个 `span`，通常是中文主标题；
      第二个 `span`（若有）往往为外文名，可能造成重复，这里刻意只取第一个。

    如页面结构更新导致选择器失效，可打开网页审查元素，调整选择器。
    """
    nodes = soup.select("div.item div.info div.hd a span:nth-of-type(1)")
    return [n.get_text(strip=True) for n in nodes]


def main():
    """抓取任务的总入口与调度逻辑。

    流程说明
    - 遍历分页参数 `start=0..225`（步长 25），逐页请求与解析标题。
    - 每页的标题列表累加到 `all_titles`，最后统一按序号输出。
    - 请求之间使用 `sleep(1)` 做速率控制，降低被限流/封禁风险。

    异常处理策略
    - requests.HTTPError：由 `fetch_page()` 内的 `resp.raise_for_status()` 抛出，
      当响应码非 2xx（如 403/404/5xx）时出现；通常与权限、反爬或服务端故障相关。
      这里选择打印错误并继续处理下一页，以提高整体完成率。
    - requests.RequestException：requests 的通用基类异常，涵盖连接/读取超时、
      DNS 解析失败、连接被拒绝、SSL 错误、代理异常等网络层问题。处理方式同上。

    生产建议
    - 若用于生产抓取，建议增加重试（指数退避）、失败持久化日志、
      指标上报与告警，以及对特定状态码（如 429/403）做差异化策略。
    """

    all_titles = []  # 存放所有页的标题汇总
    for start in range(0, 250, 25):  # 豆瓣每页 25 条，start 从 0 到 225
        try:
            soup = fetch_page(start)  # 请求并解析该页；非 2xx 时在此抛出 HTTPError
            titles = parse_titles(soup)  # 提取中文主标题列表
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


if __name__ == "__main__":
    main()

