from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime

from app.models.review import Review
from app.models.user import User
from app.models.product import Product
from app.middleware.verify_token import verify_token, admin_required


def get_product_reviews(product_id):
    try:
        # Get product
        product = Product.objects.get(id=product_id)

        # Get reviews for product
        reviews = Review.objects(product=product).order_by('-created_at')

        # Format reviews
        review_list = []
        for review in reviews:
            review_dict = review.to_mongo().to_dict()
            review_dict['id'] = str(review_dict['_id'])
            if '_id' in review_dict:
                del review_dict['_id']

            # Include user details
            user = User.objects.get(id=review.user.id)
            review_dict['user'] = {
                'id': str(user.id),
                'name': user.name
            }

            # Format product ID
            review_dict['product'] = str(review_dict['product'])

            review_list.append(review_dict)

        return jsonify(review_list), 200
    except Product.DoesNotExist:
        return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        print(f"Error in get_product_reviews: {e}")
        return jsonify({"message": "Error occurred while fetching reviews"}), 500


def get_user_reviews():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        # Get reviews for user
        reviews = Review.objects(user=user).order_by('-created_at')

        # Format reviews
        review_list = []
        for review in reviews:
            review_dict = review.to_mongo().to_dict()
            review_dict['id'] = str(review_dict['_id'])
            if '_id' in review_dict:
                del review_dict['_id']

            # Include product details
            product = Product.objects.get(id=review.product.id)
            review_dict['product'] = {
                'id': str(product.id),
                'title': product.title
            }

            # Format user ID
            review_dict['user'] = str(review_dict['user'])

            review_list.append(review_dict)

        return jsonify(review_list), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in get_user_reviews: {e}")
        return jsonify({"message": "Error occurred while fetching reviews"}), 500


def create_review():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        data = request.get_json()

        # Validate required fields
        if 'product_id' not in data:
            return jsonify({"message": "Product ID is required"}), 400
        if 'rating' not in data:
            return jsonify({"message": "Rating is required"}), 400

        # Validate rating
        rating = int(data['rating'])
        if rating < 1 or rating > 5:
            return jsonify({"message": "Rating must be between 1 and 5"}), 400

        # Get product
        product = Product.objects.get(id=data['product_id'])

        # Check if user has already reviewed this product
        existing_review = Review.objects(user=user, product=product).first()
        if existing_review:
            return jsonify({"message": "You have already reviewed this product"}), 400

        # Create review
        review = Review(
            user=user,
            product=product,
            rating=rating,
            comment=data.get('comment', '')
        )
        review.save()

        # Update product rating
        all_reviews = Review.objects(product=product)
        total_rating = sum(r.rating for r in all_reviews)
        product.rating = total_rating / len(all_reviews)
        product.num_reviews = len(all_reviews)
        product.save()

        # Format review for response
        review_dict = review.to_mongo().to_dict()
        review_dict['id'] = str(review_dict['_id'])
        if '_id' in review_dict:
            del review_dict['_id']
        review_dict['user'] = str(review_dict['user'])
        review_dict['product'] = str(review_dict['product'])

        return jsonify(review_dict), 201
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Product.DoesNotExist:
        return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        print(f"Error in create_review: {e}")
        return jsonify({"message": "Error occurred while creating review"}), 500


def update_review(review_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        data = request.get_json()

        # Get review
        review = Review.objects.get(id=review_id, user=user)

        # Update fields
        if 'rating' in data:
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                return jsonify({"message": "Rating must be between 1 and 5"}), 400
            review.rating = rating

        if 'comment' in data:
            review.comment = data['comment']

        review.save()

        # Update product rating
        product = review.product
        all_reviews = Review.objects(product=product)
        total_rating = sum(r.rating for r in all_reviews)
        product.rating = total_rating / len(all_reviews)
        product.save()

        # Format review for response
        review_dict = review.to_mongo().to_dict()
        review_dict['id'] = str(review_dict['_id'])
        if '_id' in review_dict:
            del review_dict['_id']
        review_dict['user'] = str(review_dict['user'])
        review_dict['product'] = str(review_dict['product'])

        return jsonify(review_dict), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Review.DoesNotExist:
        return jsonify({"message": "Review not found"}), 404
    except Exception as e:
        print(f"Error in update_review: {e}")
        return jsonify({"message": "Error occurred while updating review"}), 500


def delete_review(review_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        # Get review
        review = Review.objects.get(id=review_id, user=user)

        # Get product for rating update
        product = review.product

        # Delete review
        review.delete()

        # Update product rating
        all_reviews = Review.objects(product=product)
        if all_reviews:
            total_rating = sum(r.rating for r in all_reviews)
            product.rating = total_rating / len(all_reviews)
            product.num_reviews = len(all_reviews)
        else:
            product.rating = 0
            product.num_reviews = 0
        product.save()

        return jsonify({"message": "Review deleted successfully"}), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Review.DoesNotExist:
        return jsonify({"message": "Review not found"}), 404
    except Exception as e:
        print(f"Error in delete_review: {e}")
        return jsonify({"message": "Error occurred while deleting review"}), 500
