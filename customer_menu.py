# CUSTOMER MENU

def view_products():
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT id, name, price, quantity FROM products WHERE quantity > 0"
    cursor.execute(query)
    products = cursor.fetchall()
    db.close()

    if products:
        print("\nAvailable Products: ")
        for prod in products:
            print(f"Product ID: {prod[0]}, Product Name: {prod[1]}, Product Price: {prod[2]}, Quantity: {prod[3]}")
    else:
        print("No products available!")
    print("-"*50)

def place_order():

    view_products()

    product_id = int(input("\nEnter the Product ID you want to buy: "))
    quantity = int(input("Enter the quantity: "))

    db = connect_db()
    cursor = db.cursor
    query = "SELECT name, price, quantity FROM products WHERE id = {}"
    cursor.execute(query.format(product_id))
    product = cursor.fetchone()

    if not product:
        print("Invalid Product ID")
        db.close()
        return

    product_name, product_price, available_quantity = product
    if quantity > available_quantity:
        print(f"Only{ available_quantity} units of {product_name} are available.")
        db.close()
        return

    new_quantity = available_quantity - quantity
    cursor.execute("UPDATE products SET quantity = {} WHERE id = {}".format(new_quantity, product_id))

    cursor.execute(
        "INSERT INTO sales (product_id, quantity_sold) VALUES ({}, {})".format(product_id, quantity)
    )
    sale_id = cursor.lastrowid

    total_amount = product_price * quantity
    cursor.execute(
        "INSERT INTO invoices (sales_id, total_amount) VALUES ({}, {})".format(sale_id, total_amount)
    )

    db.commit()
    db.close()

    print(f"Order placed successfully for {quantity} unit(s) of {product_name}. Total Amount: ₹{total_amount}")

    print("-"*50)
