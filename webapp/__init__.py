from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from .forms import LoginForm, SignupForm, EditProfileForm, ChangePasswordForm, ProductForm, CategoryForm, SearchForm, CheckoutForm
from functools import wraps
from .dash_SalesvsMonth import sales_for_product
from .dash_CtvsOr import categories_Orders
from .dash_PvsQ import dash_productVStime
from .dashapp import create_dash_application
import os
from .dbaccess import *
from datetime import date
from .databaseConfig import database_connector

database_connector()


# creating a global cursor
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
create_dash_application(app)
dash_productVStime(app)
categories_Orders(app)
sales_for_product(app)
sess = Session()
sess.init_app(app)


# users should not be logged in in order to use the platform


@app.route("/")
def home():
    # if the user is signed in load as signed in
    # use userid insted of id (a point to consider)

    signedin = False
    username = None

    if "userid" in session:
        signedin = True
        # Assuming username is saved in session["username"]
        username = session.get("username")

    return render_template("home.html", signedin=signedin, username=username)


@app.route("/signup/", methods=["POST", "GET"])
def signup():
    # we need to call the add user function here
    if request.method == "POST":
        data = request.form
        ok = add_user(data)
        if ok:
            session["user_authenticated"] = True
            return render_template("home.html")
        else:
            flash("Username already taken. Please choose another username.", "error")
        return render_template("signup.html", ok=ok)
    return render_template("signup.html", ok=True)


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        data = request.form
        userdat = auth_user(data)
        if userdat:
            session["user_authenticated"] = True
            session["userid"] = userdat[0]
            session["username"] = userdat[1]
            session['signedin'] = True
            
            # Get user role and avatar
            user_role = get_user_role(userdat[0])
            session["user_role"] = user_role
              # Get user profile for avatar
            user_profile = get_user_profile(userdat[0])
            if user_profile and len(user_profile) > 8:  # Check if avatar exists
                session["user_avatar"] = user_profile[8]
            else:
                session["user_avatar"] = None
                
            return redirect(url_for('home'))
        return render_template("login.html", err=True)
    return render_template("login.html", err=False)


@app.route('/products')
def products():
    # Get all products from database
    try:
        products_list = get_product_info()
        categories = get_all_categories()
        return render_template('products.html', products=products_list, categories=categories)
    except Exception as e:
        print(f"Error in products route: {e}")
        flash('Error loading products. Please try again.', 'error')
        return render_template('products.html', products=[], categories=[])


# we have to define a function to fetch trype of product separately..
# it would be good if we could make a function which takes product type as an arugment and bla bla
@app.route('/electronics')
def get_electronics():
    # we need to get all the electrnoics items from our database
    # for this we are going to get the primary key of the electronics category in the database and fetch all the data which has that value as the parent category id
    category_name = "ELECTRONIC PRODUCTS"  # The category name you want to display
    electronics = get_categories("Electronics")
    return render_template('main_categories.html', products=electronics, category_name=category_name)


@app.route('/toys')
def get_toys():
    # we need to get all the electrnoics items from our database
    # for this we are going to get the primary key of the electronics category in the database and fetch all the data which has that value as the parent category id
    category_name = "TOY PRODUCTS"
    toys = get_categories("Toys")
    return render_template('main_categories.html', products=toys, category_name=category_name)


# the following function will be used to get varients from the database
@app.route('/products/<product_id>', methods=['GET'])
def get_products(product_id):
    varients = get_products_from_database(product_id)

    return render_template('product_detail.html', products=varients)


# when someone clicked on a tile in the product page this function will be called
@app.route("/product/<product_id>/")
def view_product(product_id):
    # if 'userid' not in session:
    #     return redirect(url_for('home'))
    # type = session["type"]
    tup = get_single_product_info(product_id)

    print(tup)
    return render_template('product_detail.html', product=tup)


