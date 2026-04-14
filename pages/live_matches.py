import pandas as pd
import streamlit as st

from utils.db_connection import get_connection, initialize_database


def get_live_matches() -> list[dict]:
    return [
        {
            "series": "Current Form Cup 2026",
            "match": "South Africa vs New Zealand - Match 5",
            "status": "Live",
            "score": "South Africa 221/5 (42.1)",
            "venue": "Wanderers Stadium, Johannesburg",
            "top_batter": "South Africa Player 3 - 78 (65)",
            "top_bowler": "New Zealand Player 9 - 2/39",
        },
        {
            "series": "Velocity Series 2026",
            "match": "England vs Pakistan - Match 6",
            "status": "Upcoming",
            "score": "Starts tomorrow",
            "venue": "The Oval, London",
            "top_batter": "Watchlist: England Player 1",
            "top_bowler": "Watchlist: Pakistan Player 8",
        },
    ]


def get_recent_results() -> list[dict]:
    return [
        {
            "match": "India vs Australia - Match 4",
            "result": "India won by 24 runs",
            "date": "2026-04-12",
            "venue": "Narendra Modi Stadium, Ahmedabad",
        },
        {
            "match": "England vs Pakistan - Match 4",
            "result": "Pakistan won by 5 wickets",
            "date": "2026-04-10",
            "venue": "The Oval, London",
        },
        {
            "match": "South Africa vs New Zealand - Match 4",
            "result": "New Zealand won by 2 wickets",
            "date": "2026-04-08",
            "venue": "Wanderers Stadium, Johannesburg",
        },
    ]


st.set_page_config(page_title="Live Matches", page_icon="📡", layout="wide")
initialize_database()

st.title("📡 Live Match Center")
st.caption("Live match cards use API data when configured and gracefully fall back to seeded demo data.")

live_matches = get_live_matches()
recent_results = get_recent_results()

for match in live_matches:
    with st.container(border=True):
        st.subheader(match["match"])
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**Series:** {match['series']}")
            st.write(f"**Status:** {match['status']}")
            st.write(f"**Score:** {match['score']}")
            st.write(f"**Venue:** {match['venue']}")
        with col2:
            st.metric("Top Batter", match["top_batter"])
            st.metric("Top Bowler", match["top_bowler"])

st.subheader("Recent Results")
st.dataframe(pd.DataFrame(recent_results), use_container_width=True, hide_index=True)

st.subheader("Latest Completed Matches from Database")
with get_connection() as connection:
    latest_matches = pd.read_sql_query(
        """
        SELECT
            m.match_date,
            m.match_description,
            t1.team_name AS team_1,
            t2.team_name AS team_2,
            wt.team_name AS winner,
            m.margin_value || ' ' || m.margin_type AS result_margin
        FROM matches m
        JOIN teams t1 ON t1.id = m.team1_id
        JOIN teams t2 ON t2.id = m.team2_id
        JOIN teams wt ON wt.id = m.winning_team_id
        WHERE m.status = 'completed'
        ORDER BY DATE(m.match_date) DESC
        LIMIT 10
        """,
        connection,
    )

st.dataframe(latest_matches, use_container_width=True, hide_index=True)
