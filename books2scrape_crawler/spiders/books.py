import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ol[@class='row']//h3/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='pager']/li[position()=last()]/a"))
    )

    def parse_item(self, response):
        yield{
            'name': response.xpath("//article[@class='product_page']//h1/text()").get(),
            'price': response.xpath("//p[@class='price_color']/text()").get(),
            'availability': response.xpath("normalize-space((//p[@class='instock availability']/text())[2])").get(),
            'genre': response.xpath(".//ul[@class='breadcrumb']/li[3]/a/text()").get(),
            'book_url': response.url
        }