from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from app.models.wishlist import Wishlist
from app.models.user import User
from app.models.product import Product
from app.middleware.verify_token import verify_token


def get_wishlist():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        # Find or create wishlist
        wishlist = Wishlist.objects(user=user).first()
        if not wishlist:
            wishlist = Wishlist(user=user, products=[])
            wishlist.save()

        # Format wishlist with product details
        wishlist_dict = wishlist.to_mongo().to_dict()
        wishlist_dict['id'] = str(wishlist_dict['_id'])
        if '_id' in wishlist_dict:
            del wishlist_dict['_id']

        # Get product details
        products_with_details = []
        for product_id in wishlist_dict['products']:
            try:
                product = Product.objects.get(id=product_id)
                product_dict = product.to_mongo().to_dict()
                product_dict['id'] = str(product_dict['_id'])
                if '_id' in product_dict:
                    del product_dict['_id']

                # Include brand and category details if available
                if 'brand' in product_dict and product_dict['brand']:
                    from app.models.brand import Brand
                    brand = Brand.objects.get(id=product_dict['brand'])
                    product_dict['brand'] = {
                        'id': str(brand.id),
                        'name': brand.name
                    }
                if 'category' in product_dict and product_dict['category']:
                    from app.models.category import Category
                    category = Category.objects.get(
                        id=product_dict['category'])
                    product_dict['category'] = {
                        'id': str(category.id),
                        'name': category.name
                    }

                products_with_details.append(product_dict)
            except Product.DoesNotExist:
                # Skip deleted products
                continue

        wishlist_dict['products'] = products_with_details
        wishlist_dict['user'] = str(wishlist_dict['user'])

        return jsonify(wishlist_dict), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in get_wishlist: {e}")
        return jsonify({"message": "Error occurred while fetching wishlist"}), 500


def add_to_wishlist():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        data = request.get_json()

        # Validate product ID
        if 'product_id' not in data:
            return jsonify({"message": "Product ID is required"}), 400

        # Get product
        product = Product.objects.get(id=data['product_id'])

        # Find or create wishlist
        wishlist = Wishlist.objects(user=user).first()
        if not wishlist:
            wishlist = Wishlist(user=user, products=[])

        # Check if product already in wishlist
        if product.id in wishlist.products:
            return jsonify({"message": "Product already in wishlist"}), 400

        # Add product to wishlist
        wishlist.products.append(product)
        wishlist.save()

        return jsonify({"message": "Product added to wishlist successfully"}), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Product.DoesNotExist:
        return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        print(f"Error in add_to_wishlist: {e}")
        return jsonify({"message": "Error occurred while adding to wishlist"}), 500


def remove_from_wishlist(product_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        # Get product
        product = Product.objects.get(id=product_id)

        # Find wishlist
        wishlist = Wishlist.objects(user=user).first()
        if not wishlist:
            return jsonify({"message": "Wishlist not found"}), 404

        # Check if product in wishlist
        if product.id not in wishlist.products:
            return jsonify({"message": "Product not in wishlist"}), 404

        # Remove product from wishlist
        wishlist.products.remove(product)
        wishlist.save()

        return jsonify({"message": "Product removed from wishlist successfully"}), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Product.DoesNotExist:
        return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        print(f"Error in remove_from_wishlist: {e}")
        return jsonify({"message": "Error occurred while removing from wishlist"}), 500


def clear_wishlist():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        # Find wishlist
        wishlist = Wishlist.objects(user=user).first()
        if not wishlist:
            return jsonify({"message": "Wishlist not found"}), 404

        # Clear wishlist
        wishlist.products = []
        wishlist.save()

        return jsonify({"message": "Wishlist cleared successfully"}), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in clear_wishlist: {e}")
        return jsonify({"message": "Error occurred while clearing wishlist"}), 500
