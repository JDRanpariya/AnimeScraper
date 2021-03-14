# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field



class animeItem(Item):

    title = Field()
    alt_title = Field()
    thumbnail_url = Field()
    preview_url = Field()
    no_of_episodes = Field()
    description = Field()
    gallary_urls = Field()
    studio = Field()
    characters = Field() 
    release_date = Field()
    rating = Field()
    rank = Field()
    tags = Field()
    reviews = Field()


class characterItem(Item):

    name = Field()
    gender = Field()
    alt_name = Field()
    description = Field()
    profile_pic = Field() # get age from here
    hair_color = Field()
    rank = Field()
    rating = Field()
    animes = Field()
    movies = Field()


class movieItem(Item):

    movie_title = Field()
    movie_cover = Field()
    movie_trailer = Field()
    description = Field()
    length = Field()
    gallary_urls = Field()
    studio = Field()
    characters = Field() 
    release_date = Field()
    rating = Field()
    rank = Field()
    tags = Field()
    reviews = Field()


