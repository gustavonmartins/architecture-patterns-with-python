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


def get_db():
    """Returns a database session"""
    from sqlalchemy.orm import sessionmaker

    engine = get_engine()

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    return db


def create_mapper():
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


def test_mapping():
    """Tests if SQL Alchemy traditional mapping was done properly by checking if file inserted into DB really corresponds to target model"""

    create_mapper()
    db = get_db()

    myorderline = models.OrderLine(sku="blue t shirt", qty=20, ref="ordereed from king")

    db.add(myorderline)
    db.flush()

    out = db.query(models.OrderLine).one()

    db.rollback()
    db.close()

    assert out == myorderline
