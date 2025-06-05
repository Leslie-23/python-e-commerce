import mysql.connector
from .databaseConfig import get_db_config_data
from werkzeug.security import generate_password_hash, check_password_hash

config = get_db_config_data()


def get_mysql_connection():
    return mysql.connector.connect(**config)


# all of the following functions will be used to communicate with the database

# this function is used to generate a unique custom ID
# always remember to insert id's in numerical order
# the following functions will be used to generate uniqe ID's
def gen_custID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id FROM registered_user ORDER BY user_id DESC LIMIT 1")
    res = cur.fetchall()
    conn.close()
    # return the number which is 1 greater than the last entry
    if res:
        last_id = res[0][0]
        # Return the number which is 1 greater than the last entry
        return last_id + 1
    else:
        # If there are no results (e.g., the table is empty), start with 1
        return 0


# this function generates an order ID
def gen_orderID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT order_id FROM order_item ORDER BY order_id DESC LIMIT 1")
    res = cur.fetchall()
    conn.close()
    # return the number which is 1 greater than the last entry
    if res:
        last_id = res[0][0]
        # Return the number which is 1 greater than the last entry
        return last_id + 1
    else:
        # If there are no results (e.g., the table is empty), start with 1
        return 0


# this function generates ID for a single order item
def gen_order_item_ID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT order_item_id FROM order_item ORDER BY order_item_id DESC LIMIT 1")
    res = cur.fetchall()
    conn.close()
    # return the number which is 1 greater than the last entry
    if res:
        last_id = res[0][0]
        # Return the number which is 1 greater than the last entry
        return last_id + 1
    else:
        # If there are no results (e.g., the table is empty), start with 1
        return 0


# this function generates ID for a delivary module
def gen_delivery_ID():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT delivery_module_id FROM delivery_module ORDER BY order_item_id DESC LIMIT 1")
    res = cur.fetchall()
    conn.close()
    # return the number which is 1 greater than the last entry
    if res:
        last_id = res[0][0]
        # Return the number which is 1 greater than the last entry
        return last_id + 1
    else:
        # If there are no results (e.g., the table is empty), start with 1
        return 0


def get_stock_count(variant_id):
    conn = get_mysql_connection()
    cur = conn.cursor()
    # Define the query with a placeholder for variant_id
    query = "SELECT stock_count FROM inventory WHERE variant_id = %s"

    # Execute the query with the provided variant_id
    cur.execute(query, (variant_id,))

    # Fetch the result
    result = cur.fetchone()

    print(result)

    if result:
        stock_count = result[0]
        return stock_count
    else:
        return None


# this function will be used to add a new user to the database
# it will return true if we are able to add a new user
def add_user(data):
    conn = get_mysql_connection()
    cur = conn.cursor()
    username = data["username"]
    # need to check if the username already exists
    cur.execute("SELECT * FROM registered_user WHERE username=%s", (username,))
    result = cur.fetchall()
    # if we already have a registered user from that username then we can't add another user
    if len(result) != 0:
        return False
    customer_id = gen_custID()
    tup = (customer_id, data["email"], generate_password_hash(
        data["password"], method='pbkdf2:sha256'), data["username"],)

    cur.execute(
        "INSERT INTO registered_user (user_id,email, password, username) VALUES (%s, %s, %s, %s)", tup)

    conn.commit()
    conn.close()
    return True


# this function is used to authenticate the user

def auth_user(data):
    conn = get_mysql_connection()
    cur = conn.cursor()
    # extract the data from the data object
    username = data["username"]
    password = data["password"]

    # check if the user is already in the database
    cur.execute(
        "SELECT user_id,username,password FROM registered_user WHERE username=%s", (username,))

    result = cur.fetchall()
    print("hello mofossssssssssssssssssssssssssss", result[0][2])
    conn.close()
    if not check_password_hash(result[0][2], password):
        return False
    return result[0]


def search_product(search_query):
    conn = get_mysql_connection()
    cur = conn.cursor()

    sql_query = "SELECT * FROM product WHERE title LIKE %s"
    cur.execute(sql_query, ("%" + search_query + "%",))

    # Fetch the matching products
    matching_products = cur.fetchall()

    return matching_products


