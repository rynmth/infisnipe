from discord import Asset
from datetime import datetime


class Snipe:
    def __init__(self) -> None:
        self.name : str
        self.discriminator : str
        self.avatar : Asset
        self.content : str
        self.channel : str
        self.date : datetime


class EditSnipe:
    def __init__(self) -> None:
        self.name : str
        self.discriminator : str
        self.avatar : Asset
        self.content_before : str
        self.content_after : str
        self.channel : str
        self.date : datetime
