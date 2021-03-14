# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter


#class NsfwScraperPipeline:
#    def process_item(self, item, spider):
#        return item
#from scrapy import signals
import logging
from sqlalchemy.orm import sessionmaker
from anime_scraper.models import Anime, Rating, Studio, Movie, ReleaseDate, Character, db_connect, create_table
from .items import animeItem, characterItem, movieItem


class ScenePipeline(object):

    """Anime pipeline for storing scraped items in the database"""
    
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        

    def process_item(self, item, spider):

        session = self.Session()

        anime = Anime(
                    title = item['title'],
                    alt_title = item['alt_title'],
                    thumbnail_url = item['thumbnail_url'],
                    preview_url = item['preview_url'],
                    no_of_episodes = item['no_of_episodes'],
                    description = item['description'],
                    gallary_urls = item['gallary_urls'], 
                    rank = item['rank'],
                    #anime_reviews = item['anime_reviews']
                    #studio = item['studio'],        #FK
                    #performers = item['performers'],    #FK
                    #director = item['director'],    #FK
                    #release_date = item['release_date'],    #FK
                    #movie = item['movie'],  #FK
                    #tags = item['tags']     #FK
        )
        #performer
        for character in item['characters']:
            charactert = session.query(Character).filter_by(name=character).first()
            if charactert is not None:
                anime.characters.append(charactert)
            else:
                anime.characters.append(Character(name=character))

        #studio
        studio = session.query(Studio).filter_by(studio=item['studio']).first()
        if studio is not None:
            anime.studio = studio
        else:
            anime.studio = Studio(studio=item['studio'])
        
        #rating
        rating = session.query(Rating).filter_by(rating=item['rating']).first()
        
        if rating is not None:
            anime.rating = rating
        else:
            anime.rating = Rating(rating=item['rating'])

        #release_date
        release_date = session.query(ReleaseDate).filter_by(release_date=item['release_date']).first()
        if release_date is not None:
            anime.release_date = release_date
        else:
            anime.release_date = ReleaseDate(release_date=item['release_date'])

        anime_exists = session.query(Anime).filter(Anime.title == item['title']).first() is not None

        if anime_exists:
            logging.info(f'Item {item["title"]} vs {session.query(Anime).filter(Anime.title == item["title"]).first().title} is in db')
            return item
        else:
            try:
                session.add(anime)
                session.commit()
                logging.info(f'Item {anime} stored in db')
            except:
                logging.info(f'Failed to add {anime} to db')
                session.rollback()
                raise
            finally:
                session.close()
        return item


class PerformerPipeline(object):
    """Performer pipeline for storing scraped items in the database"""
    
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        

    def process_item(self, item, spider):

        session = self.Session()
        character = Character(
                    name = item['name'],
                    alt_name = item['alt_name'],
                    gender = item['gender'],
                    description = item['description'],
                    profile_pic = item['profile_pic'],
                    rank = item['rank'],
                    hair_color = item['hair_color'],

                    #rating = Rating(rating=item['rating'])
                    
        )

        rating = session.query(Rating).filter_by(rating=item['rating']).first()
        
        if rating is not None:
            character.rating = rating
        else:
            character.rating = Rating(rating=item['rating'])

        performer_exists = session.query(Character).filter_by(name = item['name']).first() is not None

        if performer_exists:
            #logging.info(item['name'])
            #logging.info(session.query(Performer).filter_by(name=item['name']).first())
            logging.info(f'Item {character} is in db')

            return item
        else:
            try:
                session.add(character)
                session.commit()
                logging.info(f'Item {character} stored in db')
            except:
                logging.info(f'Failed to add {character} to db')
                session.rollback()
                raise
            finally:
                session.close()
        return item