# we can use the below function to get all the main products related to a given category
# ex :- when we pass electronics as the parameter to this function we are fetching all the electronics sub products from the database
def get_categories(category):
    conn = get_mysql_connection()
    cur = conn.cursor()
    # select all the subproducts related to the given category
    # Execute the SQL query
    query = """
            SELECT Category.category_name, Category.category_image,Category.category_id
            FROM Category
            WHERE Category.parent_category_id = (
                SELECT category_id FROM Category WHERE category_name = %s
            )
        """

    # Fetch the results
    cur.execute(query, (category,))
    results = cur.fetchall()

    return results


# this function will be used to get products from the database
def get_products_from_database(id):
    # use try catch statements to handle errors
    conn = get_mysql_connection()
    cur = conn.cursor()
    # query = "SELECT * FROM products WHERE category_id = %s", (id,)
    # cur.execute(query, (id,))

    query = "SELECT product.title,product.description,product.weight,product.product_image,product.product_id FROM product WHERE category_id = %s"
    cur.execute(query, (id,))  # Pass the integer id as a parameter

    results = cur.fetchall()
    return results


def get_product_info():
    conn = get_mysql_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    return products


def update_cart(user_id, variant_id, quantity):
    conn = get_mysql_connection()
    cur = conn.cursor()
    print("hello world")
    # Define the SQL statement using the INSERT ... ON DUPLICATE KEY UPDATE syntax
    # Define the SQL statement with an alias for VALUES
    query = """
        INSERT INTO cart_item (user_id, variant_id, quantity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE quantity = cart_item.quantity
        """
    # Execute the SQL statement with the provided user_id, variant_id, and quantity
    cur.execute(query, (user_id, variant_id, quantity))

    conn.commit()
    conn.close()
    return


def get_single_product_info(product_id):
    try:
        conn = get_mysql_connection()
        with conn.cursor() as cur:
            # Run the query to get product details based on the product_id
            cur.execute("SELECT * FROM product WHERE id = %s", (product_id,))
            details = cur.fetchone()  # Use fetchone since we expect a single result
        return details
    except Exception as e:
        # Handle the exception (e.g., log the error or return an error message)
        return None  # Return None or an appropriate error indicator


def get_varient_info(product_id):
    conn = get_mysql_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT variant.name,variant.price,variant.custom_attrbutes,variant.variant_image,variant.variant_id FROM variant WHERE product_id = %s",
            (product_id,))
        result = cur.fetchall()

    return result


def update_order_items(order_items, is_signedin, user_id):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    # create a transaction
    # inventry should be updated
    # we should handle this separately for logged in users and guest users

    # for a guest user his session cart should be emptied and for a logged in user his cart_item table should be updated
    # cart table should be inserted with a new entry
    try:
        # Start a transaction
        cursor.execute("START TRANSACTION")

        if is_signedin:
            order_item_id, order_id, variant_id, quantity, price = order_items[0]

            # INSERT INTO order_item
            insert_query = "INSERT INTO order_item (order_item_id, order_id, variant_id, quantity, price) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (order_item_id,
                           order_id, variant_id, quantity, price))

            # DELETE FROM cart_item
            delete_query = "DELETE FROM cart_item WHERE user_id = %s"
            cursor.execute(delete_query, (user_id,))

            # Reduce stock count in inventory
            update_query = "UPDATE inventory SET stock_count = stock_count - %s WHERE variant_id = %s"
            cursor.execute(update_query, (quantity, variant_id))

        # Commit the transaction
        cursor.execute("COMMIT")

    except Exception as e:
        # Handle any exceptions and possibly roll back the transaction
        cursor.execute("ROLLBACK")
        raise e
    finally:
        conn.close()


def update_order_table(order_table_details):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    try:
        order_id, date, delivery_method, payment_method, user_id = order_table_details

        insert_query = "INSERT INTO orders (order_id, date, delivery_method, payment_method, user_id) VALUES (%s, %s, %s, %s, %s)"

        cursor.execute(insert_query, (order_id, date,
                       delivery_method, payment_method, user_id))

        conn.commit()

    except mysql.connector.Error as err:
        # Handle any potential errors here
        print("Error: {}".format(err))


