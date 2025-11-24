from __future__ import annotations

import re
from urllib.parse import urlparse, parse_qs

import scrapy

from douban_spider.items import Top250Item


class Top250Spider(scrapy.Spider):
    name = "top250"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response: scrapy.http.Response):
        # 计算分页偏移，用于生成全局 rank
        query = parse_qs(urlparse(response.url).query)
        page_offset = int(query.get("start", [0])[0])

        # 每个条目位于 ol.grid_view 下的 li
        items = response.xpath("//ol[@class='grid_view']/li")
        for idx, li in enumerate(items, start=1):
            title = (
                li.xpath(".//div[@class='info']//div[@class='hd']/a/span[1]/text()")
                .get(default="")
                .strip()
            )
            link = li.xpath(".//div[@class='info']//div[@class='hd']/a/@href").get()
            rating = (
                li.xpath(
                    ".//span[contains(@class,'rating_num')]/text()"
                )
                .get(default="")
                .strip()
            )
            quote = (
                li.xpath(
                    ".//div[@class='info']//div[@class='bd']//p[@class='quote']/span/text()"
                )
                .get(default="")
                .strip()
            )
            info_text = " ".join(
                s.strip()
                for s in li.xpath(
                    ".//div[@class='info']//div[@class='bd']/p[1]//text()"
                ).getall()
            )
            year_match = re.search(r"(\d{4})", info_text)
            year = year_match.group(1) if year_match else ""

            item = Top250Item(
                rank=page_offset + idx,
                title=title,
                link=link,
                rating=rating,
                quote=quote,
                year=year,
            )
            yield item

        # 翻页：跟随 next
        next_href = response.xpath(
            "//div[@class='paginator']//span[@class='next']/a/@href"
        ).get()
        if next_href:
            yield response.follow(next_href, callback=self.parse)