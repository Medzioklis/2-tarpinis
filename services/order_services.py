from models.product_class import Product, db
from models.cart_class import Cart
from sqlalchemy import select

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