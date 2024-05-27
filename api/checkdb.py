# init_db.py

from api.database import engine, Base
from api.models import Blog


def create():
    Base.metadata.create_all(bind=engine)

