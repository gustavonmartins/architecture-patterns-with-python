from dataclasses import dataclass


class Batch:
    def __init__(self, sku, qty, eta=0):
        self.sku = sku
        self.qty = qty
        self.matchedorders = []
        self.eta = eta

    def was_ordered_by(self, orderline):
        return orderline in self.matchedorders

    def matched(self, orderline):
        self.matchedorders.append(orderline)


@dataclass
class OrderLine:
    sku: str
    qty: int
    ref: str


def allocate(orderline, batch):
    if isinstance(batch, list):
        batches_with_enough = [
            b for b in batch if (b.qty >= orderline.qty and b.sku == orderline.sku)
        ]
        earliest_batch = sorted(batches_with_enough, key=lambda x: x.eta)[0]

        return allocate(orderline, earliest_batch)

    else:
        if batch.was_ordered_by(orderline):
            return
        if orderline.qty <= batch.qty:
            batch.matched(orderline)
            batch.qty -= orderline.qty
