# Flask Backend Installation Guide

This guide will help you set up and run the Flask backend for the e-commerce application.

## Requirements

- Python 3.8 or higher
- MongoDB (running locally or accessible via URI)
- pip (Python package installer)

## Installation Steps

1. **Create a virtual environment (recommended)**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Update the `.env` file with your configuration:

   ```
   MONGO_URI=mongodb://localhost:27017/ecommerce
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret_key
   PRODUCTION=false
   COOKIE_EXPIRATION_DAYS=30
   ORIGIN_1=http://localhost:3000
   ORIGIN_2=http://localhost:5173
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_email_password
   ```

4. **Initialize the database with sample data (optional)**

   ```bash
   python seed_db.py
   ```

5. **Migrate data from existing Node.js backend (optional)**

   If you already have data in your MongoDB from the Node.js backend:

   ```bash
   python migrate_data.py
   ```

6. **Run the application**

   ```bash
   python run.py
   ```

   The server will start at http://localhost:5000.

## API Testing

You can test the API using tools like:

- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)
- [curl](https://curl.se/) from the command line

## Troubleshooting

- **Connection issues with MongoDB**: Ensure MongoDB is running and the connection string in `.env` is correct.
- **Package dependency issues**: Make sure you're using a compatible Python version and have installed all required packages.
- **CORS errors**: Check that the ORIGIN values in `.env` match your frontend application URLs.

## Development

To enable debug mode for development:

```bash
# Windows
set FLASK_ENV=development
python run.py

# macOS/Linux
export FLASK_ENV=development
python run.py
```
