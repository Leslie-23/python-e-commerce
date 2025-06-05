from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from app.models.product import Product
from app.models.user import User
from app.models.brand import Brand
from app.models.category import Category
from app.middleware.verify_token import admin_required


def get_products():
    try:
        # Get query parameters
        page = int(request.args.get('_page', 1))
        limit = int(request.args.get('_limit', 10))
        sort_by = request.args.get('_sort', 'title')
        order = request.args.get('_order', 'asc')

        # Apply filters
        query = {}
        if 'title' in request.args:
            query['title__icontains'] = request.args.get('title')
        if 'brand' in request.args:
            brand = Brand.objects(name=request.args.get('brand')).first()
            if brand:
                query['brand'] = brand
        if 'category' in request.args:
            category = Category.objects(
                name=request.args.get('category')).first()
            if category:
                query['category'] = category
        if 'minPrice' in request.args:
            query['price__gte'] = float(request.args.get('minPrice'))
        if 'maxPrice' in request.args:
            query['price__lte'] = float(request.args.get('maxPrice'))

        # Get products
        sort_direction = 1 if order == 'asc' else -1
        products = Product.objects(**query).order_by((sort_direction, sort_by))

        # Pagination
        total = products.count()
        products = products.skip((page - 1) * limit).limit(limit)

        # Convert to dict for JSON response
        product_list = []
        for product in products:
            product_dict = product.to_mongo().to_dict()
            product_dict['id'] = str(product_dict['_id'])
            if '_id' in product_dict:
                del product_dict['_id']
            if 'brand' in product_dict and product_dict['brand']:
                brand = Brand.objects.get(id=product_dict['brand'])
                product_dict['brand'] = {
                    'id': str(brand.id),
                    'name': brand.name
                }
            if 'category' in product_dict and product_dict['category']:
                category = Category.objects.get(id=product_dict['category'])
                product_dict['category'] = {
                    'id': str(category.id),
                    'name': category.name
                }
            product_list.append(product_dict)

        # Create response with pagination headers
        response = jsonify(product_list)
        response.headers['X-Total-Count'] = total

        return response, 200
    except Exception as e:
        print(f"Error in get_products: {e}")
        return jsonify({"message": "Error occurred while fetching products"}), 500


def get_product(product_id):
    try:
        product = Product.objects.get(id=product_id)
        product_dict = product.to_mongo().to_dict()
        product_dict['id'] = str(product_dict['_id'])
        if '_id' in product_dict:
            del product_dict['_id']

        # Include brand and category details
        if 'brand' in product_dict and product_dict['brand']:
            brand = Brand.objects.get(id=product_dict['brand'])
            product_dict['brand'] = {
                'id': str(brand.id),
                'name': brand.name
            }
        if 'category' in product_dict and product_dict['category']:
            category = Category.objects.get(id=product_dict['category'])
            product_dict['category'] = {
                'id': str(category.id),
                'name': category.name
            }

        return jsonify(product_dict), 200
    except Product.DoesNotExist:
        return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        print(f"Error in get_product: {e}")
        return jsonify({"message": "Error occurred while fetching product"}), 500


@admin_required
def create_product():
    try:
        data = request.get_json()

        # Handle brand and category references
        if 'brand' in data and data['brand']:
            brand = Brand.objects.get(id=data['brand'])
            data['brand'] = brand
        if 'category' in data and data['category']:
            category = Category.objects.get(id=data['category'])
            data['category'] = category

        # Create product
        product = Product(**data)
        product.save()

        # Convert to dict for JSON response
        product_dict = product.to_mongo().to_dict()
        product_dict['id'] = str(product_dict['_id'])
        if '_id' in product_dict:
            del product_dict['_id']

        return jsonify(product_dict), 201
    except (Brand.DoesNotExist, Category.DoesNotExist):
        return jsonify({"message": "Brand or category not found"}), 404
    except Exception as e:
        print(f"Error in create_product: {e}")
        return jsonify({"message": "Error occurred while creating product"}), 500


@admin_required
def update_product(product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = request.get_json()

        # Handle brand and category references
        if 'brand' in data and data['brand']:
            brand = Brand.objects.get(id=data['brand'])
            data['brand'] = brand
        if 'category' in data and data['category']:
            category = Category.objects.get(id=data['category'])
            data['category'] = category

        # Update product
        for key, value in data.items():
            setattr(product, key, value)

        product.save()

        # Convert to dict for JSON response
        product_dict = product.to_mongo().to_dict()
        product_dict['id'] = str(product_dict['_id'])
        if '_id' in product_dict:
            del product_dict['_id']

        return jsonify(product_dict), 200
    except Product.DoesNotExist:
        return jsonify({"message": "Product not found"}), 404
    except (Brand.DoesNotExist, Category.DoesNotExist):
        return jsonify({"message": "Brand or category not found"}), 404
    except Exception as e:
        print(f"Error in update_product: {e}")
        return jsonify({"message": "Error occurred while updating product"}), 500


@admin_required
def delete_product(product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Product.DoesNotExist:
        return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        print(f"Error in delete_product: {e}")
        return jsonify({"message": "Error occurred while deleting product"}), 500