def get_cart(custID):
    conn = get_mysql_connection()
    cur = conn.cursor()

    sql_query = """
    SELECT
        ci.quantity AS quantity,
        v.name AS name,
        v.price AS price,
        v.variant_image AS variant_image,
        p.title AS title,
        v.variant_id as variant_id
    FROM
        cart_item AS ci
    JOIN
        variant AS v ON ci.variant_id = v.variant_id
    JOIN
        product AS p ON v.product_id = p.product_id
    WHERE
        ci.user_id = %s
    """
    cur.execute(sql_query, (custID,))
    result = cur.fetchall()
    conn.close()
    print(result)

    return result


# this function will fetch variant details for a guest's cart
def get_guest_cart(variant_ids):
    conn = get_mysql_connection()
    cur = conn.cursor()

    # Create a list to store the results
    result = []

    # Construct the SQL query using JOIN to fetch the required columns from both tables
    query = """
    SELECT p.title, v.name, v.price, v.variant_image,v.variant_id
    FROM product AS p
    JOIN variant AS v ON p.product_id = v.product_id
    WHERE 
        v.variant_id = %s
    """

    for variant_id in variant_ids:
        # Execute the query for each variant_id
        cur.execute(query, (variant_id,))
        rows = cur.fetchall()
        for row in rows:
            result.append(row)

    return result


def update_delivary_module(module):
    conn = get_mysql_connection()
    cur = conn.cursor()

    # create a list of main cities
    main_cities = ['Colombo', 'Panadura', 'Galle', 'Kandy']
    new_id = gen_delivery_ID()
    # stock_count,destination_city,new_ID
    tup = new_id, module[2], module[1]

    # checking if the stock count is greater than zero
    if module[0] > 0:

        if (module[1] in main_cities):
            # add fibve days to the end of the tuple

            tup = tup + (5,)
            cur.execute(
                "INSERT INTO delivery_module (delivery_module_id, order_item_id, destination_city, estimated_days) VALUES (%s, %s, %s, %s)",
                tup)
        else:
            tup = tup + (7,)
            cur.execute(
                "INSERT INTO delivery_module (delivery_module_id, order_item_id, destination_city, estimated_days) VALUES (%s, %s, %s, %s)",
                tup)

    else:
        if (module[1] in main_cities):
            tup = tup + (8,)
            cur.execute(
                "INSERT INTO delivery_module (delivery_module_id, order_item_id, destination_city, estimated_days) VALUES (%s, %s, %s, %s)",
                tup)
        else:
            tup = tup + (10,)
            cur.execute(
                "INSERT INTO delivery_module (delivery_module_id, order_item_id, destination_city, estimated_days) VALUES (%s, %s, %s, %s)",
                tup)

    conn.commit()


def get_details_for_delivery_module(order_item_ids):

    conn = get_mysql_connection()
    cursor = conn.cursor()
    # Create a list to store variant names
    variant_info = []

    try:
        for order_item_id in order_item_ids:
            # SQL query to fetch variant name and estimated days for a specific order item ID
            query = """
            SELECT variant.name, delivery_module.estimated_days
            FROM order_item
            INNER JOIN variant ON order_item.variant_id = variant.variant_id
            LEFT JOIN delivery_module ON order_item.order_item_id = delivery_module.order_item_id
            WHERE order_item.order_item_id = %s
            """
            # Execute the SQL query with the current order_item_id
            cursor.execute(query, (order_item_id,))

            # Fetch the variant name and estimated days and append them to the variant_info list
            result = cursor.fetchone()
            if result:
                variant_info.append(result)

        print(variant_info)

    except Exception as e:
        print("Error:", e)

    return variant_info


def remove_from_cart(custID, prodID):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE custID=%s AND prodID=%s",
                (custID, prodID))
    conn.commit()


