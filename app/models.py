from dataclasses import dataclass


@dataclass
class Member:
    name: str
    email: str
    DOB: str
    password: str


class DB:
    def __init__(self):
        self.members = []

    def drop_all(self):
        self.members.clear()

    def create_all(self):
        return None


db = DB()
