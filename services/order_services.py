from models.product_class import Product, db
from models.user_class import User
from models.cart_class import Cart
from models.oder_class import Order, OrderItem
from sqlalchemy import select, update

# gauname vartotojo krepšelio turinį
def get_cart_contents(user_id):
    try:
        # Atliekame sujungimą tarp cart_items ir products lentelių
        cart_c = select(Product, Cart.quantity).join(Cart, Product.id == Cart.product_id).where(Cart.user_id == user_id)
        cart_content = db.session.execute(cart_c).all()
        
        # Sukuriame patogesnį objektų sąrašą
        items = []
        total = 0
        for product, quantity in cart_content:
            items.append({'product': product, 'quantity': quantity})
            total += product.price * quantity
        
        return items, total
    except Exception as e:
        print(f"Klaida gaunant krepšelio turinį: {e}")
        return [], 0    # jei klaida grazinam tuscia sarasa ir total 0
    
# Pridedam prekę į vartotojo krepšelį
def add_product_to_cart(user_id, product_id, quantity=1):
    try:
        # Patikriname, ar prekė jau yra krepšelyje
        row = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
        existing_item = db.session.scalars(row).first()
        
        if existing_item:
            # Jei yra, padidiname kiekį
            new_quantity = existing_item.quantity + quantity
            row = db.update(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id).values(quantity=new_quantity)
        else:
            # Jei nėra, įterpiame naują įrašą
            row = db.insert(Cart).values(user_id=user_id, product_id=product_id, quantity=quantity)
            
        db.session.execute(row)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

# Iš krepšelio turinio sukuriam uzsakyma    
def create_order_from_cart(user_id):
    
    # tikrinam ar krepselio deleted nera True
    cart = db.session.scalars(db.select(Cart).where(Cart.user_id == user_id, Cart.deleted == True )).first()
    if cart:
        raise ValueError("Krepšelis ištrintas")

    user = db.session.get(User, user_id)
    cart_items_list, total_price = get_cart_contents(user_id)

    if not cart_items_list:
        raise ValueError("Krepšelis tuščias.")
    if user.user_balance < total_price:
        raise ValueError("Nepakanka lėšų balanse.")

    try:
        # Nuskaičiuojame pinigus iš vartotojo balanso
        user.user_balance -= total_price
        
        # Sukuriame užsakymą
        order = Order(user_id=user_id, total_price=total_price)
        db.session.add(order)
        
        # Perkeliame prekes iš krepšelio į užsakymo prekes
        for item in cart_items_list:
            product = item['product']
            quantity = item['quantity']
            
            # Patikriname likutį
            if product.stock < quantity:
                raise ValueError(f"Nepakankamas prekės '{product.name}' likutis.")
            
            product.stock -= quantity
            
            order_item = OrderItem(
                order=order, 
                product_id=product.id, 
                quantity=quantity, 
                price_per_unit=product.price
            )
            db.session.add(order_item)

        # Išvalome krepšelį (pakeiciam deleted True)
        row = (update(Cart).where(Cart.user_id == user_id).values(deleted=True))
        db.session.execute(row)
        db.session.commit()
        return order
    except Exception as e:
        db.session.rollback()
        raise e
 