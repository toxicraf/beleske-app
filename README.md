# Customers Database

A simple SQLite database with a Customers table populated with test data.

## Database Structure

The `Customers` table contains the following fields:
- `id` - Primary key (auto-increment)
- `first_name` - Customer's first name
- `last_name` - Customer's last name
- `email` - Unique email address
- `phone` - Phone number
- `address` - Street address
- `city` - City
- `state` - State abbreviation
- `zip_code` - ZIP code
- `country` - Country (default: 'USA')
- `date_created` - Timestamp of record creation
- `is_active` - Active status (default: 1)

## Setup Options

### Option 1: Using Python (if Python is installed)
```bash
python create_database.py
```
This will create `customers.db` with 50 test records.

### Option 2: Using SQLite3 Command Line Tool
If you have SQLite3 installed:
```bash
sqlite3 customers.db < create_database.sql
```

Or on Windows:
```bash
setup_database.bat
```

### Option 3: Using Online SQLite Tools
1. Go to https://sqliteonline.com/ or https://sqliteviewer.app/
2. Copy the contents of `create_database.sql`
3. Paste and execute the SQL commands
4. Download the database file

### Option 4: Using DB Browser for SQLite
1. Download DB Browser for SQLite from https://sqlitebrowser.org/
2. Create a new database
3. Open the SQL tab
4. Copy and paste the contents of `create_database.sql`
5. Execute the SQL

## Querying the Database

### Using Python:
```python
import sqlite3

conn = sqlite3.connect('customers.db')
cursor = conn.cursor()

# Example query
cursor.execute('SELECT * FROM Customers WHERE city = ?', ('New York',))
results = cursor.fetchall()

for row in results:
    print(row)

conn.close()
```

### Using SQLite3 Command Line:
```bash
sqlite3 customers.db "SELECT * FROM Customers LIMIT 5;"
```

### Sample Queries:
```sql
-- Get all customers
SELECT * FROM Customers;

-- Count customers by city
SELECT city, COUNT(*) as count FROM Customers GROUP BY city;

-- Find customers in New York
SELECT first_name, last_name, email FROM Customers WHERE city = 'New York';

-- Get active customers
SELECT * FROM Customers WHERE is_active = 1;
```

## Files Included

- `create_database.py` - Python script to create and populate the database
- `create_database.sql` - SQL script with table creation and test data
- `setup_database.bat` - Windows batch script to set up the database
- `customers.db` - The SQLite database file (created after running setup)

