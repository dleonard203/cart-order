from context import cart_order
from cart_order.data import datastore


def test_make_user():
    u = datastore.make_user("dleonard", "dave", "leonard")
    assert u.first_name == "dave"
    assert u.last_name == "leonard"
    assert u.username == "dleonard"
