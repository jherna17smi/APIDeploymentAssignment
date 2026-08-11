from dataclasses import dataclass


@dataclass
class Member:
    name: str
    email: str
    DOB: str
    password: str


@dataclass
class Mechanic:
    id: int
    name: str
    specialty: str


@dataclass
class Customer:
    id: int
    name: str
    phone: str


@dataclass
class ServiceTicket:
    id: int
    customer_id: int
    mechanic_id: int
    issue: str
    status: str = "open"


@dataclass
class InventoryItem:
    id: int
    name: str
    quantity: int
    price: float


class DB:
    def __init__(self):
        self.members = []
        self.mechanics = []
        self.customers = []
        self.service_tickets = []
        self.inventory = []

    def drop_all(self):
        self.members.clear()
        self.mechanics.clear()
        self.customers.clear()
        self.service_tickets.clear()
        self.inventory.clear()

    def create_all(self):
        return None


db = DB()
