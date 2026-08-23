import duckdb
import yaml
import os
from decimal import Decimal

def extract_schema_metadata(db_path="schemapilot_alt.duckdb", output_path="schema_config_alt.yaml"):
    print(f"?? Connecting to DuckDB at {db_path}...")
    conn = duckdb.connect(db_path, read_only=True)
    
    tables_query = """
        SELECT table_name, table_type 
        FROM information_schema.tables 
        WHERE table_schema = 'main'
    """
    tables = conn.execute(tables_query).fetchall()
    
    schema_dict = {
        "database": "schemapilot_alt",
        "tables": {}
    }
    
    for table_name, table_type in tables:
        print(f"?? Inspecting {table_type}: {table_name}...")
        
        columns_query = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'main' AND table_name = '{table_name}'
            ORDER BY ordinal_position
        """
        columns = conn.execute(columns_query).fetchall()
        
        cols_dict = {}
        for col_name, data_type, is_nullable in columns:
            try:
                sample_query = f'SELECT DISTINCT "{col_name}" FROM "{table_name}" WHERE "{col_name}" IS NOT NULL LIMIT 3'
                raw_samples = [row[0] for row in conn.execute(sample_query).fetchall()]
                samples = [float(s) if isinstance(s, Decimal) else s for s in raw_samples]
            except Exception:
                samples = []
                
            cols_dict[col_name] = {
                "data_type": data_type,
                "nullable": is_nullable == 'YES',
                "sample_values": samples
            }
            
        schema_dict["tables"][table_name] = {
            "type": table_type.lower(),
            "columns": cols_dict
        }
        
    conn.close()
    
    with open(output_path, "w") as f:
        yaml.dump(schema_dict, f, sort_keys=False, default_flow_style=False)
        
    print(f"? Metadata successfully extracted and saved to {output_path}!")

if __name__ == "__main__":
    extract_schema_metadata()
