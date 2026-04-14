import streamlit as st

from utils.db_connection import initialize_database


st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_database()

st.title("🏏 Cricbuzz LiveStats")
st.caption("Main entry point for the Streamlit app.")

st.markdown(
    """
Use the sidebar to explore the project pages:

- `Live Matches`: API-backed live match cards with offline fallback data.
- `Top Player Stats`: Format-wise batting and bowling leaderboards.
- `SQL Analytics`: 25 guided cricket analytics SQL questions plus a custom query runner.
- `CRUD Operations`: Create, update, and delete player records in the SQLite database.
- `Home`: project overview, architecture, and setup notes.
"""
)

st.subheader("Quick Start")
st.code(
    "pip install -r requirements.txt\nstreamlit run app.py",
    language="bash",
)
st.info("Open `pages/home.py` for the detailed project overview.")