def Quarterly_sales(year):
    conn = get_mysql_connection()
    cur = conn.cursor()

    cur.execute(f'''CREATE VIEW year{year}orderitem AS
                    select v.price*oi.quantity as total_price , t23.date , oi.order_id, oi.variant_id
                    from order_item as oi
                    join (SELECT * FROM orders WHERE YEAR(date) = {year}) AS t23 on oi.order_id = t23.order_id
                    join variant as v on v.variant_id = oi.variant_id''')
    conn.commit()
    cur.execute(f'''select sum(total_price) as q1_price
                    from year{year}orderitem
                    where month(date) in (1,2,3);''')
    q1 = cur.fetchone()[0]
    q1 = int(q1) if q1 is not None else 0

    cur.execute(f'''select sum(total_price) as q1_price
                    from year{year}orderitem
                    where month(date) in (4,5,6);''')
    q2 = cur.fetchone()[0]
    q2 = int(q2) if q2 is not None else 0

    cur.execute(f'''select sum(total_price) as q1_price
                    from year{year}orderitem
                    where month(date) in (7,8,9);''')
    q3 = cur.fetchone()[0]
    q3 = int(q3) if q3 is not None else 0

    cur.execute(f'''select sum(total_price) as q1_price
                    from year{year}orderitem
                    where month(date) in (10,11,12);''')
    q4 = cur.fetchone()[0]
    q4 = int(q4) if q4 is not None else 0

    cur.execute(f'DROP VIEW IF EXISTS year{year}orderitem;')
    conn.commit()

    q_sale = [q1, q2, q3, q4]
    conn.close()
    return q_sale


def select_year():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute('''select distinct year(date) as year
                    from orders 
                    order by year(date) desc''')
    result = cur.fetchall()
    cur.execute('''select distinct year(date) as year
                    from orders 
                    order by year(date) desc''')
    year = cur.fetchone()[0]
    return (result, year)


def getProductQuantityList(from_year, to_year):
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute(F'''select LEFT(p.title, 20) as title, sum(oi.quantity) as quantity
                    from order_item oi
                    join orders o 
                    on o.order_id = oi.order_id
                    join variant v
                    on v.variant_id = oi.variant_id
                    join product p
                    on p.product_id = v.product_id
                    where year(date) between {from_year} and {to_year}
                    group by (p.title)''')
    result = cur.fetchall()
    product_list = []
    quantity_list = []
    for i, j in result:
        product_list.append(i)
        quantity_list.append(int(j))

    return product_list, quantity_list


def getCategoriesandOrders():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute(F'''select c.category_name,count(oi.order_id)
                from order_item as oi
                right join variant as v
                on oi.variant_id = v.variant_id 
                join product as p 
                on p.product_id = v.product_id
                right join category as c
                on c.category_id = p.category_id
                group by c.category_id,c.category_name
                order by count(oi.order_id) asc;
                ; ''')
    result = cur.fetchall()
    category = []
    orders = []
    for i, j in result:
        category.append(i)
        orders.append(j)
    return category, orders


def product_list():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute('''select product_id , title
                    from product ;
                ''')
    result = cur.fetchall()
    return result


def get_product_sales(product_id):
    conn = get_mysql_connection()
    cur = conn.cursor()

    # Parameterized SQL query
    cur.execute('''select count(oi.quantity), month(o.date)
                    from order_item as oi
                    inner join orders as o on o.order_id = oi.order_id
                    right join variant as v on v.variant_id = oi.variant_id
                    join product as p on p.product_id = v.product_id
                    where p.product_id = %s
                    group by month(o.date)
                    order by month(o.date);
                ''', (product_id,))

    result = cur.fetchall()

    # Initialize a dictionary with keys for each month (1-12) and default values of 0
    monthly_values = {month: 0 for month in range(1, 13)}

    # Update the dictionary with the actual sales data from the query
    for value, month in result:
        if month:  # Only update if month is not None
            monthly_values[month] = value

    # Convert the dictionary values to a list
    result_list = list(monthly_values.values())

    return result_list

# ==================== ADMIN FUNCTIONS ====================


