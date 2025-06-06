# MongoDB Atlas Setup Guide

## Setting Up Your Own MongoDB Database

### Step 1: Create Cluster

1. Go to https://cloud.mongodb.com/
2. Sign in to your account
3. Click "Build a Database"
4. Choose "FREE" (M0 Sandbox)
5. Select your preferred region (choose one closest to you)
6. Give your cluster a name (e.g., "MyEcommerceCluster")
7. Click "Create Cluster"

### Step 2: Create Database User

1. In the "Security" section, click "Database Access"
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create a username and strong password
5. Set "Database User Privileges" to "Atlas admin" or "Read and write to any database"
6. Click "Add User"

### Step 3: Configure Network Access

1. In the "Security" section, click "Network Access"
2. Click "Add IP Address"
3. Choose "Add My Current IP Address" or "Allow Access from Anywhere" (0.0.0.0/0) for development
4. Click "Confirm"

### Step 4: Get Connection String

1. Click "Database" in the left sidebar
2. Click "Connect" button on your cluster
3. Choose "Connect your application"
4. Select "Python" and version "3.6 or later"
5. Copy the connection string (it will look like):
   `mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority`

### Step 5: Replace in .env file

Replace the MONGO_URI in your .env file with your new connection string.

## Example Connection String Format:

```
MONGO_URI=mongodb+srv://yourusername:yourpassword@yourcluster.abcde.mongodb.net/?retryWrites=true&w=majority&appName=YourClusterName
```

## Important Notes:

- Replace `<username>` with your database username
- Replace `<password>` with your database password
- Replace `<cluster>` with your cluster name
- Keep the `?retryWrites=true&w=majority` parameters
- You can add `&appName=YourAppName` at the end
