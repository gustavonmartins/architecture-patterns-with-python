from models import Batch, OrderLine, allocate


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


def test_allocate_prefers_warehouse():
    batch_warehouse = Batch(sku="SMALL-TABLE", qty=20)
    batch_shipping = Batch(sku="SMALL-TABLE", qty=20, eta=10)
    order_line = OrderLine(ref="bla", sku="SMALL-TABLE", qty=20)
    allocate(order_line, [batch_shipping, batch_warehouse])

    assert batch_warehouse.qty == 0
    assert batch_shipping.qty == 20


def test_allocate_quickest_warehouse():
    batch_warehouse_slow = Batch(sku="SMALL-TABLE", qty=20, eta=10)
    batch_shipping_unavaiable = Batch(sku="SMALL-TABLE", qty=2, eta=1)
    batch_shipping_ok = Batch(sku="SMALL-TABLE", qty=20, eta=5)
    order_line = OrderLine(ref="bla", sku="SMALL-TABLE", qty=20)
    allocate(
        order_line, [batch_warehouse_slow, batch_shipping_unavaiable, batch_shipping_ok]
    )
    assert batch_warehouse_slow.qty == 20
    assert batch_shipping_unavaiable.qty == 2
    assert batch_shipping_ok.qty == 0
