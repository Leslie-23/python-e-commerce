# E-commerce Flask Backend

This is the backend API for the e-commerce application, built with Flask and MongoDB.

## Setup Instructions

### Prerequisites

- Python 3.8+ installed
- MongoDB installed and running
- Virtual environment (recommended)

### Installation Steps

1. **Create and activate a virtual environment**

   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   - Rename `.env.example` to `.env` (if you haven't already)
   - Update the variables in the `.env` file with your actual values

4. **Start the application**

   ```
   python run.py
   ```

   The server will start at http://localhost:5000.

## API Documentation

The API provides the following endpoints:

### Authentication

- `POST /auth/signup` - Register a new user
- `POST /auth/login` - Log in a user
- `GET /auth/logout` - Log out a user
- `GET /auth/check-auth` - Check if a user is authenticated
- `POST /auth/verify-otp` - Verify an OTP for email verification
- `POST /auth/resend-otp` - Resend an OTP for email verification
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset a password with a token

### Users

- `GET /users` - Get all users (admin only)
- `GET /users/:id` - Get a user by ID
- `PUT /users/:id` - Update a user
- `DELETE /users/:id` - Delete a user (admin only)

### Products

- `GET /products` - Get all products (supports filtering and pagination)
- `GET /products/:id` - Get a product by ID
- `POST /products` - Create a new product (admin only)
- `PUT /products/:id` - Update a product (admin only)
- `DELETE /products/:id` - Delete a product (admin only)

### Categories

- `GET /categories` - Get all categories
- `GET /categories/:id` - Get a category by ID
- `POST /categories` - Create a new category (admin only)
- `PUT /categories/:id` - Update a category (admin only)
- `DELETE /categories/:id` - Delete a category (admin only)

### Brands

- `GET /brands` - Get all brands
- `GET /brands/:id` - Get a brand by ID
- `POST /brands` - Create a new brand (admin only)
- `PUT /brands/:id` - Update a brand (admin only)
- `DELETE /brands/:id` - Delete a brand (admin only)

### Cart

- `GET /cart` - Get the current user's cart
- `POST /cart/add` - Add a product to the cart
- `PUT /cart/item/:id` - Update a cart item's quantity
- `DELETE /cart/item/:id` - Remove an item from the cart
- `DELETE /cart/clear` - Clear the cart

### Addresses

- `GET /address` - Get all addresses for the current user
- `GET /address/:id` - Get an address by ID
- `POST /address` - Create a new address
- `PUT /address/:id` - Update an address
- `DELETE /address/:id` - Delete an address

### Orders, Reviews, and Wishlist

- Endpoints for orders, reviews, and wishlist will be documented as they are implemented

## Migrating from Node.js to Flask

This codebase was migrated from a Node.js/Express backend to a Flask backend. The API structure and functionality have been maintained, but the implementation uses Python and Flask instead of JavaScript and Express.
