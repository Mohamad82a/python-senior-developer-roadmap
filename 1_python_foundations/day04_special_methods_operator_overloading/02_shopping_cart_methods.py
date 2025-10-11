class ShoppingCart:
    """Implement len() and string representation"""
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return f"Cart({', '.join(self.items)})"

cart = ShoppingCart()
cart.add("Apple")
cart.add("Banana")
print(len(cart))  # 2
print(cart)       # Cart(Apple, Banana)
