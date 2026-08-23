import os
import yaml
import duckdb
import time
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

def init_audit_table(db_path="schemapilot.duckdb"):
    conn = duckdb.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS agent_audit_logs (
            timestamp TIMESTAMP,
            question VARCHAR,
            generated_sql VARCHAR,
            status VARCHAR,
            latency_ms DOUBLE,
            error_message VARCHAR
        )
    """)
    conn.close()

def log_audit_event(question, sql, status, latency, error=None, db_path="schemapilot.duckdb"):
    conn = duckdb.connect(db_path)
    conn.execute("""
        INSERT INTO agent_audit_logs VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now(), question, sql, status, latency, error))
    conn.close()

def load_schema_context():
    with open("schema_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    context_str = "Available Tables:\n"
    for table_name, details in config.get("tables", {}).items():
        context_str += f"- {table_name} ({details['type']}): columns -> {list(details['columns'].keys())}\n"
    return context_str

def run_audited_agent(question: str):
    init_audit_table()
    start_time = time.time()
    
    print(f"\n?? [Audited Self-Healing Swarm] Processing: '{question}'")
    print("=" * 60)
    
    schema_context = load_schema_context()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Step 1 & 2: Plan & Generate SQL
    architect_prompt = f"You are a Data Architect. Plan the query for the question using this schema:\n{schema_context}"
    plan_res = llm.invoke([SystemMessage(content=architect_prompt), HumanMessage(content=question)])
    
    coder_prompt = f"""
    You are an expert SQL Engineer. Write valid DuckDB SQL based on the plan.
    Always use LIMIT 10 unless specified otherwise. Output ONLY raw SQL inside a markdown block.
    Schema:\n{schema_context}
    Plan: {plan_res.content}
    """
    sql_res = llm.invoke([SystemMessage(content=coder_prompt), HumanMessage(content=question)])
    
    raw_content = sql_res.content
    if "`sql" in raw_content:
        sql_query = raw_content.split("`sql")[1].split("`")[0].strip()
    elif "`" in raw_content:
        sql_query = raw_content.split("`")[1].split("`")[0].strip()
    else:
        sql_query = raw_content.strip()

    # Step 3: Critic Safety Audit
    bad_keywords = ["drop", "delete", "update", "truncate", "alter"]
    if any(kw in sql_query.lower() for kw in bad_keywords):
        latency = (time.time() - start_time) * 1000
        log_audit_event(question, sql_query, "BLOCKED_SECURITY", latency, "Destructive operation blocked")
        print("? [Critic Alert] Destructive operation blocked and logged to telemetry!")
        return

    # Step 4: Execution with Self-Correction & Logging
    max_retries = 3
    conn = duckdb.connect("schemapilot.duckdb", read_only=True)
    final_status = "FAILED"
    last_error = None
    
    for attempt in range(1, max_retries + 1):
        print(f"\n?? [Execution Attempt {attempt}/{max_retries}] Running SQL:\n{sql_query}")
        try:
            results = conn.execute(sql_query).fetchall()
            print("? Execution Successful!")
            print("?? Results:")
            for r in results:
                print(f"   {r}")
            final_status = "SUCCESS"
            break
        except Exception as e:
            last_error = str(e)
            print(f"?? [Error Caught]: {e}")
            if attempt == max_retries:
                print("? Max retries reached.")
                break
            
            fix_prompt = f"""
            The previous SQL query failed with this database error: {e}
            Original Question: {question}
            Failed SQL: {sql_query}
            Fix the SQL query so it is valid DuckDB syntax. Output ONLY raw SQL inside a markdown block.
            """
            fix_res = llm.invoke([SystemMessage(content="You are an expert SQL debugger."), HumanMessage(content=fix_prompt)])
            fixed_content = fix_res.content
            if "`sql" in fixed_content:
                sql_query = fixed_content.split("`sql")[1].split("`")[0].strip()
            elif "`" in fixed_content:
                sql_query = fixed_content.split("`")[1].split("`")[0].strip()
            else:
                sql_query = fixed_content.strip()

    conn.close()
    
    # Record telemetry latency & outcome
    total_latency = (time.time() - start_time) * 1000
    log_audit_event(question, sql_query, final_status, total_latency, last_error)
    print(f"\n?? Telemetry Logged: Status={final_status} | Latency={total_latency:.2f}ms")
    print("? Workflow & Audit Complete!")

if __name__ == "__main__":
    run_audited_agent("What are the top 3 countries with the highest total order quantity?")
