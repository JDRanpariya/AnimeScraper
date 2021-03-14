from scrapy import Spider
from string import ascii_uppercase
import re
import json, logging
from ..items import characterItem
import scrapy
from datetime import datetime
import time

base_uri = "https://www.anime-planet.com"

class AnimePerformerSpider(Spider):
    name = "ap_characters"
    allowed_domains = ["anime-planet.com"]
    custom_settings = {'ITEM_PIPELINES': {'anime_scraper.pipelines.PerformerPipeline': 400}}
    start_urls = [
        "https://www.anime-planet.com/characters/all"
    ]
    

    def parse(self, response):

        characters = response.xpath("//*[@class='tableAvatar']/a[1]/@href").getall()

        for character_url in characters:
            #print(base_uri + scene_url)
            yield scrapy.Request(url=base_uri+character_url, callback=self.parse_character)
        #last_page_url = response.xpath("//li[@class='sowzbh-1 gjRQwQ'][7]/a/@href").get()
        #page_num = re.findall("\d+", last_page_url)[0]

        for page_num in range(1,3):
            yield scrapy.Request(url=f"https://www.anime-planet.com/characters/all?page={page_num}", callback=self.parse)

        


    def parse_character(self, response):

        #atr = response.xpath("//li/span/text()").getall() # bio fiels available

        item = characterItem()

        item['name'] = response.xpath("//h1[@itemprop='name']/text()").get()    # } DONE

        if response.xpath("//h2[@class='aka']/text()").get() is not None:
            item['alt_name'] = response.xpath("//h2[@class='aka']/text()").get().strip()
        else:
            item['alt_name'] = ''

        item['gender'] = response.xpath("//div[@class='pure-1 md-1-5']/text()").get().strip().split(":")[-1].strip()

        if response.xpath("//div[@itemprop='description']/p/text()").getall() == []:
            item['description'] = ''
        else:
            lines = response.xpath("//div[@itemprop='description']/p/text()").getall()
            description = ''.join(line for line in lines)
            description = description.replace("\n","")
            item['description'] = description

        item['profile_pic'] = [base_uri + response.xpath("//img[@itemprop='image']/@src").get()]



        if response.xpath("//div[@class='pure-1 md-1-5'][2]/text()").get() is not None:
            item['hair_color'] =  response.xpath("//div[@class='pure-1 md-1-5'][2]/text()").get().strip().split(":")[-1].strip()
        else:
            item['hair_color'] = ''

        if response.xpath("//div[@class='pure-1 md-1-5'][3]/text()").get() is not None:
           item['rank'] = response.xpath("//div[@class='pure-1 md-1-5'][3]/a/text()").get().split("#")[-1]
        else:
            item['rank'] = ''

        item['rating'] = 5

        yield item
