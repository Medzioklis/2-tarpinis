from product import Product

def create_product_from_input():
    id = input("Įveskite prekės ID: ")
    name = input("Įveskite prekės pavadinimą: ")
    description = input("Įveskite prekės aprašymą: ")
    price = float(input("Įveskite prekės kainą: "))
    quantity = int(input("Įveskite užsakytą kiekį: "))
    stock_left = int(input("Įveskite sandėlio likutį: "))

    return Product(id, name, description, price, quantity, stock_left)