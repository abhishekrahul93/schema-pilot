
import streamlit as st
import httpx

st.set_page_config(page_title="SchemaPilot Dashboard", layout="wide")

st.title("??? SchemaPilot: Autonomous SQL & Governance Engine")
st.markdown("Query your data using natural language, backed by automated LLM evaluations and strict safety guards.")

prompt = st.text_input("Enter your analytical question:", "Show me the schema details or run an audit.")

if st.button("Execute Agent Action"):
    with st.spinner("SchemaPilot Agent is processing..."):
        try:
            response = httpx.post("http://localhost:8000/agent", json={"parameters": {"question": prompt}}, timeout=30.0)
            if response.status_code == 200:
                data = response.json()
                st.success("Action Executed Successfully!")
                st.json(data)
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Could not connect to FastAPI backend: {e}")

