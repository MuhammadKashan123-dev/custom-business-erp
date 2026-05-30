from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
DATABASE_URL="postgresql://postgres:pakistan057@localhost/erp_db"
engine = create_engine(DATABASE_URL)
sessionlocal = sessionmaker(autoflush=False , autocommit = False ,bind=engine)
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)