from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


TEMP_USERNAME = "User1"
TEMP_FIRSTNAME = "User"
TEMP_LASTNAME = "One"

engine = create_engine("sqlite:///:memory:", echo=True)
_Session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

class Session():
    """Context manager for interacting with the DB"""

    def __init__(self):
        self.session = _Session()

    def __enter__(self):
        return self.session

    def __exit__(self, type, value, traceback):
        self.session.commit()
        self.session.close()


class User(Base):
    """Store data about the user (mostly going to by used by the UI once auth is implemented)"""
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    username = Column("username", String, unique=True)


class Store(Base):
    """Store data about the stores that the customers use. Since users could have different stores, reference them by id"""
    __tablename__ = "store"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, unique=True)


class Item(Base):
    """The actual items that will go into a users cart. If there are multiple stores, one entry per store gets made"""
    __tablename__ = "item"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    store_id = Column("store_id", Integer, ForeignKey("store.id"))
    description = Column("description", String)
    price = Column("price", Float)
    aisle = Column("aisle", Integer)


def make_user(username: str, firstname: str, lastname: str) -> User:
    """Checks if a user exists. If so, does not create. If it does not, creates the user"""
    with Session() as session:
        users = session.query(User).filter_by(username=username).all()
        if len(users) > 0:
            print(f"User {username} already exists, not creating")
            return users[0]
        user = User(username=username, first_name=firstname, last_name=lastname)
        session.add(user)
        return user


def _make_fake_user():
    user = make_user(TEMP_USERNAME, TEMP_FIRSTNAME, TEMP_LASTNAME)
    return user


def get_fake_user():
    return _make_fake_user()


def make_store(name: str) -> Store:
    with Session() as session:
        stores = session.query(Store).filter_by(name=name).all()
        if len(stores) > 0:
            print(f"Store {name} already exists, not creating")
            return stores[0]
        store = Store(name=name)
        session.add(store)
        return store


def ensure_stores(stores: list[str]) -> dict:
    """Given a list of store names, ensure they exist in the DB. Returns a mapping of name: id for the purposes of item creation"""
    mapping = dict()
    for store in stores:
        store_obj = make_store(store)
        mapping[store] = store_obj.id
    return mapping


def add_item(name: str, description: str, price: float, aisle: int, store_name: str, store_mappings: dict) -> Item:
    with Session() as session:
        store_id = store_mappings.get(store_name)
        items = session.query(Item).filter_by(name=name, store_id=store_id).all()
        if len(items) > 0:
            print("item already exists at store, not creating")
            return items[0]
        item = Item(name=name, description=description, price=price, store_id=store_id, aisle=aisle)
        session.add(item)
        return item

Base.metadata.create_all(bind=engine)
