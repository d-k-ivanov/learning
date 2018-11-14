#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:  # the Context

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())

def FidelityPromo(order):  # first Concrete Strategy
    """5% discount for customers with 1000 or more fidelity points"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0


def BulkItemPromo(order):  # second Concrete Strategy
    """10% discount for each LineItem with 20 or more units"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount


def LargeOrderPromo(order):  # third Concrete Strategy
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0

def BestPromo(order):
    """Select the best discount program"""
    promos = [globals()[name] for name in globals() if name.endswith('Promo') and name != 'BestPromo']
    return max(promo(order) for promo in promos)

if __name__ == '__main__':
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    cart = [LineItem('banana', 4, .5), LineItem('apple', 10, 1.5), LineItem('watermellon', 5, 5.0)]
    banana_cart = [ LineItem('banana', 30, .5), LineItem('apple', 10, 1.5)]
    long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]

    print('---------------------------------------------------------------------------')

    print(globals())

    print('---------------------------------------------------------------------------')

    print(Order(joe, cart, FidelityPromo))
    print(Order(ann, cart, FidelityPromo))
    print(Order(joe, banana_cart, BulkItemPromo))
    print(Order(joe, long_order, LargeOrderPromo))
    print(Order(joe, cart, LargeOrderPromo))

    print('---------------------------------------------------------------------------')

    print(Order(joe, long_order, BestPromo))
    print(Order(joe, banana_cart, BestPromo))
    print(Order(ann, cart, BestPromo))

    print('---------------------------------------------------------------------------')

