from typing import Dict
from models.item import Item
import uuid
from models.model import Model
from models.user import User
from dataclasses import dataclass,field
from libs.mailgun import Mailgun

"""
NOTE :

Dataclasses help us to define neater init , repr , equation and hashing functions for a class

"""


@dataclass(eq=False) # switch off comparing two alerts and it will generate an error
class Alert(Model):
    collection : str = field(init=False,default="alerts")
    item_id : str
    name: str
    price_limit : float
    user_email : str
    _id : str = field(default_factory=lambda : uuid.uuid4().hex)

    def __post__init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id" : self._id ,
            "name" : self.name,
            "item_id" : self.item_id,
            "price_limit" : self.price_limit,
            "user_email" : self.user_email
        }

    def load_item_price(self) -> float:
        self.__post__init__()
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        self.__post__init__()
        self.item.load_price()
        if self.item.price < self.price_limit:
            print(Mailgun.send_mail([self.user_email], f"Notification for {self.name}", f"Item {self.name} has reached below the price limit {self.price_limit}! \n Latest Price : {self.item.price}.Go to this address to check your item : {self.item.url}",
                                    f"<p>Item {self.name} has reached below the price limit {self.price_limit}! \n Latest Price : {self.item.price}.Click <a href ='{self.item.url}'>here</a> to check it out</p>"))
            print(f"Item {self.item} has reached below the price limit {self.price_limit}! \n Latest Price : {self.item.price}")