# need to create a function to get varient details from the database
@app.route('/varients/<product_id>', methods=['GET'])
def get_varient(product_id):
    # need to write the business logic here

    tup = get_varient_info(product_id)

    print(tup)
    # variant id is the last elemet in the fetched tuple
    # variant.name,variant.price,variant.custom_attrbutes,variant.variant_image,variant.variant_id
    variant_id = (tup[-1][-1])

    print(variant_id)
    stock_count = get_stock_count(variant_id)

    print(stock_count, "is the stock count")
    signedin = False
    if "userid" in session:
        signedin = True

    return render_template('variants.html', variants=tup, signedin=signedin, stock_count=stock_count)


@app.route('/search', methods=['GET'])
def search_products():
    search_query = request.args.get('query')

    products = search_product(search_query)

    return render_template('search_results.html', products=products)


@app.route("/cart/", methods=["POST", "GET"])
def cart():
    # Check if the user is signed in

    signedin = session.get("signedin", False)
    if signedin is True:
        username = session['username']
        cart = get_cart(session['userid'])
        return render_template('cart.html', cart=cart, signedin=signedin, username=username)
    else:
        signedin = False
        session_cart = session.get('cart', {})
        # get a list of all the varient ID's that are added to the cart
        variant_ids_string = list(session_cart.keys())
        variant_ids = [int(i) for i in variant_ids_string]
        # need to implement the function to fetch values from the database for the given id's
        variant_details = get_guest_cart(variant_ids)

        # append the count to each tuple in the variant details

        for i in range(len(variant_details)):
            variant_details[i] = variant_details[i] + (variant_ids[i],)

        return render_template('cart.html', guest_cart=variant_details, signedin=False, session_cart=session_cart)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    variant_id = request.form.get('variant_id')
    quantity = int(request.form.get('quantity'))
    try:
        username = session['username']

        if username is not None:
            print('hi')
            # User is logged in, update the database cart
            user_id = session['userid']
            # Update the cart_items table in the database
            # user_id, variant_id, quantity
            update_cart(user_id, variant_id, quantity)

            return redirect(url_for('cart'))
    except KeyError:
        # User is not logged in, update the session cart
        if 'cart' not in session:
            session['cart'] = {}
        cart = session['cart']
        if variant_id in cart:
            cart[variant_id] += quantity
        else:
            cart[variant_id] = quantity
        session.modified = True  # Mark the session as modified

        return redirect(url_for('cart'))


@app.route('/checkout')
def checkout():
    # need to show an estimated delivary time , total prices should be fetched from the cart
    # get_cart()

    is_logged = session.get("signedin", False)

    if is_logged is True:
        user_id = session['userid']
        # ci.quantity AS quantity,
        # v.name AS name,
        # v.price AS price,
        # v.variant_image AS variant_image,
        # p.title AS title,
        # v.variant_id as variant_id
        items = get_cart(user_id)
        # manipulating the tuple to meet our requirements

        total_price = sum([(tup[0] * tup[2]) for tup in items])

        print(total_price)

        return render_template('checkout.html', total_price=total_price)
    # also need to find the total price
    else:

        # find a way to calculate the total price from the session cart

        flash(
            'You are going to checkout as a guest. Some features may not be not available')
        return render_template('checkout.html')


