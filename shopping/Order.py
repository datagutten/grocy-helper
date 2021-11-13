import datetime
from typing import List

from .OrderLine import OrderLine


class Order:
    date: datetime.date
    identifier: str
    lines: List[OrderLine] = []

    def __init__(self, date: datetime.date = None, identifier=None):
        self.date = date
        self.identifier = identifier

    def add_line(self, line: OrderLine):
        self.lines.append(line)
