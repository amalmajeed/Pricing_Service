from typing import Dict
import pymongo
import os
#import re

class Database(object):
    # RE = re.compile(r'.*:[1-9]+')
    # URI = RE.match(os.environ.get('MONGOLAB_URI')).group(0)
    # DATABASE = pymongo.MongoClient(URI).get_database('heroku_jnzbgb2c')
    URI = os.environ.get('MONGODB_URI')
    #URI = 'mongodb://amalmajeed:Godblessus786@ds151817.mlab.com:51817'
    DATABASE = pymongo.MongoClient(URI).get_default_database()

    @staticmethod
    def insert(collection : str , data : Dict):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection: str, query: Dict)->pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def update(collection : str , query : Dict , data : Dict)->None:
        Database.DATABASE[collection].update(query , data , upsert = True)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].remove(query)
