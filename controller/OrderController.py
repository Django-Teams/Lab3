from forms.OrderForm import OrderForm
from model.Order import Order
from service.OrderService import OrderService


class OrderController:
    def make(self, form: OrderForm, service: OrderService):
        order = Order(ser)