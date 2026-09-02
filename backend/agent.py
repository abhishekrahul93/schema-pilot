import os
import duckdb

def run_agent_query(question: str) -> dict:
    db_path = os.path.join(os.path.dirname(__file__), "schemapilot.duckdb")
    try:
        conn = duckdb.connect(db_path, read_only=True)
        result = conn.execute("SELECT * FROM fct_orders LIMIT 5").fetchall()
        conn.close()
        return {
            "status": "success",
            "question": question,
            "data_sample": str(result),
            "message": "Executed via SchemaPilot agent module."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database execution failed: {str(e)}"
        }
