from pathlib import Path

import streamlit as st

from utils.db_connection import initialize_database


st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")
initialize_database()

st.title("🏠 Project Home")
st.caption("Overview, tools used, and navigation for the Cricbuzz LiveStats project.")

st.markdown(
    """
This project delivers a multi-page cricket analytics dashboard with:

- live and recent match information
- top batting, bowling, and fielding leaderboards
- 25 SQL practice and analytics queries
- player CRUD operations using SQLite
"""
)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Modules")
    st.write("- `live_matches.py` for live match tracking")
    st.write("- `top_stats.py` for player leaderboards")
    st.write("- `sql_queries.py` for analytics and custom SQL")
    st.write("- `crud_operations.py` for player management")

with col2:
    st.subheader("Stack")
    st.write("- Python")
    st.write("- Streamlit")
    st.write("- SQLite")
    st.write("- pandas")
    st.write("- requests")

st.subheader("Run the App")
st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")

readme_path = Path(__file__).resolve().parents[1] / "README.md"
st.markdown(f"See [README.md]({readme_path}) for setup details.")
