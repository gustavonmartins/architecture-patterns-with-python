import models


def get_engine():
    """Creates a new SQLAlchemy Engine. Is useful later for metadata"""
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base

    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    return engine


def create_db_and_mapper():

    """Creates a mapper from desired model into SQLAlchemy"""
    from sqlalchemy.orm import (
        mapper,
        clear_mappers,
    )

    from sqlalchemy import (
        MetaData,
        Table,
        Column,
        Integer,
        String,
    )

    metadata = MetaData()
    metadata.clear()
    order_lines = Table(
        "order_lines",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("sku", String),
        Column("qty", Integer),
        Column("ref", String),
    )
    metadata.create_all(get_engine())

    clear_mappers()
    mapper(models.OrderLine, order_lines)


def get_db():
    """Returns a database session"""
    from sqlalchemy.orm import sessionmaker

    engine = get_engine()

    SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
    )
    db = SessionLocal()

    return db


class OrderLineRepository:
    def add(self, batch):
        db = get_db()
        db.add(batch)
        db.commit()

    def get(self, ref):
        db = get_db()
        return db.query(models.OrderLine).filter(models.OrderLine.ref == ref).one()

    def list(self):
        db = get_db()
        return db.query(models.OrderLine).all()
