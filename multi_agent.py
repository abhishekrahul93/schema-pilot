import os
import yaml
import duckdb
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

def load_schema_context():
    with open("schema_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    context_str = "Available Tables:\n"
    for table_name, details in config.get("tables", {}).items():
        context_str += f"- {table_name} ({details['type']}): columns -> {list(details['columns'].keys())}\n"
    return context_str

def run_multi_agent_pipeline(question: str):
    print(f"\n?? [Multi-Agent Swarm] Processing Question: '{question}'")
    print("=" * 60)
    
    schema_context = load_schema_context()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # --- STEP 1: THE ARCHITECT (Planning & Table Selection) ---
    print("??? [Agent 1: The Architect] Analyzing schema and planning query route...")
    architect_prompt = f"""
    You are an expert Data Architect. Given the user question and schema metadata, 
    determine which tables and columns are required.
    
    Schema:
    {schema_context}
    
    User Question: {question}
    
    Output a concise execution plan.
    """
    plan_response = llm.invoke([SystemMessage(content=architect_prompt), HumanMessage(content=question)])
    print(f"?? Plan:\n{plan_response.content}\n")
    
    # --- STEP 2: THE CODER (SQL Generation) ---
    print("?? [Agent 2: The Coder] Writing DuckDB SQL based on the plan...")
    coder_prompt = f"""
    You are an expert SQL Engineer. Write a valid DuckDB SQL query based on the plan.
    Always use LIMIT 10 unless specified otherwise. Output ONLY the raw SQL code inside a markdown block.
    
    Schema:
    {schema_context}
    Plan: {plan_response.content}
    """
    sql_response = llm.invoke([SystemMessage(content=coder_prompt), HumanMessage(content=question)])
    
    # Extract SQL from markdown block
    raw_content = sql_response.content
    if "`sql" in raw_content:
        sql_query = raw_content.split("`sql")[1].split("`")[0].strip()
    elif "`" in raw_content:
        sql_query = raw_content.split("`")[1].split("`")[0].strip()
    else:
        sql_query = raw_content.strip()
        
    print(f"?? Generated SQL:\n{sql_query}\n")
    
    # --- STEP 3: THE CRITIC (Safety & Validation Audit) ---
    print("??? [Agent 3: The Critic] Auditing SQL for safety and correctness...")
    bad_keywords = ["drop", "delete", "update", "truncate", "alter"]
    if any(kw in sql_query.lower() for kw in bad_keywords):
        print("? [Critic Alert] Destructive operation detected and blocked!")
        return
    else:
        print("? [Critic Audit] Query passed safety checks. Executing against DuckDB...\n")
        
    # --- EXECUTION ---
    try:
        conn = duckdb.connect("schemapilot.duckdb", read_only=True)
        results = conn.execute(sql_query).fetchall()
        conn.close()
        
        print("?? Execution Results:")
        for r in results:
            print(f"   {r}")
            
        print("\n? Multi-Agent Workflow Completed Successfully!")
    except Exception as e:
        print(f"? Execution Error: {e}")

if __name__ == "__main__":
    # Test complex multi-step question
    test_q = "What are the top 3 countries with the highest total order quantity?"
    run_multi_agent_pipeline(test_q)
