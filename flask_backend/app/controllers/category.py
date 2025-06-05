from flask import request, jsonify
from app.models.category import Category
from app.middleware.verify_token import admin_required


def get_categories():
    try:
        categories = Category.objects.all()
        category_list = []
        for category in categories:
            category_dict = category.to_mongo().to_dict()
            category_dict['id'] = str(category_dict['_id'])
            if '_id' in category_dict:
                del category_dict['_id']
            category_list.append(category_dict)

        return jsonify(category_list), 200
    except Exception as e:
        print(f"Error in get_categories: {e}")
        return jsonify({"message": "Error occurred while fetching categories"}), 500


def get_category(category_id):
    try:
        category = Category.objects.get(id=category_id)
        category_dict = category.to_mongo().to_dict()
        category_dict['id'] = str(category_dict['_id'])
        if '_id' in category_dict:
            del category_dict['_id']

        return jsonify(category_dict), 200
    except Category.DoesNotExist:
        return jsonify({"message": "Category not found"}), 404
    except Exception as e:
        print(f"Error in get_category: {e}")
        return jsonify({"message": "Error occurred while fetching category"}), 500


@admin_required
def create_category():
    try:
        data = request.get_json()

        # Check if category with same name already exists
        existing_category = Category.objects(name=data['name']).first()
        if existing_category:
            return jsonify({"message": "Category with this name already exists"}), 400

        # Create category
        category = Category(**data)
        category.save()

        category_dict = category.to_mongo().to_dict()
        category_dict['id'] = str(category_dict['_id'])
        if '_id' in category_dict:
            del category_dict['_id']

        return jsonify(category_dict), 201
    except Exception as e:
        print(f"Error in create_category: {e}")
        return jsonify({"message": "Error occurred while creating category"}), 500


@admin_required
def update_category(category_id):
    try:
        category = Category.objects.get(id=category_id)
        data = request.get_json()

        # Check if updating name and if that name already exists
        if 'name' in data and data['name'] != category.name:
            existing_category = Category.objects(name=data['name']).first()
            if existing_category:
                return jsonify({"message": "Category with this name already exists"}), 400

        # Update category
        for key, value in data.items():
            setattr(category, key, value)

        category.save()

        category_dict = category.to_mongo().to_dict()
        category_dict['id'] = str(category_dict['_id'])
        if '_id' in category_dict:
            del category_dict['_id']

        return jsonify(category_dict), 200
    except Category.DoesNotExist:
        return jsonify({"message": "Category not found"}), 404
    except Exception as e:
        print(f"Error in update_category: {e}")
        return jsonify({"message": "Error occurred while updating category"}), 500


@admin_required
def delete_category(category_id):
    try:
        category = Category.objects.get(id=category_id)

        # Check if category is associated with any products
        from app.models.product import Product
        products = Product.objects(category=category).count()
        if products > 0:
            return jsonify({"message": f"Cannot delete category as it's associated with {products} product(s)"}), 400

        category.delete()
        return jsonify({"message": "Category deleted successfully"}), 200
    except Category.DoesNotExist:
        return jsonify({"message": "Category not found"}), 404
    except Exception as e:
        print(f"Error in delete_category: {e}")
        return jsonify({"message": "Error occurred while deleting category"}), 500
