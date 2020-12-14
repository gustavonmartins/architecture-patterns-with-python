from db import get_db
import models


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
