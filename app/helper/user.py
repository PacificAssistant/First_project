from sqlalchemy import create_engine, MetaData

from app.models import User
from config import dbdir

engine = create_engine(f'sqlite:///{dbdir}')
meta = MetaData()

# Initialize all models (and tables) based on metadata
meta.create_all(engine, tables=[User.__table__])