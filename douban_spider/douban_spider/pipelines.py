# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import json
import os
from typing import Optional

from itemadapter import ItemAdapter


class CsvJsonlPipeline:
    """将抓取结果同时写入 CSV 与 JSONL。

    配置项（settings.py）：
    - CSV_OUTPUT: CSV 输出文件路径（默认 scraping_output/douban_top250_scrapy.csv）
    - JSONL_OUTPUT: JSONL 输出文件路径（默认 scraping_output/douban_top250_scrapy.jsonl）
    - APPEND_OUTPUT: 是否以追加模式写入（默认 False）
    """

    def __init__(self, csv_path: str, jsonl_path: str, append: bool):
        self.csv_path = csv_path
        self.jsonl_path = jsonl_path
        self.append = append

        self.csv_file = None
        self.csv_writer = None
        self.jsonl_file = None
        self._csv_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        csv_path = settings.get("CSV_OUTPUT", "scraping_output/douban_top250_scrapy.csv")
        jsonl_path = settings.get(
            "JSONL_OUTPUT", "scraping_output/douban_top250_scrapy.jsonl"
        )
        append = bool(settings.get("APPEND_OUTPUT", False))
        return cls(csv_path, jsonl_path, append)

    def open_spider(self, spider):
        # 确保目录存在
        for path in (self.csv_path, self.jsonl_path):
            d = os.path.dirname(os.path.abspath(path))
            if d and not os.path.exists(d):
                os.makedirs(d, exist_ok=True)

        # CSV 打开与表头处理
        mode = "a" if self.append else "w"
        self.csv_file = open(self.csv_path, mode, encoding="utf-8-sig", newline="")
        self.csv_writer = csv.writer(self.csv_file)

        # 若是覆盖写入，直接写表头；若是追加，避免重复表头
        need_header = True
        if self.append and os.path.exists(self.csv_path):
            try:
                if os.path.getsize(self.csv_path) > 0:
                    need_header = False
                    # 读取现有行数（减去表头）用于连续编号
                    with open(
                        self.csv_path, "r", encoding="utf-8-sig", newline=""
                    ) as rf:
                        self._csv_count = max(sum(1 for _ in rf) - 1, 0)
            except Exception:
                need_header = False
        if need_header:
            self.csv_writer.writerow(["rank", "title", "link", "rating", "quote", "year"])

        # JSONL 打开
        self.jsonl_file = open(
            self.jsonl_path, "a" if self.append else "w", encoding="utf-8"
        )

    def close_spider(self, spider):
        try:
            if self.csv_file:
                self.csv_file.close()
        finally:
            self.csv_file = None
        try:
            if self.jsonl_file:
                self.jsonl_file.close()
        finally:
            self.jsonl_file = None

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        row = [
            adapter.get("rank"),
            adapter.get("title"),
            adapter.get("link"),
            adapter.get("rating"),
            adapter.get("quote"),
            adapter.get("year"),
        ]
        if self.csv_writer:
            # 连续编号保障：若 rank 缺失且需要递增，可替换；此处按 rank 字段为准
            self.csv_writer.writerow(row)
        if self.jsonl_file:
            self.jsonl_file.write(
                json.dumps(
                    {
                        "rank": adapter.get("rank"),
                        "title": adapter.get("title"),
                        "link": adapter.get("link"),
                        "rating": adapter.get("rating"),
                        "quote": adapter.get("quote"),
                        "year": adapter.get("year"),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
        return item
