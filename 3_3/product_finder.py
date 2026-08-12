"""
Exercise: The Product Finder
Module 3 | Lesson 3 | ~30 min

Objective:
  Practice writing SQL queries using WHERE, AND, ORDER BY, LIMIT, and LIKE
  to filter and sort data from a products table.
"""

import sqlite3

# ── Database setup (provided — do not modify) ─────────────────────────────────
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

conn.executescript("""
    CREATE TABLE products (
        id         INTEGER PRIMARY KEY,
        name       TEXT    NOT NULL,
        category   TEXT    NOT NULL,
        price      REAL    NOT NULL,
        stock      INTEGER NOT NULL DEFAULT 0,
        on_sale    INTEGER NOT NULL DEFAULT 0   -- 1 = on sale, 0 = regular price
    );

    INSERT INTO products VALUES
      (1,  'Wireless Headphones',    'Electronics', 79.99,  45,  1),
      (2,  'Mechanical Keyboard',    'Electronics', 129.99, 12,  0),
      (3,  'USB-C Hub',              'Electronics', 39.99,  0,   1),
      (4,  'Running Shoes',          'Apparel',     89.99,  30,  0),
      (5,  'Yoga Mat',               'Sports',      34.99,  75,  1),
      (6,  'Stainless Water Bottle', 'Sports',      24.99,  100, 0),
      (7,  'Leather Wallet',         'Accessories', 49.99,  20,  0),
      (8,  'Sunglasses',             'Accessories', 69.99,  0,   1),
      (9,  'Python Programming Book','Books',       44.99,  8,   0),
      (10, 'SQL for Beginners',      'Books',       29.99,  15,  1),
      (11, 'Standing Desk',          'Furniture',   299.99, 5,   0),
      (12, 'Ergonomic Chair',        'Furniture',   449.99, 3,   1),
      (13, 'Bluetooth Speaker',      'Electronics', 59.99,  22,  0),
      (14, 'Smartwatch',             'Electronics', 199.99, 0,   0),
      (15, 'Notebook Set',           'Stationery',  12.99,  200, 1);
""")
conn.commit()


# ── Queries — write the SQL for each one ─────────────────────────────────────

# 1. Products that are out of stock (stock = 0)
print("1. Out of stock products:")
# TODO: write the SQL query
# query1 = "SELECT ..."
# for row in conn.execute(query1):
#     print(f"   {row['name']} ({row['category']})")
query1 = ("SELECT name, category FROM products WHERE stock = 0") #select name and category from product table where the stock is 0.
for row in conn.execute(query1): #runs the query
    print(f"{row['name']} ({row['category']})") #prints the data

# 2. Electronics under $100, ordered by price ascending
print("2. Electronics under $100 (cheapest first):")
# TODO: write the SQL query using WHERE with AND
# query2 = "SELECT ..."
# for row in conn.execute(query2):
#     print(f"   ${row['price']:.2f}  {row['name']}")
query2 = ("SELECT name, price FROM products WHERE price < 100 ORDER BY price")# select namme and price (the starter data didnt include ratings but the assignment had ratings. i went with what the starter code had) from product table where price is less than 100 and is sorted by smallest value first
for row in conn.execute(query2): #runs the query
    print(f"${row['price']:.2f} {row['name']}") #prints the data

# 3. The 3 most expensive products overall
print("3. Top 3 most expensive products:")
# TODO: write the SQL query using ORDER BY and LIMIT
# query3 = "SELECT ..."
# for row in conn.execute(query3):
#     print(f"   {row['name']} — ${row['price']:.2f}")
query3 = ("SELECT name, price FROM products WHERE category IN ('Accessories') ORDER BY price DESC LIMIT 3") #selects the name and price from products table where the item is an accessory its ordered by most expensive price and is limited to top 3
for row in conn.execute(query3): #runs query
    print(f"{row['name']} - ${row['price']:.2f}") #prints results. FYI there are only 2 accessories listed for this. 

# 4. Products currently on sale (on_sale = 1) with stock > 0
#NOTE: THIS QUESTION DIFFERS FROM WHAT IS ASKED ONLINE. I COMPLETED AS THE STARTER CODE INSTRUCTS NOT THE ASSIGNMENT ONLINE
print("4. On-sale products that are in stock:")
# TODO: write the SQL query using WHERE with AND
# query4 = "SELECT ..."
# for row in conn.execute(query4):
#     print(f"   {row['name']} — ${row['price']:.2f}  (stock: {row['stock']})")
query4 = ("SELECT * FROM products WHERE on_sale = 1 AND stock > 0")
for row in conn.execute(query4):#I USED THE PARAMETERS OF THE SORT FROM THE ORIGINAL TASK FROM ONLINE DIRECTIONS (IE ALL COLUMNS)
    print(f" {row['name']} - ${row['price']:.2f} (stock: {row['stock']})")

# 5. Products whose name contains the word "book" (case-insensitive)
#NOTE: THIS QUESTION DIFFERS FROM WHAT IS ASKED ONLINE. I COMPLETED AS THE STARTER CODE INSTRUCTS NOT THE ASSIGNMENT ONLINE
print("5. Products matching 'book':")
# TODO: write the SQL query using LIKE
# query5 = "SELECT ..."
# for row in conn.execute(query5):
#     print(f"   {row['name']}")
query5 = ("SELECT name FROM products WHERE name LIKE '%book%'")#i used book anywhere not just a singluar word hence why notebook populates
for row in conn.execute(query5):
    print(f"   {row['name']}")

conn.close()

# Expected output (sample):
# 1. Out of stock products:
#    USB-C Hub (Electronics)
#    Sunglasses (Accessories)
#    Smartwatch (Electronics)
#
# 2. Electronics under $100 (cheapest first):
#    $39.99  USB-C Hub
#    $59.99  Bluetooth Speaker
#    $79.99  Wireless Headphones
#
# 3. Top 3 most expensive products:
#    Ergonomic Chair — $449.99
#    Standing Desk — $299.99
#    Smartwatch — $199.99
#
# 4. On-sale products that are in stock:
#    Wireless Headphones — $79.99  (stock: 45)
#    Yoga Mat — $34.99  (stock: 75)
#    SQL for Beginners — $29.99  (stock: 15)
#    Ergonomic Chair — $449.99  (stock: 3)
#    Notebook Set — $12.99  (stock: 200)
#
# 5. Products matching 'book':
#    Python Programming Book
#    SQL for Beginners      <- contains "book" ... wait, it doesn't.
#    (only rows whose name contains the substring "book")