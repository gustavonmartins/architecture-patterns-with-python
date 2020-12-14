import models


def test_mapping():
    from repository import OrderLineRepository
    from db import create_db_and_mapper

    """Tests if SQL Alchemy traditional mapping was done properly by checking if file inserted into DB really corresponds to target model"""

    create_db_and_mapper()
    myorderline = models.OrderLine(sku="blue t shirt", qty=20, ref="ordereed from king")
    repo = OrderLineRepository()
    repo.add(myorderline)

    out = repo.list()

    assert out == [myorderline]
