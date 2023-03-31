from service.OrderService import OrderService

# GET DISHES TO DISPLAY

os = OrderService()
dishes = os.get_dishes()

# MAKE AN ORDER
# SET ATTRIBUTE 'count' with count of dish

dish = dishes[0]  # Dish to order
dish.count = 2  # Order 2 servings
my_order = [dish]  # Insert ordered dishes into the list

os = OrderService()
order = os.order(my_order)  # Make an order and get order details
