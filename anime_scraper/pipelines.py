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
from anime_scraper.models import Anime, Rating, Tag, Studio, Movie, ReleaseDate, Character, db_connect, create_table
from .items import animeItem, characterItem, movieItem


class ScenePipeline(object):

    """Anime pipeline for storing scraped items in the database"""
    
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine, future=True)
        

    def process_item(self, item, spider):

        session = self.Session()

        scene = Anime(
                    title = item['title'],
                    alt_title = item['alt_title'],
                    thumbnail_url = item['thumbnail_url'],
                    preview_url = item['preview_url'],
                    no_of_episodes = item['no_of_episodes'],
                    description = item['description'],
                    gallary_urls = item['gallary_urls'], 
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
                scene.performers.append(charactert)
            else:
                scene.performers.append(Character(name=character))

        #tag
        for tag in item['tags']:
            #logging.info(tag, "theNewOne" , type([tag]))
            tagt = session.query(Tag).filter_by(tag_name=tag).first()
            if tagt is not None:
                scene.tags.append(tagt)
            else:
                scene.tags.append(Tag(tag_name=tag))

        #studio
        studio = session.query(Studio).filter_by(studio=item['studio']).first()
        if studio is not None:
            scene.studio = studio
        else:
            scene.studio = Studio(studio=item['studio'])
        
        #rating
        rating = session.query(Rating).filter_by(rating=item['rating']).first()
        if rating is not None:
            scene.rating = rating
        else:
            scene.rating = Rating(rating=item['rating'])

        #release_date
        release_date = session.query(ReleaseDate).filter_by(release_date=item['release_date']).first()
        if release_date is not None:
            scene.release_date = release_date
        else:
            scene.release_date = ReleaseDate(release_date=item['release_date'])

        scene_exists = session.query(Anime).filter_by(title=item['title']).first() is not None

        if scene_exists:
            logging.info(f'Item {scene} is in db')
            return item
        else:
            try:
                session.add(scene)
                session.commit()
                logging.info(f'Item {scene} stored in db')
            except:
                logging.info(f'Failed to add {scene} to db')
                session.rollback()
                raise
            finally:
                session.close()
        return item

class MoviePipeline(object):

    """Movie pipeline for storing scraped items in the database"""
    
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        

    def process_item(self, item, spider):

        session = self.Session()

        movie = Movie(
                    movie_title = item['movie_title'],
                    movie_cover = item['movie_cover'],
                    movie_trailer = item['movie_trailer'],
                    length = item['length'],
                    description = item['description'],
                    gallary_urls = item['gallary_urls'], 
                    #studio = item['studio'],            #FK
                    #performers = item['performers'],        #FK
                    #director = item['director'],        #FK
                    #release_date = item['release_date'],    #FK
                    #scenes = item['scenes'],            #FK
                    #genres = item['genres'],        #FK
                    #tags = item['tags']         #FK
        )
        
        #performer
        for character in item['characters']:
            performert = session.query(Character).filter_by(name=character).first()
            if performert is not None:
                movie.performers.append(performert)
            else:
                movie.performers.append(Character(name=character))


        #tag
        for count,tag in enumerate(item['tags']):
            #logging.info(tag, "theNewOne" , type([tag]))
            tagt = session.query(Tag).filter_by(tag=tag).first()
            if tagt is not None:
                movie.tags.append(tagt)
            else:
                movie.tags.append(Tag(tag=tag))

        #studio
        studio = session.query(Studio).filter_by(studio=item['studio']).first()
        if studio is not None:
            movie.studio = studio
        else:
            movie.studio = Studio(studio=item['studio'])
        
        #rating
        rating = session.query(Rating).filter_by(rating=item['rating']).first()
        if rating is not None:
            movie.rating = rating
        else:
            movie.rating = Rating(rating=item['rating'])

        #release_date
        release_date = session.query(ReleaseDate).filter_by(release_date=item['release_date']).first()
        if release_date is not None:
            movie.release_date = release_date
        else:
            movie.release_date = ReleaseDate(release_date=item['release_date'])


        movie_exists = session.query(Movie).filter_by(title=item['title']).first() is not None

        if movie_exists:
            logging.info(f'Item {movie} is in db')
            return item
        else:
            try:
                session.add(movie)
                session.commit()
                logging.info(f'Item {movie} stored in db')
            except:
                logging.info(f'Failed to add {movie} to db')
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