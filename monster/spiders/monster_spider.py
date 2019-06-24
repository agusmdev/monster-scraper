# -*- coding: utf-8 -*-
import scrapy


class MonsterSpider(scrapy.Spider):
    name = 'monster_spider'
    start_urls = ['https://www.monster.com/jobs/search/?where=usa&stpage=1&page={}'.format(i) for i in range(1, 5001)]
    seen = set()


    def parse(self, response):
        jobs = response.xpath('//h2/a/@href')
        for job in jobs:
            if job not in self.seen:
                self.seen.add(job)
                yield response.follow(job, callback=self.parse_item)

    def parse_item(self, response):
        yield {
            'title':response.xpath('//h1/text()').extract(),
            'description':response.xpath('//div[@id="JobDescription"]//text()').extract(),
            'date':response.xpath('//dd[@class="value" and not(contains(., ","))]/text()').extract(),
            'location':response.xpath('//dd[@class="value" and contains(., ",")]/text()').extract(),
            'contractType':response.xpath('//dd[@class="value text-muted"]/text()').extract()
        }
