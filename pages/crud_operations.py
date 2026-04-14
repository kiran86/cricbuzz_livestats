import pandas as pd
import streamlit as st

from utils.db_connection import get_connection, initialize_database


st.set_page_config(page_title="CRUD Operations", page_icon="🛠️", layout="wide")
initialize_database()

st.title("🛠️ Player CRUD Operations")

with get_connection() as connection:
    teams = pd.read_sql_query(
        "SELECT id, team_name FROM teams ORDER BY team_name",
        connection,
    )

team_lookup = dict(zip(teams["team_name"], teams["id"]))
team_names = teams["team_name"].tolist()

tab_create, tab_update, tab_delete, tab_view = st.tabs(["Create", "Update", "Delete", "View"])

with tab_create:
    with st.form("create_player_form"):
        full_name = st.text_input("Full name")
        team_name = st.selectbox("Team", team_names, key="create_team")
        playing_role = st.selectbox("Playing role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        batting_style = st.selectbox("Batting style", ["Right-hand bat", "Left-hand bat"])
        bowling_style = st.text_input("Bowling style", value="Part-time spin")
        submitted = st.form_submit_button("Add Player")

    if submitted:
        with get_connection() as connection:
            country = connection.execute(
                "SELECT country FROM teams WHERE id = ?",
                (team_lookup[team_name],),
            ).fetchone()["country"]
            connection.execute(
                """
                INSERT INTO players(full_name, team_id, country, playing_role, batting_style, bowling_style)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (full_name, team_lookup[team_name], country, playing_role, batting_style, bowling_style),
            )
            connection.commit()
        st.success(f"Added {full_name} to {team_name}.")

with tab_update:
    with get_connection() as connection:
        players = pd.read_sql_query(
            """
            SELECT p.id, p.full_name, t.team_name, p.playing_role, p.batting_style, p.bowling_style
            FROM players p
            JOIN teams t ON t.id = p.team_id
            ORDER BY p.full_name
            """,
            connection,
        )

    player_options = {
        f"{row.full_name} ({row.team_name})": row.id
        for row in players.itertuples(index=False)
    }
    selected_player_label = st.selectbox("Choose a player to update", list(player_options.keys()))
    selected_player_id = player_options[selected_player_label]
    current_row = players.loc[players["id"] == selected_player_id].iloc[0]

    with st.form("update_player_form"):
        updated_name = st.text_input("Full name", value=current_row["full_name"])
        updated_team = st.selectbox("Team", team_names, index=team_names.index(current_row["team_name"]))
        updated_role = st.selectbox(
            "Playing role",
            ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"],
            index=["Batsman", "Bowler", "All-rounder", "Wicket-keeper"].index(current_row["playing_role"]),
        )
        updated_batting = st.selectbox(
            "Batting style",
            ["Right-hand bat", "Left-hand bat"],
            index=["Right-hand bat", "Left-hand bat"].index(current_row["batting_style"]),
        )
        updated_bowling = st.text_input("Bowling style", value=current_row["bowling_style"])
        update_submitted = st.form_submit_button("Update Player")

    if update_submitted:
        with get_connection() as connection:
            team_id = team_lookup[updated_team]
            country = connection.execute(
                "SELECT country FROM teams WHERE id = ?",
                (team_id,),
            ).fetchone()["country"]
            connection.execute(
                """
                UPDATE players
                SET full_name = ?, team_id = ?, country = ?, playing_role = ?, batting_style = ?, bowling_style = ?
                WHERE id = ?
                """,
                (updated_name, team_id, country, updated_role, updated_batting, updated_bowling, selected_player_id),
            )
            connection.commit()
        st.success(f"Updated {updated_name}.")

with tab_delete:
    with get_connection() as connection:
        players_for_delete = pd.read_sql_query(
            """
            SELECT p.id, p.full_name, t.team_name
            FROM players p
            JOIN teams t ON t.id = p.team_id
            ORDER BY p.full_name
            """,
            connection,
        )

    delete_options = {
        f"{row.full_name} ({row.team_name})": row.id
        for row in players_for_delete.itertuples(index=False)
    }
    delete_label = st.selectbox("Choose a player to delete", list(delete_options.keys()))
    if st.button("Delete Player", type="primary"):
        player_id = delete_options[delete_label]
        with get_connection() as connection:
            connection.execute("DELETE FROM player_format_stats WHERE player_id = ?", (player_id,))
            connection.execute("DELETE FROM fielding_scorecards WHERE player_id = ?", (player_id,))
            connection.execute("DELETE FROM bowling_scorecards WHERE player_id = ?", (player_id,))
            connection.execute("DELETE FROM batting_scorecards WHERE player_id = ?", (player_id,))
            connection.execute("DELETE FROM players WHERE id = ?", (player_id,))
            connection.commit()
        st.warning(f"Deleted {delete_label}.")

with tab_view:
    with get_connection() as connection:
        player_table = pd.read_sql_query(
            """
            SELECT
                p.full_name,
                t.team_name,
                p.country,
                p.playing_role,
                p.batting_style,
                p.bowling_style
            FROM players p
            JOIN teams t ON t.id = p.team_id
            ORDER BY t.team_name, p.full_name
            """,
            connection,
        )

    st.dataframe(player_table, use_container_width=True, hide_index=True)