def get_user_role(user_id):
    """Get user role - check if user is admin"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        # Check if user has admin role (assuming a user_roles table or is_admin column)
        # For now, we'll check if username contains 'admin' or user_id is 1
        cur.execute(
            "SELECT username FROM registered_user WHERE user_id = %s", (user_id,))
        result = cur.fetchone()
        if result and (result[0].lower() == 'admin' or user_id == 1):
            return 'admin'
        return 'user'
    except Exception as e:
        print(f"Error getting user role: {e}")
        return 'user'
    finally:
        conn.close()


def get_admin_stats():
    """Get overview statistics for admin dashboard"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        stats = {}

        # Total users
        cur.execute("SELECT COUNT(*) FROM registered_user")
        stats['total_users'] = cur.fetchone()[0]

        # Total products
        cur.execute("SELECT COUNT(*) FROM product")
        stats['total_products'] = cur.fetchone()[0]

        # Total orders
        cur.execute("SELECT COUNT(*) FROM orders")
        stats['total_orders'] = cur.fetchone()[0]

        # Total revenue
        cur.execute("SELECT SUM(oi.quantity * oi.price) FROM order_item oi")
        result = cur.fetchone()[0]
        stats['total_revenue'] = result if result else 0

        # Low stock items
        cur.execute("SELECT COUNT(*) FROM inventory WHERE stock_count < 10")
        stats['low_stock_items'] = cur.fetchone()[0]

        return stats
    except Exception as e:
        print(f"Error getting admin stats: {e}")
        return {}
    finally:
        conn.close()


