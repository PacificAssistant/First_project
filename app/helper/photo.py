from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import dbdir


def save_photo_to_db(filename, image_data):
    conn = create_engine(f'sqlite:///{dbdir}')
    Session = sessionmaker(bind=conn)
    session = Session()
    # Deleting records with an empty `text` field
    session.execute('')

    # Commit changes to the database
    session.commit()
