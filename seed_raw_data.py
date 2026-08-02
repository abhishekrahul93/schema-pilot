import duckdb
import random
from datetime import datetime, timedelta

conn = duckdb.connect("schemapilot.duckdb")
print("?? Creating messy raw tables...")

conn.sql("DROP TABLE IF EXISTS raw_customers; DROP TABLE IF EXISTS raw_products; DROP TABLE IF EXISTS raw_orders; DROP TABLE IF EXISTS raw_order_lines;")

conn.sql("CREATE TABLE raw_customers (customer_id VARCHAR, name VARCHAR, email VARCHAR, country VARCHAR, signup_date VARCHAR);")
first_names = ["Alice", "Bob", "Charlie", "Diana", "Evan", "Fiona", "George", "Hannah"]
last_names = ["Smith", "Jones", "Taylor", "Brown", "Wilson", "Davis", "Miller", "Moore"]
countries = ["USA", "United States", "usa", "Canada", "UK", "   ", "", None, "Germany"]

customers_data = []
for i in range(1, 819):
    c_id = f"CUST_{i:04d}"
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    email_base = name.lower().replace(" ", ".")
    if i % 15 == 0: email = f" {email_base}@gmail.com "
    elif i % 25 == 0: email = email_base.upper() + "@YAHOO.COM"
    elif i % 50 == 0: email = None
    else: email = f"{email_base}@example.com"
    country = random.choice(countries)
    signup_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
    customers_data.append((c_id, name, email, country, signup_date))

for _ in range(30): customers_data.append(random.choice(customers_data))
conn.executemany("INSERT INTO raw_customers VALUES (?, ?, ?, ?, ?)", customers_data)

conn.sql("CREATE TABLE raw_products (product_id VARCHAR, product_name VARCHAR, category VARCHAR, price DECIMAL(10,2), cost DECIMAL(10,2));")
categories = ["Electronics", "Apparel", "Home & Kitchen", "Books"]
products_data = []
for i in range(1, 151):
    p_id = f"PROD_{i:03d}"
    price = round(random.uniform(10.0, 500.0), 2)
    products_data.append((p_id, f"Product {i}", random.choice(categories), price, round(price * 0.5, 2)))
conn.executemany("INSERT INTO raw_products VALUES (?, ?, ?, ?, ?)", products_data)

conn.sql("CREATE TABLE raw_orders (order_id VARCHAR, customer_id VARCHAR, order_date VARCHAR, status VARCHAR);")
orders_data = [(f"ORD_{i:05d}", random.choice([c[0] for c in customers_data]), (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d %H:%M:%S"), random.choice(["completed", "shipped", "cancelled", "COMPLETED"])) for i in range(1, 6001)]
conn.executemany("INSERT INTO raw_orders VALUES (?, ?, ?, ?)", orders_data)

conn.sql("CREATE TABLE raw_order_lines (line_id VARCHAR, order_id VARCHAR, product_id VARCHAR, quantity INTEGER);")
lines_data = []
line_counter = 1
for o in orders_data:
    for _ in range(random.randint(1, 4)):
        p_id = "PROD_999" if random.random() < 0.05 else random.choice([p[0] for p in products_data])
        lines_data.append((f"LINE_{line_counter:06d}", o[0], p_id, random.randint(1, 5)))
        line_counter += 1
conn.executemany("INSERT INTO raw_order_lines VALUES (?, ?, ?, ?)", lines_data)

print("? Messy raw data successfully seeded into schemapilot.duckdb!")
conn.close()
