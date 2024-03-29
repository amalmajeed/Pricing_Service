from abc import ABCMeta , abstractmethod
from common.database import Database
from typing import Dict, List,TypeVar , Type , Union


T = TypeVar('T' , bound='Model' )

# ABSTRACT CLASS DEFINITION

class Model(metaclass=ABCMeta):
    collection : str
    _id : str ## The instance property self._id overrides it

    def __init__(self , *args , **kwargs):
        pass

    def save_to_mongo(self):
        Database.update(self.collection, {"_id":self._id} , self.json() ) # YET TO ADD UPDATE

    def remove_from_mongo(self):
        Database.remove( self.collection , {"_id":self._id} )

    @abstractmethod
    def json(self) -> Dict :
        raise NotImplementedError

    @classmethod
    def get_by_id(cls : Type[T], _id: str) -> T:
        return cls.find_one_by( "_id" , _id )

    @classmethod
    def all(cls : Type[T]) -> List[T]:
        elements_from_db = [cls(**element) for element in Database.find(cls.collection, {})]
        return elements_from_db

    @classmethod
    def find_one_by(cls : Type[T] ,attribute : str, value : Union[str,Dict]) -> T:
        x = Database.find_one(cls.collection , {attribute : value})
        return cls(**x[0])

    @classmethod
    def find_many_by(cls : Type[T] ,attribute : str, value : str) -> List[T]:
        elements_from_db = [cls(**element) for element in Database.find(cls.collection, {attribute: value})]
        return elements_from_db
