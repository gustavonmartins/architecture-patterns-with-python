from models import Batch, OrderLine


def test_allocation():
    batch = Batch(sku="SMALL-TABLE", qty=20)
    order_line = OrderLine(sku="SMALL-TABLE", qty=2, ref="some order")
    allocate(order_line, batch)
    assert batch.qty == 18


def test_allocation_not_enough():
    batch = Batch(sku="BLUE-CUSHION", qty=1)
    order_line = OrderLine(sku="BLUE-CUSHION", qty=2, ref="some order")
    allocate(order_line, batch)
    assert batch.qty == 1


def test_cant_allocate_twice():
    batch = Batch(sku="SMALL-TABLE", qty=20)
    order_line = OrderLine(ref="some orderline", sku="SMALL-TABLE", qty=2)
    allocate(order_line, batch)
    allocate(order_line, batch)
    assert batch.qty == 18


def allocate(orderline, batch):
    if batch.was_ordered_by(orderline):
        return
    if orderline.qty <= batch.qty:
        batch.matched(orderline)
        batch.qty -= orderline.qty
