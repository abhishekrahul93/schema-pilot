import os
import yaml
import duckdb
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

def load_schema_context():
    if not os.path.exists("schema_config.yaml"):
        return "Schema config not found."
    with open("schema_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    context_str = "Available Tables:\n"
    for table_name, details in config.get("tables", {}).items():
        context_str += f"- {table_name} ({details['type']}): columns -> {list(details['columns'].keys())}\n"
    return context_str

def run_self_healing_swarm(question: str):
    print(f"\n🤖 [Self-Healing Swarm] Processing: '{question}'")
    print("=" * 60)
    
    schema_context = load_schema_context()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    print("🏛️ [Agent 1: The Architect] Planning query route...")
    architect_prompt = f"You are a Data Architect. Plan the query route using this schema:\n{schema_context}"
    plan_res = llm.invoke([SystemMessage(content=architect_prompt), HumanMessage(content=question)])
    
    print("💻 [Agent 2: The Coder] Writing DuckDB SQL...")
    coder_prompt = f"""
    You are an expert SQL Engineer. Write valid DuckDB SQL based on the plan.
    Always use LIMIT 10 unless specified otherwise. Output ONLY raw SQL inside a markdown block.
    Schema:
    {schema_context}
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

    print("🛡️ [Agent 3: The Critic] Auditing safety...")
    if any(kw in sql_query.lower() for kw in ["drop", "delete", "update", "truncate", "alter"]):
        print("❌ [Critic Alert] Destructive operation blocked!")
        return

    conn = duckdb.connect("schemapilot.duckdb", read_only=True)
    for attempt in range(1, 4):
        print(f"\n⚙️ [Execution Attempt {attempt}/3] Running SQL:\n{sql_query}")
        try:
            results = conn.execute(sql_query).fetchall()
            print("✅ Execution Successful!\n📊 Results:")
            for row in results:
                print(f"   {row}")
            break
        except Exception as e:
            print(f"⚠️ [Auto-Repair] Error caught: {e}")
            if attempt == 3:
                print("❌ Max retries reached.")
                break
            fix_res = llm.invoke([
                SystemMessage(content="You are an expert SQL debugger."),
                HumanMessage(content=f"Fix this failed DuckDB SQL error: {e}. Question: {question}. Failed SQL: {sql_query}. Output ONLY raw SQL inside a markdown block.")
            ])
            fixed = fix_res.content
            sql_query = fixed.split("`sql")[1].split("`")[0].strip() if "`sql" in fixed else fixed.strip()

    conn.close()
    print("\n✨ Workflow Complete!")

if __name__ == "__main__":
    run_self_healing_swarm("What are the top 3 countries with the highest total order quantity?")
