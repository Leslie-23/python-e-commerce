from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime

from app.models.cart import Cart
from app.models.user import User
from app.models.product import Product
from app.middleware.verify_token import verify_token


def get_cart():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        # Find or create cart
        cart = Cart.objects(user=user).first()
        if not cart:
            cart = Cart(user=user, items=[])
            cart.save()

        # Format cart items with product details
        cart_dict = cart.to_mongo().to_dict()
        cart_dict['id'] = str(cart_dict['_id'])
        if '_id' in cart_dict:
            del cart_dict['_id']

        # Update product details in items
        items_with_details = []
        for item in cart_dict['items']:
            try:
                product = Product.objects.get(id=item['product'])
                product_dict = product.to_mongo().to_dict()
                product_dict['id'] = str(product_dict['_id'])
                if '_id' in product_dict:
                    del product_dict['_id']

                item['product'] = product_dict
                items_with_details.append(item)
            except Product.DoesNotExist:
                # Skip deleted products
                continue

        cart_dict['items'] = items_with_details
        cart_dict['user'] = str(cart_dict['user'])

        return jsonify(cart_dict), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in get_cart: {e}")
        return jsonify({"message": "Error occurred while fetching cart"}), 500


def add_to_cart():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        # Validate product
        product = Product.objects.get(id=product_id)

        # Check stock
        if product.stock < quantity:
            return jsonify({"message": "Not enough stock available"}), 400

        # Find or create cart
        cart = Cart.objects(user=user).first()
        if not cart:
            cart = Cart(user=user, items=[])

        # Check if product already in cart
        product_in_cart = False
        for item in cart.items:
            if str(item['product']) == product_id:
                item['quantity'] += quantity
                product_in_cart = True
                break

        # If product not in cart, add it
        if not product_in_cart:
            cart.items.append({
                'product': product.id,
                'quantity': quantity,
                'price': product.discounted_price if product.discounted_price else product.price
            })

        # Update cart timestamp
        cart.updated_at = datetime.utcnow()
        cart.save()

        return jsonify({"message": "Product added to cart successfully"}), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Product.DoesNotExist:
        return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        print(f"Error in add_to_cart: {e}")
        return jsonify({"message": "Error occurred while adding to cart"}), 500


def update_cart_item(item_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        data = request.get_json()
        quantity = data.get('quantity', 1)

        # Find cart
        cart = Cart.objects(user=user).first()
        if not cart:
            return jsonify({"message": "Cart not found"}), 404

        # Find item in cart
        item_found = False
        for item in cart.items:
            if str(item['product']) == item_id:
                # Check stock if increasing quantity
                if quantity > item['quantity']:
                    product = Product.objects.get(id=item_id)
                    if product.stock < quantity:
                        return jsonify({"message": "Not enough stock available"}), 400

                # Update quantity
                item['quantity'] = quantity
                item_found = True
                break

        if not item_found:
            return jsonify({"message": "Item not found in cart"}), 404

        # Update cart timestamp
        cart.updated_at = datetime.utcnow()
        cart.save()

        return jsonify({"message": "Cart item updated successfully"}), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Product.DoesNotExist:
        return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        print(f"Error in update_cart_item: {e}")
        return jsonify({"message": "Error occurred while updating cart item"}), 500


def remove_from_cart(item_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        # Find cart
        cart = Cart.objects(user=user).first()
        if not cart:
            return jsonify({"message": "Cart not found"}), 404

        # Find and remove item from cart
        cart.items = [item for item in cart.items if str(
            item['product']) != item_id]

        # Update cart timestamp
        cart.updated_at = datetime.utcnow()
        cart.save()

        return jsonify({"message": "Item removed from cart successfully"}), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in remove_from_cart: {e}")
        return jsonify({"message": "Error occurred while removing from cart"}), 500


def clear_cart():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        # Find cart
        cart = Cart.objects(user=user).first()
        if not cart:
            return jsonify({"message": "Cart not found"}), 404

        # Clear cart items
        cart.items = []

        # Update cart timestamp
        cart.updated_at = datetime.utcnow()
        cart.save()

        return jsonify({"message": "Cart cleared successfully"}), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in clear_cart: {e}")
        return jsonify({"message": "Error occurred while clearing cart"}), 500
