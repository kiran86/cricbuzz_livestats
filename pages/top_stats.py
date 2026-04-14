import pandas as pd
import streamlit as st

from utils.db_connection import get_connection, initialize_database


st.set_page_config(page_title="Top Player Stats", page_icon="📊", layout="wide")
initialize_database()

st.title("📊 Top Player Stats")
selected_format = st.selectbox("Choose a format", ["ODI", "T20I", "Test"])

with get_connection() as connection:
    top_batters = pd.read_sql_query(
        """
        SELECT
            p.full_name,
            t.team_name,
            s.runs_scored,
            s.batting_average,
            s.strike_rate,
            s.centuries
        FROM player_format_stats s
        JOIN players p ON p.id = s.player_id
        JOIN teams t ON t.id = p.team_id
        WHERE s.format = ?
        ORDER BY s.runs_scored DESC
        LIMIT 10
        """,
        connection,
        params=(selected_format,),
    )

    top_bowlers = pd.read_sql_query(
        """
        SELECT
            p.full_name,
            t.team_name,
            s.wickets_taken,
            s.bowling_average,
            s.economy_rate,
            s.matches_played
        FROM player_format_stats s
        JOIN players p ON p.id = s.player_id
        JOIN teams t ON t.id = p.team_id
        WHERE s.format = ?
        ORDER BY s.wickets_taken DESC, s.economy_rate ASC
        LIMIT 10
        """,
        connection,
        params=(selected_format,),
    )

    fielding_leaders = pd.read_sql_query(
        """
        SELECT
            p.full_name,
            t.team_name,
            s.catches,
            s.stumpings
        FROM player_format_stats s
        JOIN players p ON p.id = s.player_id
        JOIN teams t ON t.id = p.team_id
        WHERE s.format = ?
        ORDER BY (s.catches + s.stumpings) DESC, p.full_name
        LIMIT 10
        """,
        connection,
        params=(selected_format,),
    )

col1, col2 = st.columns(2)
with col1:
    st.subheader("Top Batters")
    st.dataframe(top_batters, use_container_width=True, hide_index=True)
with col2:
    st.subheader("Top Bowlers")
    st.dataframe(top_bowlers, use_container_width=True, hide_index=True)

st.subheader("Fielding Leaders")
st.dataframe(fielding_leaders, use_container_width=True, hide_index=True)