@app.route('/checkout_successful', methods=['POST'])
def checkout_successful():
    if request.method == 'POST':
        # Here, we can process the form data as needed
        # you can access form data using request.form
        full_name = request.form.get('firstname')
        email = request.form.get('email')
        # Process other form data here as necessary
        # Assuming 'city' is the name attribute of the city input field
        city = request.form.get('city')

        signedin = session.get("signedin", False)
        order_id = gen_orderID()
        # need to update the order table in order to get rid of the foregin key constraint

        # Get the current date
        current_date = date.today()
        # Format the current date as a string in 'YYYY-MM-DD' format
        formatted_date = current_date.strftime('%Y-%m-%d')

        # order_id, date, delivery_method, payment_method, user_id

        if signedin:

            user_id = session['userid']

            order_table_details = [
                order_id, formatted_date, 'Express', 'visa', user_id]
            # first of all we need to update the order_table in order to avoid the primary key constraint
            update_order_table(order_table_details)

            # get the user's cart
            cart = get_cart(session['userid'])
            # extract the variant ID's from the cart
            order_item_ids = []
            for item in cart:
                new_ID = gen_order_item_ID()
                order_item_ids.append(new_ID)

                variant_Id = item[5]
                quantity = item[0]
                price = item[2]

                temp = []
                temp.append((new_ID, order_id, variant_Id, quantity, price))

                # update the delivary module
                stock_count = get_stock_count(variant_Id)
                destination_city = city
                delivary_module = [stock_count, destination_city, new_ID]

                # need to update the order item table from the above details
                update_order_items(temp, signedin, user_id=user_id)

                update_delivary_module(delivary_module)

            names = get_details_for_delivery_module(order_item_ids)

            return (render_template('checkout_succesful.html', names=names))

        if not signedin:
            # get the session cart
            # when updating the order tables we need a user_id and we don't have a user ID for a guest user

            # I AM GOING TO HARDCODE USERID *00000* FOR A GUEST USER
            user_id = 0
            order_table_details = [
                order_id, formatted_date, 'Express', 'visa', user_id]
            # first of all we need to update the order_table in order to avoid the primary key constraint
            update_order_table(order_table_details)

            # p.title, v.name, v.price, v.variant_image,v.variant_id
            session_cart = session.get('cart', {})
            # get a list of all the varient ID's that are added to the cart
            variant_ids_string = list(session_cart.keys())
            variant_ids = [int(i) for i in variant_ids_string]
            # need to implement the function to fetch values from the database for the given id's
            guest_cart = get_guest_cart(variant_ids)

            order_item_ids = []  # we are using this for the delivery module
            for item in guest_cart:
                new_ID = gen_order_item_ID()

                order_item_ids.append(new_ID)

                order_item_ids.append(new_ID)
                variant_Id = item[4]
                # quantity is in the hashmap of the session cart
                quantity = session_cart[str(variant_Id)]
                price = item[2]

                temp = []
                temp.append((new_ID, order_id, variant_Id, quantity, price))

                # update the delivary module
                stock_count = get_stock_count(variant_Id)
                destination_city = city
                delivary_module = [stock_count, destination_city, new_ID]

                update_order_items(temp, signedin, user_id=user_id)

                update_delivary_module(delivary_module)

            # clear the session cart
            session['cart'].clear()

            # try to implement and transaction to finish the checkout functionality
            # After processing the form data, you can render a success page
            return render_template('login.html', full_name=full_name, email=email)


@app.route('/analytics')
def analytics():
    return render_template('analytics3.html')


app.config['SECRET_KEY'] = os.urandom(17)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATES_AUTO_RELOAD'] = True
sess.init_app(app)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Handle contact form submission
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Here you could save to database or send email
        flash(f'Thank you {name}! Your message has been received. We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template("contact.html")

# Admin decorator to check if user is admin


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))

        user_role = get_user_role(session['userid'])
        if user_role != 'admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== ADMIN PANEL ROUTES ====================


@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard with overview statistics"""
    stats = get_admin_stats()
    recent_orders = get_recent_orders(limit=10)
    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)


@app.route('/admin/users')
@admin_required
def admin_users():
    """Manage users"""
    users = get_all_users()
    return render_template('admin/users.html', users=users)


@app.route('/admin/users/<int:user_id>/toggle_role', methods=['POST'])
@admin_required
def toggle_user_role(user_id):
    """Toggle user role between admin and user"""
    success = toggle_user_admin_role(user_id)
    if success:
        flash('User role updated successfully!', 'success')
    else:
        flash('Failed to update user role.', 'error')
    return redirect(url_for('admin_users'))


@app.route('/admin/products')
@admin_required
def admin_products():
    """Manage products"""
    products = get_all_products_admin()
    categories = get_all_categories()
    return render_template('admin/products.html', products=products, categories=categories)


@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Add new product"""
    if request.method == 'POST':
        data = request.form
        success = add_new_product(data)
        if success:
            flash('Product added successfully!', 'success')
            return redirect(url_for('admin_products'))
        else:
            flash('Failed to add product.', 'error')

    categories = get_all_categories()
    return render_template('admin/add_product.html', categories=categories)


