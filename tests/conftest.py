import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.registry import mapper_registry

@pytest.fixture(scope='module')
def engine():
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    mapper_registry.metadata.create_all(bind=engine)
    yield engine
    mapper_registry.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
