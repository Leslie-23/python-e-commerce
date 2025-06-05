from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from app.models.address import Address
from app.models.user import User
from app.middleware.verify_token import verify_token


def get_addresses():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        addresses = Address.objects(user=user)

        address_list = []
        for address in addresses:
            address_dict = address.to_mongo().to_dict()
            address_dict['id'] = str(address_dict['_id'])
            if '_id' in address_dict:
                del address_dict['_id']
            address_dict['user'] = str(address_dict['user'])
            address_list.append(address_dict)

        return jsonify(address_list), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in get_addresses: {e}")
        return jsonify({"message": "Error occurred while fetching addresses"}), 500


def get_address(address_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        address = Address.objects.get(id=address_id, user=user)

        address_dict = address.to_mongo().to_dict()
        address_dict['id'] = str(address_dict['_id'])
        if '_id' in address_dict:
            del address_dict['_id']
        address_dict['user'] = str(address_dict['user'])

        return jsonify(address_dict), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Address.DoesNotExist:
        return jsonify({"message": "Address not found"}), 404
    except Exception as e:
        print(f"Error in get_address: {e}")
        return jsonify({"message": "Error occurred while fetching address"}), 500


def create_address():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        data = request.get_json()
        data['user'] = user

        # Create address
        address = Address(**data)
        address.save()

        address_dict = address.to_mongo().to_dict()
        address_dict['id'] = str(address_dict['_id'])
        if '_id' in address_dict:
            del address_dict['_id']
        address_dict['user'] = str(address_dict['user'])

        return jsonify(address_dict), 201
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in create_address: {e}")
        return jsonify({"message": "Error occurred while creating address"}), 500


def update_address(address_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        address = Address.objects.get(id=address_id, user=user)

        data = request.get_json()

        # Update address
        for key, value in data.items():
            if key != 'user':  # Don't allow changing the user
                setattr(address, key, value)

        address.save()

        address_dict = address.to_mongo().to_dict()
        address_dict['id'] = str(address_dict['_id'])
        if '_id' in address_dict:
            del address_dict['_id']
        address_dict['user'] = str(address_dict['user'])

        return jsonify(address_dict), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Address.DoesNotExist:
        return jsonify({"message": "Address not found"}), 404
    except Exception as e:
        print(f"Error in update_address: {e}")
        return jsonify({"message": "Error occurred while updating address"}), 500


def delete_address(address_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        address = Address.objects.get(id=address_id, user=user)

        # Check if address is used in any orders
        from app.models.order import Order
        orders = Order.objects(shipping_address=address).count()
        if orders > 0:
            return jsonify({"message": "Cannot delete address as it's used in orders"}), 400

        address.delete()

        return jsonify({"message": "Address deleted successfully"}), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Address.DoesNotExist:
        return jsonify({"message": "Address not found"}), 404
    except Exception as e:
        print(f"Error in delete_address: {e}")
        return jsonify({"message": "Error occurred while deleting address"}), 500
