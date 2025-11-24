# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Top250Item(scrapy.Item):
    """豆瓣 Top250 数据项。

    字段：
    - rank: 排名（1..250）
    - title: 主标题
    - link: 详情页链接
    - rating: 评分（float 或 str）
    - quote: 短评引语（可为空）
    - year: 发行年份（尽力提取）
    """

    rank = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    rating = scrapy.Field()
    quote = scrapy.Field()
    year = scrapy.Field()
