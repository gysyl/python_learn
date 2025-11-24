"""
Selenium 初始化脚本（Windows / Chrome 142）

功能
- 自动初始化 Chrome WebDriver（Selenium Manager 会匹配本机 Chrome 版本）。
- 可选择是否使用无头模式（headless）。
- 设置超时与基础选项，进行一次快速连通性检查。
- 打印浏览器与驱动版本信息，便于确认匹配情况。

使用方法
- 在项目根目录执行：
  `python -m scraping.selenium_init`  # 默认 headless
  或：`python -m scraping.selenium_init --show`  # 显示浏览器界面

说明
- 需要已安装 `selenium>=4.6.0`（你已安装 4.38.0）。
- Selenium Manager 会自动下载并缓存合适的 chromedriver。
- 若下载受网络限制，请在公司网络或开启代理后重试；也可改用 Edge/Firefox。
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def get_local_chrome_version() -> str:
    """在 Windows 上尝试读取本机 Chrome 版本（可选）。

    读取注册表 `HKCU\\Software\\Google\\Chrome\\BLBeacon` 的 `version` 键。
    若读取失败，返回空字符串。
    """
    try:
        import winreg  # type: ignore

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon"
        ) as key:
            version, _ = winreg.QueryValueEx(key, "version")
            return str(version)
    except Exception:
        return ""


def init_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    """初始化并返回一个已配置的 Chrome WebDriver。

    - headless=True 使用无头模式（适合服务器/不需要 UI）。
    - 通过 Selenium Manager 自动匹配并下载驱动，无需手动配置路径。
    """
    options = webdriver.ChromeOptions()
    if headless:
        # 使用新的无头模式，更接近真实渲染
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--lang=zh-CN")

    # 可选：降低日志噪音
    options.add_argument("--log-level=2")

    driver = webdriver.Chrome(options=options)
    # 基础超时配置
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    driver.implicitly_wait(5)
    return driver


def quick_smoke_test(driver: webdriver.Chrome) -> None:
    """访问一个稳定站点并打印标题与版本信息，验证初始化是否成功。"""
    driver.get("https://www.bing.com")
    print("页面标题:", driver.title)

    caps = driver.capabilities or {}
    browser_ver = caps.get("browserVersion")
    chrome_info = caps.get("chrome", {}) if isinstance(caps.get("chrome"), dict) else {}
    driver_ver = None
    # chromedriverVersion 的格式通常为 'xxx (xxxx)'
    if chrome_info:
        driver_ver = chrome_info.get("chromedriverVersion")

    print("Chrome 版本:", browser_ver or get_local_chrome_version() or "未知")
    if driver_ver:
        print("Chromedriver:", driver_ver)
    else:
        print("Chromedriver: 未从 capabilities 读取到（正常情况下仍已自动匹配）")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="初始化并验证 Selenium Chrome WebDriver")
    parser.add_argument(
        "--show", action="store_true", help="显示浏览器界面（默认无头模式）"
    )
    args = parser.parse_args(argv)

    print("检测到的本机 Chrome:", get_local_chrome_version() or "未能读取版本")

    try:
        driver = init_chrome_driver(headless=not args.show)
        try:
            quick_smoke_test(driver)
            return 0
        finally:
            driver.quit()
    except WebDriverException as e:
        print("[错误] WebDriver 初始化失败:", e)
        print("建议:")
        print("- 确认本机已安装 Chrome，并且版本为 142.x。")
        print("- 检查网络环境，确保可访问 Selenium 的驱动下载源。")
        print("- 如仍失败，可改用 Edge/Firefox 进行初始化测试。")
        return 1


if __name__ == "__main__":
    sys.exit(main())