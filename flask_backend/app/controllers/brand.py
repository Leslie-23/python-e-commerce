from flask import request, jsonify
from app.models.brand import Brand
from app.middleware.verify_token import admin_required


def get_brands():
    try:
        brands = Brand.objects.all()
        brand_list = []
        for brand in brands:
            brand_dict = brand.to_mongo().to_dict()
            brand_dict['id'] = str(brand_dict['_id'])
            if '_id' in brand_dict:
                del brand_dict['_id']
            brand_list.append(brand_dict)

        return jsonify(brand_list), 200
    except Exception as e:
        print(f"Error in get_brands: {e}")
        return jsonify({"message": "Error occurred while fetching brands"}), 500


def get_brand(brand_id):
    try:
        brand = Brand.objects.get(id=brand_id)
        brand_dict = brand.to_mongo().to_dict()
        brand_dict['id'] = str(brand_dict['_id'])
        if '_id' in brand_dict:
            del brand_dict['_id']

        return jsonify(brand_dict), 200
    except Brand.DoesNotExist:
        return jsonify({"message": "Brand not found"}), 404
    except Exception as e:
        print(f"Error in get_brand: {e}")
        return jsonify({"message": "Error occurred while fetching brand"}), 500


@admin_required
def create_brand():
    try:
        data = request.get_json()

        # Check if brand with same name already exists
        existing_brand = Brand.objects(name=data['name']).first()
        if existing_brand:
            return jsonify({"message": "Brand with this name already exists"}), 400

        # Create brand
        brand = Brand(**data)
        brand.save()

        brand_dict = brand.to_mongo().to_dict()
        brand_dict['id'] = str(brand_dict['_id'])
        if '_id' in brand_dict:
            del brand_dict['_id']

        return jsonify(brand_dict), 201
    except Exception as e:
        print(f"Error in create_brand: {e}")
        return jsonify({"message": "Error occurred while creating brand"}), 500


@admin_required
def update_brand(brand_id):
    try:
        brand = Brand.objects.get(id=brand_id)
        data = request.get_json()

        # Check if updating name and if that name already exists
        if 'name' in data and data['name'] != brand.name:
            existing_brand = Brand.objects(name=data['name']).first()
            if existing_brand:
                return jsonify({"message": "Brand with this name already exists"}), 400

        # Update brand
        for key, value in data.items():
            setattr(brand, key, value)

        brand.save()

        brand_dict = brand.to_mongo().to_dict()
        brand_dict['id'] = str(brand_dict['_id'])
        if '_id' in brand_dict:
            del brand_dict['_id']

        return jsonify(brand_dict), 200
    except Brand.DoesNotExist:
        return jsonify({"message": "Brand not found"}), 404
    except Exception as e:
        print(f"Error in update_brand: {e}")
        return jsonify({"message": "Error occurred while updating brand"}), 500


@admin_required
def delete_brand(brand_id):
    try:
        brand = Brand.objects.get(id=brand_id)

        # Check if brand is associated with any products
        from app.models.product import Product
        products = Product.objects(brand=brand).count()
        if products > 0:
            return jsonify({"message": f"Cannot delete brand as it's associated with {products} product(s)"}), 400

        brand.delete()
        return jsonify({"message": "Brand deleted successfully"}), 200
    except Brand.DoesNotExist:
        return jsonify({"message": "Brand not found"}), 404
    except Exception as e:
        print(f"Error in delete_brand: {e}")
        return jsonify({"message": "Error occurred while deleting brand"}), 500
