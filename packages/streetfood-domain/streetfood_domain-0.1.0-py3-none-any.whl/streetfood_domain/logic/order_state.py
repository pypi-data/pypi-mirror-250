from __future__ import annotations

class OrderHandler:
    def __init__(self, successor=None):
        self.successor = successor
        self.order = None

    def handle_order(self, order_data):
        if self.successor:
            self.successor.handle_order(order_data)

class NewOrderHandler(OrderHandler):
    def handle_order(self, order_data):
        if order_data.get("cart"): 
            super().handle_order(order_data)
        raise Exception("First add items to cart")

class ContactOrderHandler(OrderHandler):
    def handle_order(self, order_data):
        if order_data.get("contacts"):
            super().handle_order(order_data)
        raise Exception("First add contacts")

class PayedOrderHandler(OrderHandler):
    def handle_order(self, order_data):
        if order_data.get("payment_callbacks"):
            super().handle_order(order_data)
        raise Exception("First payed")
        

if __name__ == "__main__":
    order = {
        "cart_data": {},
        "contacts": [],
        "payment_callbacks": [],
        "ready": False,
        "done": False,
    }

    handler_chain = NewOrderHandler(ContactOrderHandler(PayedOrderHandler()))
    handler_chain.handle_order(order)
