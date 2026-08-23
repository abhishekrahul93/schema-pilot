import os
import yaml
import duckdb
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase

def load_schema_context(config_path="schema_config_alt.yaml"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"? Could not find {config_path}.")
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    context_str = f"Database Type: DuckDB\nDatabase Name: {config.get('database')}\n\nAvailable Tables and Views:\n"
    for table_name, details in config.get("tables", {}).items():
        context_str += f"- Table/View: {table_name} ({details['type']})\n  Columns:\n"
        for col_name, col_info in details['columns'].items():
            samples = ", ".join([str(s) for s in col_info['sample_values']])
            context_str += f"    * {col_name} ({col_info['data_type']}) | Sample values: [{samples}]\n"
    return context_str

def run_agent(question: str):
    # Load the ALTERNATE schema configuration
    schema_context = load_schema_context("schema_config_alt.yaml")
    
    # Connect to the ALTERNATE database file
    db = SQLDatabase.from_uri("duckdb:///schemapilot_alt.duckdb")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    system_prompt = f"""
You are SchemaPilot, an expert Forward Deployed AI Data Analyst agent.
You answer user questions by writing and executing SQL queries against the DuckDB database.

Here is the exact schema metadata configuration loaded for this environment:
{schema_context}

RULES:
1. Use the tables and columns available in the loaded metadata configuration above.
2. Write syntactically correct DuckDB SQL.
3. Limit results to 10 rows unless requested otherwise.
4. Explain your findings clearly to the user based on the query results.
"""

    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="tool-calling",
        verbose=True,
        prefix=system_prompt
    )
    
    print(f"\n?? Question: {question}")
    print("-" * 50)
    response = agent_executor.invoke({"input": question})
    print("-" * 50)
    print(f"?? Answer:\n{response['output']}")

if __name__ == "__main__":
    # Asking a similar business question, but the table schema is completely different!
    test_question = "What are the top 3 regions with the highest total item count?"
    run_agent(test_question)
