from models.model import Model
from typing import Dict
import uuid
import re
from dataclasses import dataclass,field

"""
NOTE :

Dataclasses help us to define neater init , repr , equation and hashing functions for a class

"""

@dataclass(eq=False)
class Store(Model):
    collection : str = field(init=False,default="stores")
    name : str
    url_prefix : str
    tag_name : str
    query: Dict
    _id: str = field(default_factory=lambda : uuid.uuid4().hex)

    def json(self) -> Dict :
        return {"_id": self._id ,
                "name": self.name ,
                'url_prefix': self.url_prefix ,
                "tag_name": self.tag_name,
                "query": self.query
                }
    """"
     "get_by_id" already present in Model superclass
     "save_to_mongo" already present in Model superclass
     "remove_from_mongo" already present in Model superclass
     "all" already present in Model superclass
     "find_one_by" already present in Model superclass
     "find_many_by" already present in Model superclass
    """

    @classmethod
    def get_by_name(cls, store_name : str) -> "Store":
        return cls.find_one_by("name" , store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix : str) -> "Store":
        url_regex = {"$regex" : "^{}".format(url_prefix)}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url : str) -> "Store":
        """
        Return a store from a given URL like https://www.blabla.com/bla/p1233p33.html
        :param url: The items URL
        :return: Store which the item is sold in
        """
        pattern = re.compile(r"https?://.*?/")  # A URL PREFIX REGEX PATTERN
        match = pattern.search(url) # LIST OF MATCHED GROUPS FOR A PREFIX PATTERN
        url_prefix = match.group(0)
        return cls.get_by_url_prefix(url_prefix)
