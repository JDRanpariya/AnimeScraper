from scrapy import Spider
import re
import json
from ..items import animeItem
import scrapy
from datetime import datetime
import time

# * working JDRanpariya

base_uri = "https://www.anime-planet.com"

class NameSpider(Spider):
    name = "animes"
    allowed_domains = ["anime-planet.com"]
    custom_settings = {'ITEM_PIPELINES': {'anime_scraper.pipelines.ScenePipeline': 400}}
    start_urls = [
        "https://www.anime-planet.com/anime/all"
    ]

    def parse(self, response):
        animes = response.xpath("//*[@data-type='anime']/a/@href").getall()
        
        for anime_url in animes:
            #print(base_uri + anime_url)
            yield scrapy.Request(url=base_uri + anime_url, callback=self.parse_anime)
        #time.sleep(0.5)
        #last_page_url = response.xpath("//div[@data-item='c-51 r-11 t-c-31 / middle right']/a/@href").get()
        #page_num = re.findall("\d+", last_page_url)[0]

        for page_num in range(1,2):
            yield scrapy.Request(url=f"https://www.anime-planet.com/anime/all?page={page_num}", callback=self.parse)


    def parse_anime(self, response):

            item = animeItem()

            item['title'] = response.xpath("//h1[@itemprop='name']/text()").get()
            if response.xpath("//h2[@class='aka']/text()").get() is not None:
                item['alt_title'] = response.xpath("//h2[@class='aka']/text()").get().strip()
            else:
                item['alt_title'] = None

            # ! -> get trailer for anime
            item['preview_url'] = None
            item['no_of_episodes'] = int(re.findall("\d+", response.xpath("//div[@class='pure-1 md-1-5']/span/text()").get())[0])
            item['thumbnail_url'] = [base_uri + response.xpath("//img[@itemprop='image']/@src").get()]

            
            if response.xpath("//div[@class='pure-1 md-3-5']/div/p/text()").getall() == []:
                item['description'] = None
            else:
                lines = response.xpath("//div[@class='pure-1 md-3-5']/div/p/text()").getall()
                description = ''.join(line for line in lines)
                description = description.replace("\n","")
                item['description'] = description

            # ! TODO -> get gallary urls for anime
            item['gallary_urls'] = None
            item['studio'] = response.xpath("//div[@class='pure-1 md-1-5'][2]/a/text()").get()
            item['characters'] = response.xpath("//a[@data-character-type='characters']/article/div/strong/text()").getall()

            # ! TODO -> convert date from string to datetime obj
            item['release_date'] = None # * its string -> response.xpath("//div[@class='pure-1 md-1-5'][3]/a/text()").get()
            item['rating'] = 5
            if response.xpath("//div[@class='pure-1 md-1-5'][5]/text()").get() is not None:
                item['rank'] = response.xpath("//div[@class='pure-1 md-1-5'][5]/text()").get().split("#")[-1]
            else:
                item['rank'] = None
            item['reviews'] = response.xpath("//a[@class='ShortReview rounded-card']/p/text()").getall()

            tags = []
            for tag in response.xpath("//div[@class='tags ']/ul/li/a/text()").getall():
                tags.append(tag.strip())

            item['tags'] = tags


            yield item
