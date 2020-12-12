
class Batch:
    def __init__(self, sku, qty):
        self.sku = sku
        self.qty = qty
        self.matchedorders = []

    def was_ordered_by(self, orderline):
        return orderline in self.matchedorders

    def matched(self, orderline):
        self.matchedorders.append(orderline)


class OrderLine:
    def __init__(self, sku, qty, ref):
        self.sku = sku
        self.qty = qty
        self.ref = ref
