from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime

from app.models.order import Order
from app.models.user import User
from app.models.cart import Cart
from app.models.address import Address
from app.models.product import Product
from app.middleware.verify_token import verify_token, admin_required


def get_orders():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        # Check if admin and querying all orders
        if user.is_admin and request.args.get('all') == 'true':
            orders = Order.objects.order_by('-created_at')
        else:
            # Get orders for current user only
            orders = Order.objects(user=user).order_by('-created_at')

        # Format orders
        order_list = []
        for order in orders:
            order_dict = order.to_mongo().to_dict()
            order_dict['id'] = str(order_dict['_id'])
            if '_id' in order_dict:
                del order_dict['_id']

            # Format user ID
            order_dict['user'] = str(order_dict['user'])

            # Format shipping address
            address = Address.objects.get(id=order.shipping_address.id)
            address_dict = address.to_mongo().to_dict()
            address_dict['id'] = str(address_dict['_id'])
            if '_id' in address_dict:
                del address_dict['_id']
            address_dict['user'] = str(address_dict['user'])
            order_dict['shipping_address'] = address_dict

            order_list.append(order_dict)

        return jsonify(order_list), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in get_orders: {e}")
        return jsonify({"message": "Error occurred while fetching orders"}), 500


def get_order(order_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        # Allow admins to view any order
        if user.is_admin:
            order = Order.objects.get(id=order_id)
        else:
            # Only allow users to view their own orders
            order = Order.objects.get(id=order_id, user=user)

        # Format order
        order_dict = order.to_mongo().to_dict()
        order_dict['id'] = str(order_dict['_id'])
        if '_id' in order_dict:
            del order_dict['_id']

        # Format user ID
        order_dict['user'] = str(order_dict['user'])

        # Format shipping address
        address = Address.objects.get(id=order.shipping_address.id)
        address_dict = address.to_mongo().to_dict()
        address_dict['id'] = str(address_dict['_id'])
        if '_id' in address_dict:
            del address_dict['_id']
        address_dict['user'] = str(address_dict['user'])
        order_dict['shipping_address'] = address_dict

        return jsonify(order_dict), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Order.DoesNotExist:
        return jsonify({"message": "Order not found"}), 404
    except Exception as e:
        print(f"Error in get_order: {e}")
        return jsonify({"message": "Error occurred while fetching order"}), 500


def create_order():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        data = request.get_json()

        # Validate payment method
        if 'payment_method' not in data:
            return jsonify({"message": "Payment method is required"}), 400

        # Validate shipping address
        if 'shipping_address' not in data:
            return jsonify({"message": "Shipping address is required"}), 400

        # Get shipping address
        try:
            address = Address.objects.get(
                id=data['shipping_address'], user=user)
        except Address.DoesNotExist:
            return jsonify({"message": "Shipping address not found"}), 404

        # Get cart
        cart = Cart.objects(user=user).first()
        if not cart or not cart.items:
            return jsonify({"message": "Cart is empty"}), 400

        # Calculate total amount and validate stock
        total_amount = 0
        order_items = []

        for item in cart.items:
            try:
                product = Product.objects.get(id=item['product'])

                # Check stock
                if product.stock < item['quantity']:
                    return jsonify({
                        "message": f"Not enough stock for {product.title}. Available: {product.stock}, Requested: {item['quantity']}"
                    }), 400

                # Calculate price
                price = product.discounted_price if product.discounted_price else product.price
                item_total = price * item['quantity']
                total_amount += item_total

                # Add to order items
                order_items.append({
                    'product': str(product.id),
                    'title': product.title,
                    'price': price,
                    'quantity': item['quantity'],
                    'total': item_total
                })

                # Update product stock
                product.stock -= item['quantity']
                product.save()

            except Product.DoesNotExist:
                # Skip deleted products
                continue

        # Create order
        order = Order(
            user=user,
            items=order_items,
            total_amount=total_amount,
            payment_method=data['payment_method'],
            shipping_address=address
        )
        order.save()

        # Clear cart
        cart.items = []
        cart.updated_at = datetime.utcnow()
        cart.save()

        # Format order for response
        order_dict = order.to_mongo().to_dict()
        order_dict['id'] = str(order_dict['_id'])
        if '_id' in order_dict:
            del order_dict['_id']
        order_dict['user'] = str(order_dict['user'])
        order_dict['shipping_address'] = str(order_dict['shipping_address'])

        return jsonify(order_dict), 201
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in create_order: {e}")
        return jsonify({"message": "Error occurred while creating order"}), 500


@admin_required
def update_order_status(order_id):
    try:
        data = request.get_json()

        if 'status' not in data:
            return jsonify({"message": "Order status is required"}), 400

        # Validate status
        valid_statuses = ['pending', 'processing',
                          'shipped', 'delivered', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({"message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400

        # Get order
        order = Order.objects.get(id=order_id)

        # Update status
        order.status = data['status']
        order.updated_at = datetime.utcnow()
        order.save()

        # Format order for response
        order_dict = order.to_mongo().to_dict()
        order_dict['id'] = str(order_dict['_id'])
        if '_id' in order_dict:
            del order_dict['_id']
        order_dict['user'] = str(order_dict['user'])
        order_dict['shipping_address'] = str(order_dict['shipping_address'])

        return jsonify(order_dict), 200
    except Order.DoesNotExist:
        return jsonify({"message": "Order not found"}), 404
    except Exception as e:
        print(f"Error in update_order_status: {e}")
        return jsonify({"message": "Error occurred while updating order status"}), 500


@admin_required
def update_payment_status(order_id):
    try:
        data = request.get_json()

        if 'payment_status' not in data:
            return jsonify({"message": "Payment status is required"}), 400

        # Validate payment status
        valid_statuses = ['pending', 'completed', 'failed']
        if data['payment_status'] not in valid_statuses:
            return jsonify({"message": f"Invalid payment status. Must be one of: {', '.join(valid_statuses)}"}), 400

        # Get order
        order = Order.objects.get(id=order_id)

        # Update payment status
        order.payment_status = data['payment_status']
        order.updated_at = datetime.utcnow()
        order.save()

        # Format order for response
        order_dict = order.to_mongo().to_dict()
        order_dict['id'] = str(order_dict['_id'])
        if '_id' in order_dict:
            del order_dict['_id']
        order_dict['user'] = str(order_dict['user'])
        order_dict['shipping_address'] = str(order_dict['shipping_address'])

        return jsonify(order_dict), 200
    except Order.DoesNotExist:
        return jsonify({"message": "Order not found"}), 404
    except Exception as e:
        print(f"Error in update_payment_status: {e}")
        return jsonify({"message": "Error occurred while updating payment status"}), 500
