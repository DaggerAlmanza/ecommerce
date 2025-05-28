from sqlalchemy.orm import sessionmaker

from app.database.models import engine


Session = sessionmaker(bind=engine)
session = Session()
