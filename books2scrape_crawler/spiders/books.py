import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    def start_requests(self):
        yield scrapy.Request(url='http://books.toscrape.com',headers={
            'User-Agent': self.user_agent
        })
        
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ol[@class='row']//h3/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='pager']/li[position()=last()]/a"), process_request='set_user_agent')
    )

    def set_user_agent(self,request,spider):
        request.headers['User-Agent'] = self.user_agent
        return request
    
    def parse_item(self, response):
        yield{
            'name': response.xpath("//article[@class='product_page']//h1/text()").get(),
            'price': response.xpath("//p[@class='price_color']/text()").get(),
            'availability': response.xpath("normalize-space((//p[@class='instock availability']/text())[2])").get(),
            'genre': response.xpath(".//ul[@class='breadcrumb']/li[3]/a/text()").get(),
            'book_url': response.url,
            'user-agent': response.request.headers['User-Agent']
        }