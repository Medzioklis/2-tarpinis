class Product:
    def __init__(self, id, name, description, price, quantity, stock_left):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.stock_left = stock_left

    def __str__(self):
        return f"{self.name} (ID: {self.id}) – {self.description} | {self.price} EUR | Užsakyta: {self.quantity}, Sandėlyje: {self.stock_left}"