@app.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    """Edit existing product"""
    if request.method == 'POST':
        data = request.form
        success = update_product(product_id, data)
        if success:
            flash('Product updated successfully!', 'success')
            return redirect(url_for('admin_products'))
        else:
            flash('Failed to update product.', 'error')

    product = get_product_by_id(product_id)
    categories = get_all_categories()
    variants = get_product_variants(product_id)
    return render_template('admin/edit_product.html', product=product, categories=categories, variants=variants)


@app.route('/admin/products/<int:product_id>/delete', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    """Delete product"""
    success = delete_product(product_id)
    if success:
        flash('Product deleted successfully!', 'success')
    else:
        flash('Failed to delete product.', 'error')
    return redirect(url_for('admin_products'))


@app.route('/admin/categories')
@admin_required
def admin_categories():
    """Manage categories"""
    categories = get_all_categories_with_stats()
    return render_template('admin/categories.html', categories=categories)


@app.route('/admin/categories/add', methods=['GET', 'POST'])
@admin_required
def admin_add_category():
    """Add new category"""
    if request.method == 'POST':
        data = request.form
        success = add_new_category(data)
        if success:
            flash('Category added successfully!', 'success')
            return redirect(url_for('admin_categories'))
        else:
            flash('Failed to add category.', 'error')

    parent_categories = get_all_categories()
    return render_template('admin/add_category.html', parent_categories=parent_categories)


@app.route('/admin/orders')
@admin_required
def admin_orders():
    """Manage orders"""
    page = request.args.get('page', 1, type=int)
    orders = get_all_orders_paginated(page=page, per_page=20)
    return render_template('admin/orders.html', orders=orders)


@app.route('/admin/orders/<int:order_id>')
@admin_required
def admin_order_detail(order_id):
    """View order details"""
    order = get_order_details(order_id)
    order_items = get_order_items(order_id)
    return render_template('admin/order_detail.html', order=order, order_items=order_items)


@app.route('/admin/inventory')
@admin_required
def admin_inventory():
    """Manage inventory"""
    inventory = get_inventory_overview()
    low_stock_items = get_low_stock_items(threshold=10)
    return render_template('admin/inventory.html', inventory=inventory, low_stock_items=low_stock_items)


@app.route('/admin/inventory/<int:variant_id>/update', methods=['POST'])
@admin_required
def admin_update_inventory(variant_id):
    """Update inventory levels"""
    new_stock = request.form.get('stock_count', type=int)
    success = update_inventory_stock(variant_id, new_stock)
    if success:
        flash('Inventory updated successfully!', 'success')
    else:
        flash('Failed to update inventory.', 'error')
    return redirect(url_for('admin_inventory'))


@app.route('/admin/analytics')
@admin_required
def admin_analytics():
    """Advanced analytics for admin"""
    return render_template('admin/analytics.html')


@app.route('/admin/settings')
@admin_required
def admin_settings():
    """Admin settings"""
    return render_template('admin/settings.html')

# ==================== USER PROFILE ROUTES ====================


@app.route('/profile')
def user_profile():
    """User profile page"""
    if 'userid' not in session:
        flash('Please log in to view your profile.', 'error')
        return redirect(url_for('login'))

    user_data = get_user_profile(session['userid'])
    user_orders = get_user_orders(session['userid'])
    return render_template('user/profile.html', user=user_data, orders=user_orders)


@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    """Edit user profile"""
    if 'userid' not in session:
        flash('Please log in to edit your profile.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.form
        success = update_user_profile(session['userid'], data)
        if success:
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user_profile'))
        else:
            flash('Failed to update profile.', 'error')

    user_data = get_user_profile(session['userid'])
    return render_template('user/edit_profile.html', user=user_data)


@app.route('/orders')
def user_orders():
    """User order history"""
    if 'userid' not in session:
        flash('Please log in to view your orders.', 'error')
        return redirect(url_for('login'))

    orders = get_user_orders(session['userid'])
    return render_template('user/orders.html', orders=orders)


@app.route('/orders/<int:order_id>')
def user_order_detail(order_id):
    """User order detail"""
    if 'userid' not in session:
        flash('Please log in to view order details.', 'error')
        return redirect(url_for('login'))

    order = get_user_order_detail(session['userid'], order_id)
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('user_orders'))

    order_items = get_order_items(order_id)
    return render_template('user/order_detail.html', order=order, order_items=order_items)


@app.route('/profile/change-password', methods=['GET', 'POST'])
def change_password():
    """Change user password"""
    if 'userid' not in session:
        flash('Please log in to change your password.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return render_template('user/change_password.html')

        if change_user_password(session['userid'], current_password, new_password):
            flash('Password changed successfully!', 'success')
            return redirect(url_for('user_profile'))
        else:
            flash('Current password is incorrect.', 'error')

    return render_template('user/change_password.html')


@app.route('/logout')
def logout():
    """Enhanced logout functionality"""
    username = session.get('username')
    session.clear()
    flash(f'You have been logged out successfully, {username}!', 'info')
    return redirect(url_for('home'))


# ==================== ADDITIONAL API ROUTES ====================

@app.route('/api/admin/stats')
@admin_required
def api_admin_stats():
    """API endpoint for admin dashboard stats"""
    stats = get_admin_stats()
    return jsonify(stats)


@app.route('/api/users/<int:user_id>/toggle-admin', methods=['POST'])
@admin_required
def api_toggle_user_admin(user_id):
    """API to toggle user admin status"""
    success = toggle_user_admin_status(user_id)
    return jsonify({'success': success})


@app.route('/api/orders/<int:order_id>/status', methods=['POST'])
@admin_required
def api_update_order_status(order_id):
    """API to update order status"""
    new_status = request.json.get('status')
    success = update_order_status(order_id, new_status)
    return jsonify({'success': success})


@app.route('/api/inventory/bulk-update', methods=['POST'])
@admin_required
def api_bulk_update_inventory():
    """API for bulk inventory updates"""
    updates = request.json.get('updates', [])
    success = bulk_update_inventory(updates)
    return jsonify({'success': success})


@app.route('/api/products/featured', methods=['GET', 'POST'])
@admin_required
def api_toggle_featured_product():
    """API to toggle product featured status"""
    if request.method == 'POST':
        product_id = request.json.get('product_id')
        featured = request.json.get('featured')
        success = toggle_product_featured(product_id, featured)
        return jsonify({'success': success})


@app.route('/api/categories/reorder', methods=['POST'])
@admin_required
def api_reorder_categories():
    """API to reorder categories"""
    category_orders = request.json.get('orders', [])
    success = reorder_categories(category_orders)
    return jsonify({'success': success})


@app.route('/api/user/avatar', methods=['POST'])
def api_upload_avatar():
    """API to upload user avatar"""
    if 'userid' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})

    if 'avatar' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})

    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})

    success, avatar_url = upload_user_avatar(session['userid'], file)
    if success:
        session['user_avatar'] = avatar_url
        return jsonify({'success': True, 'avatar_url': avatar_url})
    else:
        return jsonify({'success': False, 'message': 'Upload failed'})


@app.route('/api/cart/count')
def api_cart_count():
    """API to get cart item count"""
    if 'userid' in session:
        count = get_cart_count(session['userid'])
    else:
        count = len(session.get('cart', {}))
    return jsonify({'count': count})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500