def get_recent_orders(limit=10):
    """Get recent orders for admin dashboard"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT o.order_id, o.date, ru.username, COUNT(oi.order_item_id) as item_count,
               SUM(oi.quantity * oi.price) as total_amount
        FROM orders o
        LEFT JOIN registered_user ru ON o.user_id = ru.user_id
        LEFT JOIN order_item oi ON o.order_id = oi.order_id
        GROUP BY o.order_id, o.date, ru.username
        ORDER BY o.date DESC
        LIMIT %s
        """
        cur.execute(query, (limit,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting recent orders: {e}")
        return []
    finally:
        conn.close()


def get_all_users():
    """Get all users for admin management"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT ru.user_id, ru.username, ru.email, 
               COUNT(o.order_id) as order_count,
               COALESCE(SUM(oi.quantity * oi.price), 0) as total_spent
        FROM registered_user ru
        LEFT JOIN orders o ON ru.user_id = o.user_id
        LEFT JOIN order_item oi ON o.order_id = oi.order_id
        GROUP BY ru.user_id, ru.username, ru.email
        ORDER BY ru.user_id
        """
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting all users: {e}")
        return []
    finally:
        conn.close()


def toggle_user_admin_role(user_id):
    """Toggle user admin role"""
    # For now, this is a placeholder since we don't have a proper role system
    # In a real system, you'd update a roles table or is_admin column
    try:
        return True
    except Exception as e:
        print(f"Error toggling user role: {e}")
        return False


def get_all_products_admin():
    """Get all products for admin management"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT p.product_id, p.title, p.description, c.category_name,
               COUNT(v.variant_id) as variant_count,
               MIN(v.price) as min_price, MAX(v.price) as max_price
        FROM product p
        LEFT JOIN category c ON p.category_id = c.category_id
        LEFT JOIN variant v ON p.product_id = v.product_id
        GROUP BY p.product_id, p.title, p.description, c.category_name
        ORDER BY p.product_id
        """
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting all products: {e}")
        return []
    finally:
        conn.close()


def get_all_categories():
    """Get all categories"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT c.category_id, c.category_name, pc.category_name as parent_name
        FROM category c
        LEFT JOIN category pc ON c.parent_category_id = pc.category_id
        ORDER BY c.category_id
        """
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting all categories: {e}")
        return []
    finally:
        conn.close()


def add_new_product(data):
    """Add new product"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        # Generate new product ID
        cur.execute("SELECT MAX(product_id) FROM product")
        max_id = cur.fetchone()[0]
        new_id = (max_id + 1) if max_id else 1

        query = """
        INSERT INTO product (product_id, title, description, category_id)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(
            query, (new_id, data['title'], data['description'], data['category_id']))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding product: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_product_by_id(product_id):
    """Get product details by ID"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT p.product_id, p.title, p.description, p.category_id, c.category_name
        FROM product p
        LEFT JOIN category c ON p.category_id = c.category_id
        WHERE p.product_id = %s
        """
        cur.execute(query, (product_id,))
        return cur.fetchone()
    except Exception as e:
        print(f"Error getting product by ID: {e}")
        return None
    finally:
        conn.close()


def get_product_variants(product_id):
    """Get all variants for a product"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT v.variant_id, v.name, v.price, v.custom_attrbutes, 
               i.stock_count
        FROM variant v
        LEFT JOIN inventory i ON v.variant_id = i.variant_id
        WHERE v.product_id = %s
        """
        cur.execute(query, (product_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting product variants: {e}")
        return []
    finally:
        conn.close()


def update_product(product_id, data):
    """Update product details"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        UPDATE product 
        SET title = %s, description = %s, category_id = %s
        WHERE product_id = %s
        """
        cur.execute(
            query, (data['title'], data['description'], data['category_id'], product_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating product: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def delete_product(product_id):
    """Delete product and its variants"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        # Note: In a real system, you'd want to handle this more carefully
        # considering foreign key constraints
        cur.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting product: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_all_categories_with_stats():
    """Get all categories with product count statistics"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT c.category_id, c.category_name, pc.category_name as parent_name,
               COUNT(p.product_id) as product_count
        FROM category c
        LEFT JOIN category pc ON c.parent_category_id = pc.category_id
        LEFT JOIN product p ON c.category_id = p.category_id
        GROUP BY c.category_id, c.category_name, pc.category_name
        ORDER BY c.category_id
        """
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting categories with stats: {e}")
        return []
    finally:
        conn.close()


def add_new_category(data):
    """Add new category"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        # Get next category ID
        cur.execute("SELECT MAX(category_id) FROM category")
        max_id = cur.fetchone()[0]
        new_id = (max_id + 1) if max_id else 1
        
        parent_id = data.get('parent_category_id') if data.get('parent_category_id') != '' else None
        
        query = """
        INSERT INTO category (category_id, category_name, parent_category_id)
        VALUES (%s, %s, %s)
        """
        cur.execute(query, (new_id, data['category_name'], parent_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding category: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_all_orders_paginated(page=1, per_page=20):
    """Get paginated orders for admin"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        offset = (page - 1) * per_page
        query = """
        SELECT o.order_id, o.date, o.delivery_method, o.payment_method,
               ru.username, COUNT(oi.order_item_id) as item_count,
               SUM(oi.quantity * oi.price) as total_amount
        FROM orders o
        LEFT JOIN registered_user ru ON o.user_id = ru.user_id
        LEFT JOIN order_item oi ON o.order_id = oi.order_id
        GROUP BY o.order_id, o.date, o.delivery_method, o.payment_method, ru.username
        ORDER BY o.date DESC
        LIMIT %s OFFSET %s
        """
        cur.execute(query, (per_page, offset))
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting paginated orders: {e}")
        return []
    finally:
        conn.close()


def get_order_details(order_id):
    """Get detailed order information"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT o.order_id, o.date, o.delivery_method, o.payment_method,
               ru.username, ru.email
        FROM orders o
        LEFT JOIN registered_user ru ON o.user_id = ru.user_id
        WHERE o.order_id = %s
        """
        cur.execute(query, (order_id,))
        return cur.fetchone()
    except Exception as e:
        print(f"Error getting order details: {e}")
        return None
    finally:
        conn.close()


def get_inventory_overview():
    """Get inventory overview for admin"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT v.variant_id, p.title, v.name as variant_name, v.price,
               i.stock_count
        FROM variant v
        JOIN product p ON v.product_id = p.product_id
        LEFT JOIN inventory i ON v.variant_id = i.variant_id
        ORDER BY p.title, v.name
        """
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting inventory overview: {e}")
        return []
    finally:
        conn.close()


def get_low_stock_items(threshold=10):
    """Get items with low stock"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT v.variant_id, p.title, v.name as variant_name, i.stock_count
        FROM variant v
        JOIN product p ON v.product_id = p.product_id
        JOIN inventory i ON v.variant_id = i.variant_id
        WHERE i.stock_count < %s
        ORDER BY i.stock_count ASC
        """
        cur.execute(query, (threshold,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting low stock items: {e}")
        return []
    finally:
        conn.close()


def update_inventory_stock(variant_id, new_stock):
    """Update inventory stock"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = "UPDATE inventory SET stock_count = %s WHERE variant_id = %s"
        cur.execute(query, (new_stock, variant_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating inventory stock: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# ==================== USER PROFILE FUNCTIONS ====================


def get_user_profile(user_id):
    """Get user profile data"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT user_id, username, email
        FROM registered_user
        WHERE user_id = %s
        """
        cur.execute(query, (user_id,))
        return cur.fetchone()
    except Exception as e:
        print(f"Error getting user profile: {e}")
        return None
    finally:
        conn.close()


def get_user_orders(user_id):
    """Get user's order history"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT o.order_id, o.date, o.delivery_method, o.payment_method,
               COUNT(oi.order_item_id) as item_count,
               SUM(oi.quantity * oi.price) as total_amount
        FROM orders o
        LEFT JOIN order_item oi ON o.order_id = oi.order_id
        WHERE o.user_id = %s
        GROUP BY o.order_id, o.date, o.delivery_method, o.payment_method
        ORDER BY o.date DESC
        """
        cur.execute(query, (user_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting user orders: {e}")
        return []
    finally:
        conn.close()


def update_user_profile(user_id, data):
    """Update user profile"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        UPDATE registered_user 
        SET username = %s, email = %s
        WHERE user_id = %s
        """
        cur.execute(query, (data['username'], data['email'], user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating user profile: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_user_order_detail(user_id, order_id):
    """Get specific order detail for user"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT o.order_id, o.date, o.delivery_method, o.payment_method
        FROM orders o
        WHERE o.user_id = %s AND o.order_id = %s
        """
        cur.execute(query, (user_id, order_id))
        return cur.fetchone()
    except Exception as e:
        print(f"Error getting user order detail: {e}")
        return None
    finally:
        conn.close()

# ==================== API FUNCTIONS ====================


def search_products_api(query, category=''):
    """Search products for API"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        if category:
            sql_query = """
            SELECT p.product_id, p.title, p.description, c.name as category_name
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            WHERE p.title LIKE %s AND c.name LIKE %s
            """
            cur.execute(sql_query, ("%" + query + "%", "%" + category + "%"))
        else:
            sql_query = """
            SELECT p.product_id, p.title, p.description, c.name as category_name
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            WHERE p.title LIKE %s
            """
            cur.execute(sql_query, ("%" + query + "%",))
        
        results = cur.fetchall()
        return [{'id': r[0], 'title': r[1], 'description': r[2], 'category': r[3]} for r in results]
    except Exception as e:
        print(f"Error in API product search: {e}")
        return []
    finally:
        conn.close()


def change_user_password(user_id, current_password, new_password):
    """Change user password"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        # First verify current password
        cur.execute("SELECT password FROM registered_user WHERE user_id = %s", (user_id,))
        result = cur.fetchone()
        
        if not result or not check_password_hash(result[0], current_password):
            return False
        
        # Update password
        hashed_password = generate_password_hash(new_password)
        cur.execute("UPDATE registered_user SET password = %s WHERE user_id = %s", 
                   (hashed_password, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error changing password: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def toggle_user_admin_status(user_id):
    """Toggle user admin status"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        # Get current role
        cur.execute("SELECT role FROM registered_user WHERE user_id = %s", (user_id,))
        result = cur.fetchone()
        
        if not result:
            return False
        
        current_role = result[0]
        new_role = 'admin' if current_role != 'admin' else 'user'
        
        cur.execute("UPDATE registered_user SET role = %s WHERE user_id = %s", 
                   (new_role, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error toggling admin status: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def bulk_update_inventory(updates):
    """Bulk update inventory stock"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        for update in updates:
            variant_id = update.get('variant_id')
            stock_count = update.get('stock_count')
            cur.execute("UPDATE inventory SET stock_count = %s WHERE variant_id = %s", 
                       (stock_count, variant_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error bulk updating inventory: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def toggle_product_featured(product_id, featured):
    """Toggle product featured status"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE product SET featured = %s WHERE product_id = %s", 
                   (featured, product_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error toggling product featured: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def reorder_categories(category_orders):
    """Reorder categories"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        for order_data in category_orders:
            category_id = order_data.get('category_id')
            display_order = order_data.get('order')
            cur.execute("UPDATE category SET display_order = %s WHERE category_id = %s", 
                       (display_order, category_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error reordering categories: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def upload_user_avatar(user_id, file):
    """Upload and save user avatar"""
    import os
    from werkzeug.utils import secure_filename
    
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join('webapp', 'static', 'uploads', 'avatars')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate secure filename
        filename = secure_filename(file.filename)
        if filename == '':
            return False, None
            
        # Add user ID to filename to make it unique
        name, ext = os.path.splitext(filename)
        filename = f"user_{user_id}_{name}{ext}"
        
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        
        # Update user avatar in database
        avatar_url = f"/static/uploads/avatars/{filename}"
        conn = get_mysql_connection()
        cur = conn.cursor()
        cur.execute("UPDATE registered_user SET avatar = %s WHERE user_id = %s", 
                   (avatar_url, user_id))
        conn.commit()
        conn.close()
        
        return True, avatar_url
    except Exception as e:
        print(f"Error uploading avatar: {e}")
        return False, None


def get_cart_count(user_id):
    """Get total cart item count for user"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT SUM(quantity) FROM cart_items WHERE user_id = %s", (user_id,))
        result = cur.fetchone()
        return result[0] if result and result[0] else 0
    except Exception as e:
        print(f"Error getting cart count: {e}")
        return 0
    finally:
        conn.close()


def get_product_by_id(product_id):
    """Get product details by ID"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT p.product_id, p.title, p.description, p.category_id, c.name as category_name,
               p.featured, p.created_at
        FROM product p
        JOIN category c ON p.category_id = c.category_id
        WHERE p.product_id = %s
        """
        cur.execute(query, (product_id,))
        return cur.fetchone()
    except Exception as e:
        print(f"Error getting product by ID: {e}")
        return None
    finally:
        conn.close()


def get_product_variants(product_id):
    """Get all variants for a product"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT v.variant_id, v.name, v.price, v.variant_image, i.stock_count
        FROM variant v
        LEFT JOIN inventory i ON v.variant_id = i.variant_id
        WHERE v.product_id = %s
        """
        cur.execute(query, (product_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting product variants: {e}")
        return []
    finally:
        conn.close()


def update_order_status(order_id, new_status):
    """Update order status"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE orders SET status = %s WHERE order_id = %s", 
                   (new_status, order_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating order status: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_order_items(order_id):
    """Get items for a specific order"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT oi.order_item_id, p.title, v.name, oi.quantity, v.price
        FROM order_item oi
        JOIN variant v ON oi.variant_id = v.variant_id
        JOIN product p ON v.product_id = p.product_id
        WHERE oi.order_id = %s
        """
        cur.execute(query, (order_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting order items: {e}")
        return []
    finally:
        conn.close()


def add_category(data):
    """Add new category"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        name = data.get('name')
        description = data.get('description', '')
        parent_category = data.get('parent_category') or None
        is_active = 1 if data.get('is_active') else 0
        
        query = """
        INSERT INTO category (name, description, parent_category_id, is_active)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (name, description, parent_category, is_active))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding category: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def delete_category(category_id):
    """Delete category"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        # Check if category has products
        cur.execute("SELECT COUNT(*) FROM product WHERE category_id = %s", (category_id,))
        product_count = cur.fetchone()[0]
        
        if product_count > 0:
            return False, "Cannot delete category with products"
        
        cur.execute("DELETE FROM category WHERE category_id = %s", (category_id,))
        conn.commit()
        return True, "Category deleted successfully"
    except Exception as e:
        print(f"Error deleting category: {e}")
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


def search_products_by_category(category_id):
    """Search products by category"""
    conn = get_mysql_connection()
    cur = conn.cursor()
    try:
        query = """
        SELECT p.product_id, p.title, p.description, c.name as category_name
        FROM product p
        JOIN category c ON p.category_id = c.category_id
        WHERE p.category_id = %s
        """
        cur.execute(query, (category_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error searching products by category: {e}")
        return []
    finally:
        conn.close()
