from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Posts, User


from config import dbdir

# Creating an engine to connect to the database
engine = create_engine(f'sqlite:///{dbdir}')

# Creating a session
Session = sessionmaker(bind=engine)
session = Session()

# Deleting records with an empty `text` field
session.query(Posts).filter(Posts.User_id == 4).delete(synchronize_session=False)

# Commit changes to the database
session.commit()