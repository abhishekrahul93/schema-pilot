import duckdb
import random
from datetime import datetime, timedelta

def create_alt_db():
    db_path = "schemapilot_alt.duckdb"
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = duckdb.connect(db_path)
    
    print("?? Creating alternate schema database (schemapilot_alt.duckdb)...")
    
    # Completely different table name and schema design
    conn.execute("""
        CREATE TABLE sales_ledger (
            transaction_id VARCHAR,
            client_id VARCHAR,
            client_name VARCHAR,
            destination_region VARCHAR,
            purchase_timestamp TIMESTAMP,
            item_count INTEGER,
            order_status VARCHAR
        )
    """)
    
    countries = ['North America', 'Europe', 'Asia', 'Unknown']
    statuses = ['completed', 'pending', 'cancelled']
    
    # Insert mock records
    data = []
    for i in range(1, 500):
        tid = f"TXN_{i:05d}"
        cid = f"CL_{random.randint(1, 50):03d}"
        cname = f"Client {random.randint(1, 50)}"
        region = random.choice(countries)
        ts = datetime.now() - timedelta(days=random.randint(1, 100))
        items = random.randint(1, 10)
        status = random.choice(statuses)
        data.append((tid, cid, cname, region, ts, items, status))
        
    conn.executemany("INSERT INTO sales_ledger VALUES (?, ?, ?, ?, ?, ?, ?)", data)
    conn.close()
    print("? Alternate database created successfully!")

if __name__ == "__main__":
    import os
    create_alt_db()
