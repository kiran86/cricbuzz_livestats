import pandas as pd
import streamlit as st

from sql.queries import SQL_QUERIES
from utils.db_connection import get_connection, initialize_database


st.set_page_config(page_title="SQL Analytics", page_icon="🧮", layout="wide")
initialize_database()

st.title("🧮 SQL Queries & Analytics")
st.caption("This page includes the 25 guided SQL questions from the assignment and a custom SQL runner.")

query_options = {
    f"Q{number}. {config['title']} ({config['level']})": number
    for number, config in SQL_QUERIES.items()
}
selected_label = st.selectbox("Choose a predefined analytics query", list(query_options.keys()))
selected_number = query_options[selected_label]
selected_query = SQL_QUERIES[selected_number]

st.code(selected_query["sql"].strip(), language="sql")

with get_connection() as connection:
    result = pd.read_sql_query(selected_query["sql"], connection)

st.dataframe(result, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Custom SQL Runner")
custom_sql = st.text_area(
    "Write your own read-only SQL query",
    value="SELECT full_name, playing_role, country FROM players ORDER BY full_name LIMIT 10;",
    height=180,
)

if st.button("Run Custom Query"):
    if not custom_sql.strip().lower().startswith("select"):
        st.error("Only SELECT statements are allowed in the custom runner.")
    else:
        try:
            with get_connection() as connection:
                custom_result = pd.read_sql_query(custom_sql, connection)
            st.dataframe(custom_result, use_container_width=True, hide_index=True)
        except Exception as exc:  # pragma: no cover - Streamlit feedback
            st.error(f"Query failed: {exc}")
