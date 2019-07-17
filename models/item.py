from typing import Dict
import re
import requests
from bs4 import BeautifulSoup
import uuid
from models.model import Model
from dataclasses import dataclass,field

"""
NOTE :

Dataclasses help us to define neater init , repr , equation and hashing functions for a class

"""

@dataclass(eq=False)
class Item(Model):
    collection :str = field(init=False,default="items")
    url : str
    tag_name : str = field(repr=False)
    query : Dict = field(repr=False)
    price : float = field(default=None)
    _id : str = field(default_factory=lambda : uuid.uuid4().hex)

    def load_price(self):
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()
        pattern = re.compile(r'(\d+,?\d*\.\d\d)')
        match = pattern.search(string_price)
        found_price = match.group(1).replace(',', '')
        self.price = float(found_price)

    def json(self) -> Dict:
        return {"_id": self._id ,
                'url': self.url ,
                "tag_name": self.tag_name,
                "price": self.price,
                "query": self.query
                }
