from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta
import json
import random

from utils.db_connection import get_connection


TEAM_DEFINITIONS = [
    ("India", "India"),
    ("Australia", "Australia"),
    ("England", "England"),
    ("Pakistan", "Pakistan"),
    ("South Africa", "South Africa"),
    ("New Zealand", "New Zealand"),
    ("Sri Lanka", "Sri Lanka"),
    ("West Indies", "West Indies"),
]

ROLE_BY_SLOT = {
    1: "Batsman",
    2: "Batsman",
    3: "Batsman",
    4: "Batsman",
    5: "All-rounder",
    6: "Wicket-keeper",
    7: "All-rounder",
    8: "Bowler",
    9: "Bowler",
    10: "Bowler",
    11: "Bowler",
}

PLAYER_ROSTERS = {
    "India": [
        ("Rohit Sharma", "Batsman", "Right-hand bat", "Part-time off-spin"),
        ("Shubman Gill", "Batsman", "Right-hand bat", "Part-time off-spin"),
        ("Virat Kohli", "Batsman", "Right-hand bat", "Part-time medium"),
        ("Shreyas Iyer", "Batsman", "Right-hand bat", "Leg-break"),
        ("Hardik Pandya", "All-rounder", "Right-hand bat", "Right-arm fast-medium"),
        ("KL Rahul", "Wicket-keeper", "Right-hand bat", "Wicket-keeper"),
        ("Ravindra Jadeja", "All-rounder", "Left-hand bat", "Left-arm orthodox"),
        ("Jasprit Bumrah", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Mohammed Shami", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Kuldeep Yadav", "Bowler", "Left-hand bat", "Left-arm wrist-spin"),
        ("Mohammed Siraj", "Bowler", "Right-hand bat", "Right-arm fast"),
    ],
    "Australia": [
        ("David Warner", "Batsman", "Left-hand bat", "Part-time leg-spin"),
        ("Travis Head", "Batsman", "Left-hand bat", "Part-time off-spin"),
        ("Steve Smith", "Batsman", "Right-hand bat", "Leg-break"),
        ("Marnus Labuschagne", "Batsman", "Right-hand bat", "Leg-break"),
        ("Glenn Maxwell", "All-rounder", "Right-hand bat", "Off-spin"),
        ("Alex Carey", "Wicket-keeper", "Left-hand bat", "Wicket-keeper"),
        ("Mitchell Marsh", "All-rounder", "Right-hand bat", "Right-arm medium-fast"),
        ("Pat Cummins", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Mitchell Starc", "Bowler", "Left-hand bat", "Left-arm fast"),
        ("Adam Zampa", "Bowler", "Right-hand bat", "Leg-break"),
        ("Josh Hazlewood", "Bowler", "Left-hand bat", "Right-arm fast-medium"),
    ],
    "England": [
        ("Jonny Bairstow", "Batsman", "Right-hand bat", "Part-time medium"),
        ("Phil Salt", "Batsman", "Right-hand bat", "Part-time off-spin"),
        ("Joe Root", "Batsman", "Right-hand bat", "Off-spin"),
        ("Harry Brook", "Batsman", "Right-hand bat", "Part-time medium"),
        ("Ben Stokes", "All-rounder", "Left-hand bat", "Right-arm fast-medium"),
        ("Jos Buttler", "Wicket-keeper", "Right-hand bat", "Wicket-keeper"),
        ("Moeen Ali", "All-rounder", "Left-hand bat", "Off-spin"),
        ("Jofra Archer", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Adil Rashid", "Bowler", "Right-hand bat", "Leg-break"),
        ("Mark Wood", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Reece Topley", "Bowler", "Right-hand bat", "Left-arm fast-medium"),
    ],
    "Pakistan": [
        ("Fakhar Zaman", "Batsman", "Left-hand bat", "Slow left-arm orthodox"),
        ("Imam-ul-Haq", "Batsman", "Left-hand bat", "Part-time off-spin"),
        ("Babar Azam", "Batsman", "Right-hand bat", "Part-time off-spin"),
        ("Saud Shakeel", "Batsman", "Left-hand bat", "Part-time off-spin"),
        ("Shadab Khan", "All-rounder", "Right-hand bat", "Leg-break"),
        ("Mohammad Rizwan", "Wicket-keeper", "Right-hand bat", "Wicket-keeper"),
        ("Agha Salman", "All-rounder", "Right-hand bat", "Off-spin"),
        ("Shaheen Shah Afridi", "Bowler", "Left-hand bat", "Left-arm fast"),
        ("Haris Rauf", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Abrar Ahmed", "Bowler", "Right-hand bat", "Leg-break googly"),
        ("Naseem Shah", "Bowler", "Right-hand bat", "Right-arm fast"),
    ],
    "South Africa": [
        ("Reeza Hendricks", "Batsman", "Right-hand bat", "Part-time off-spin"),
        ("Temba Bavuma", "Batsman", "Right-hand bat", "Part-time medium"),
        ("Aiden Markram", "Batsman", "Right-hand bat", "Off-spin"),
        ("Rassie van der Dussen", "Batsman", "Right-hand bat", "Part-time leg-spin"),
        ("Marco Jansen", "All-rounder", "Left-hand bat", "Left-arm fast-medium"),
        ("Quinton de Kock", "Wicket-keeper", "Left-hand bat", "Wicket-keeper"),
        ("Andile Phehlukwayo", "All-rounder", "Right-hand bat", "Right-arm medium-fast"),
        ("Kagiso Rabada", "Bowler", "Left-hand bat", "Right-arm fast"),
        ("Keshav Maharaj", "Bowler", "Right-hand bat", "Left-arm orthodox"),
        ("Lungi Ngidi", "Bowler", "Right-hand bat", "Right-arm fast-medium"),
        ("Anrich Nortje", "Bowler", "Right-hand bat", "Right-arm fast"),
    ],
    "New Zealand": [
        ("Devon Conway", "Batsman", "Left-hand bat", "Wicket-keeper"),
        ("Finn Allen", "Batsman", "Right-hand bat", "Part-time off-spin"),
        ("Kane Williamson", "Batsman", "Right-hand bat", "Off-spin"),
        ("Daryl Mitchell", "Batsman", "Right-hand bat", "Right-arm medium"),
        ("Rachin Ravindra", "All-rounder", "Left-hand bat", "Left-arm orthodox"),
        ("Tom Latham", "Wicket-keeper", "Left-hand bat", "Wicket-keeper"),
        ("Mitchell Santner", "All-rounder", "Left-hand bat", "Left-arm orthodox"),
        ("Matt Henry", "Bowler", "Right-hand bat", "Right-arm fast-medium"),
        ("Lockie Ferguson", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Ish Sodhi", "Bowler", "Right-hand bat", "Leg-break"),
        ("Trent Boult", "Bowler", "Right-hand bat", "Left-arm fast-medium"),
    ],
    "Sri Lanka": [
        ("Pathum Nissanka", "Batsman", "Right-hand bat", "Part-time off-spin"),
        ("Kusal Perera", "Batsman", "Left-hand bat", "Wicket-keeper"),
        ("Kusal Mendis", "Batsman", "Right-hand bat", "Wicket-keeper"),
        ("Charith Asalanka", "Batsman", "Left-hand bat", "Off-spin"),
        ("Dhananjaya de Silva", "All-rounder", "Right-hand bat", "Off-spin"),
        ("Sadeera Samarawickrama", "Wicket-keeper", "Right-hand bat", "Wicket-keeper"),
        ("Wanindu Hasaranga", "All-rounder", "Right-hand bat", "Leg-break"),
        ("Maheesh Theekshana", "Bowler", "Right-hand bat", "Off-spin"),
        ("Dushmantha Chameera", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Dilshan Madushanka", "Bowler", "Left-hand bat", "Left-arm fast-medium"),
        ("Lahiru Kumara", "Bowler", "Right-hand bat", "Right-arm fast"),
    ],
    "West Indies": [
        ("Brandon King", "Batsman", "Right-hand bat", "Part-time off-spin"),
        ("Alick Athanaze", "Batsman", "Left-hand bat", "Off-spin"),
        ("Shai Hope", "Batsman", "Right-hand bat", "Wicket-keeper"),
        ("Nicholas Pooran", "Batsman", "Left-hand bat", "Wicket-keeper"),
        ("Rovman Powell", "All-rounder", "Right-hand bat", "Right-arm medium"),
        ("Johnson Charles", "Wicket-keeper", "Right-hand bat", "Wicket-keeper"),
        ("Romario Shepherd", "All-rounder", "Right-hand bat", "Right-arm medium-fast"),
        ("Jason Holder", "Bowler", "Right-hand bat", "Right-arm fast-medium"),
        ("Alzarri Joseph", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Gudakesh Motie", "Bowler", "Left-hand bat", "Left-arm orthodox"),
        ("Akeal Hosein", "Bowler", "Left-hand bat", "Left-arm orthodox"),
    ],
}

SERIES_BLUEPRINTS = [
    ("Freedom Cup 2023", "India", "ODI", ("India", "Australia"), date(2023, 2, 10), 6),
    ("Ashes White-Ball 2023", "England", "ODI", ("England", "Australia"), date(2023, 4, 5), 6),
    ("Trans-Tasman Clash 2023", "New Zealand", "T20I", ("New Zealand", "South Africa"), date(2023, 6, 8), 6),
    ("Island Challenge 2023", "Sri Lanka", "T20I", ("Sri Lanka", "West Indies"), date(2023, 8, 3), 6),
    ("Asia Rivals 2024", "UAE", "ODI", ("India", "Pakistan"), date(2024, 1, 12), 6),
    ("World Test Duel 2024", "Australia", "Test", ("Australia", "England"), date(2024, 2, 1), 6),
    ("Protea Kiwi Championship 2024", "South Africa", "ODI", ("South Africa", "New Zealand"), date(2024, 4, 10), 6),
    ("Caribbean Spin Cup 2024", "West Indies", "T20I", ("West Indies", "Sri Lanka"), date(2024, 6, 18), 6),
    ("Subcontinental Showdown 2025", "India", "T20I", ("India", "England"), date(2025, 1, 14), 6),
    ("Southern Sparks 2025", "Pakistan", "ODI", ("Pakistan", "South Africa"), date(2025, 3, 20), 6),
    ("Pacific Pulse 2025", "New Zealand", "ODI", ("New Zealand", "Australia"), date(2025, 5, 11), 6),
    ("Royal Willow Cup 2025", "England", "Test", ("England", "India"), date(2025, 7, 2), 6),
    ("Champions Prep 2026", "India", "ODI", ("India", "Australia"), date.today() - timedelta(days=70), 6),
    ("Velocity Series 2026", "England", "T20I", ("England", "Pakistan"), date.today() - timedelta(days=45), 6),
    ("Current Form Cup 2026", "South Africa", "ODI", ("South Africa", "New Zealand"), date.today() - timedelta(days=20), 6),
]

VENUES = [
    ("Narendra Modi Stadium", "Ahmedabad", "India", 132000),
    ("Eden Gardens", "Kolkata", "India", 68000),
    ("Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
    ("The Oval", "London", "England", 27500),
    ("National Stadium", "Karachi", "Pakistan", 34228),
    ("Wanderers Stadium", "Johannesburg", "South Africa", 34000),
    ("Eden Park", "Auckland", "New Zealand", 50000),
    ("R. Premadasa Stadium", "Colombo", "Sri Lanka", 35000),
    ("Kensington Oval", "Bridgetown", "West Indies", 28000),
    ("Dubai International Stadium", "Dubai", "UAE", 25000),
]


def initialize_database(force: bool = False) -> None:
    with get_connection() as connection:
        if not force:
            row = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'players'"
            ).fetchone()
            if row:
                count = connection.execute("SELECT COUNT(*) AS count FROM players").fetchone()["count"]
                if count > 0:
                    return

        drop_tables(connection)
        create_schema(connection)
        seed_database(connection)
        connection.commit()


def drop_tables(connection) -> None:
    tables = [
        "api_match_snapshots",
        "fielding_scorecards",
        "bowling_scorecards",
        "batting_scorecards",
        "innings",
        "matches",
        "series",
        "player_format_stats",
        "players",
        "venues",
        "teams",
    ]
    for table in tables:
        connection.execute(f"DROP TABLE IF EXISTS {table}")


def create_schema(connection) -> None:
    connection.executescript(
        """
        CREATE TABLE teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL UNIQUE,
            country TEXT NOT NULL
        );

        CREATE TABLE venues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venue_name TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            capacity INTEGER NOT NULL
        );

        CREATE TABLE players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            team_id INTEGER NOT NULL,
            country TEXT NOT NULL,
            playing_role TEXT NOT NULL,
            batting_style TEXT NOT NULL,
            bowling_style TEXT NOT NULL,
            FOREIGN KEY (team_id) REFERENCES teams(id)
        );

        CREATE TABLE series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_name TEXT NOT NULL,
            host_country TEXT NOT NULL,
            match_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            total_matches_planned INTEGER NOT NULL
        );

        CREATE TABLE matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_id INTEGER NOT NULL,
            match_description TEXT NOT NULL,
            match_date TEXT NOT NULL,
            format TEXT NOT NULL,
            venue_id INTEGER NOT NULL,
            team1_id INTEGER NOT NULL,
            team2_id INTEGER NOT NULL,
            winning_team_id INTEGER,
            margin_value INTEGER,
            margin_type TEXT,
            status TEXT NOT NULL,
            toss_winner_team_id INTEGER,
            toss_decision TEXT,
            FOREIGN KEY (series_id) REFERENCES series(id),
            FOREIGN KEY (venue_id) REFERENCES venues(id),
            FOREIGN KEY (team1_id) REFERENCES teams(id),
            FOREIGN KEY (team2_id) REFERENCES teams(id),
            FOREIGN KEY (winning_team_id) REFERENCES teams(id),
            FOREIGN KEY (toss_winner_team_id) REFERENCES teams(id)
        );

        CREATE TABLE innings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER NOT NULL,
            innings_number INTEGER NOT NULL,
            batting_team_id INTEGER NOT NULL,
            bowling_team_id INTEGER NOT NULL,
            total_runs INTEGER NOT NULL,
            wickets INTEGER NOT NULL,
            overs REAL NOT NULL,
            FOREIGN KEY (match_id) REFERENCES matches(id),
            FOREIGN KEY (batting_team_id) REFERENCES teams(id),
            FOREIGN KEY (bowling_team_id) REFERENCES teams(id)
        );

        CREATE TABLE batting_scorecards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            innings_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            batting_position INTEGER NOT NULL,
            runs INTEGER NOT NULL,
            balls INTEGER NOT NULL,
            fours INTEGER NOT NULL,
            sixes INTEGER NOT NULL,
            how_out TEXT NOT NULL,
            FOREIGN KEY (innings_id) REFERENCES innings(id),
            FOREIGN KEY (player_id) REFERENCES players(id)
        );

        CREATE TABLE bowling_scorecards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            innings_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            overs_bowled REAL NOT NULL,
            maidens INTEGER NOT NULL,
            runs_conceded INTEGER NOT NULL,
            wickets INTEGER NOT NULL,
            economy_rate REAL NOT NULL,
            FOREIGN KEY (innings_id) REFERENCES innings(id),
            FOREIGN KEY (player_id) REFERENCES players(id)
        );

        CREATE TABLE fielding_scorecards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            catches INTEGER NOT NULL DEFAULT 0,
            stumpings INTEGER NOT NULL DEFAULT 0,
            run_outs INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (match_id) REFERENCES matches(id),
            FOREIGN KEY (player_id) REFERENCES players(id)
        );

        CREATE TABLE player_format_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            format TEXT NOT NULL,
            matches_played INTEGER NOT NULL,
            innings_batted INTEGER NOT NULL,
            runs_scored INTEGER NOT NULL,
            batting_average REAL NOT NULL,
            strike_rate REAL NOT NULL,
            centuries INTEGER NOT NULL,
            wickets_taken INTEGER NOT NULL,
            bowling_average REAL,
            economy_rate REAL,
            catches INTEGER NOT NULL,
            stumpings INTEGER NOT NULL,
            FOREIGN KEY (player_id) REFERENCES players(id)
        );

        CREATE TABLE api_match_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            fetched_at TEXT NOT NULL,
            external_match_id TEXT,
            series_name TEXT,
            team_1 TEXT,
            team_2 TEXT,
            status TEXT,
            score_summary TEXT,
            venue TEXT,
            raw_payload TEXT NOT NULL
        );

        CREATE INDEX idx_players_team_id ON players(team_id);
        CREATE INDEX idx_matches_date ON matches(match_date);
        CREATE INDEX idx_matches_status ON matches(status);
        CREATE INDEX idx_matches_format ON matches(format);
        CREATE INDEX idx_batting_innings_player ON batting_scorecards(innings_id, player_id);
        CREATE INDEX idx_bowling_innings_player ON bowling_scorecards(innings_id, player_id);
        CREATE INDEX idx_stats_format ON player_format_stats(format);
        CREATE INDEX idx_api_snapshots_fetched_at ON api_match_snapshots(fetched_at);
        """
    )


def seed_database(connection) -> None:
    team_ids = {}
    for team_name, country in TEAM_DEFINITIONS:
        cursor = connection.execute(
            "INSERT INTO teams(team_name, country) VALUES (?, ?)",
            (team_name, country),
        )
        team_ids[team_name] = cursor.lastrowid

    venue_ids = {}
    for venue_name, city, country, capacity in VENUES:
        cursor = connection.execute(
            "INSERT INTO venues(venue_name, city, country, capacity) VALUES (?, ?, ?, ?)",
            (venue_name, city, country, capacity),
        )
        venue_ids[venue_name] = cursor.lastrowid

    player_ids_by_team = defaultdict(list)
    for team_name, country in TEAM_DEFINITIONS:
        for full_name, role, batting_style, bowling_style in PLAYER_ROSTERS[team_name]:
            cursor = connection.execute(
                """
                INSERT INTO players(
                    full_name, team_id, country, playing_role, batting_style, bowling_style
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    full_name,
                    team_ids[team_name],
                    country,
                    role,
                    batting_style,
                    bowling_style,
                ),
            )
            player_ids_by_team[team_name].append(cursor.lastrowid)

    series_records = []
    for series_name, host_country, match_type, teams, start_date, total_matches in SERIES_BLUEPRINTS:
        cursor = connection.execute(
            """
            INSERT INTO series(series_name, host_country, match_type, start_date, total_matches_planned)
            VALUES (?, ?, ?, ?, ?)
            """,
            (series_name, host_country, match_type, start_date.isoformat(), total_matches),
        )
        series_records.append(
            {
                "id": cursor.lastrowid,
                "series_name": series_name,
                "host_country": host_country,
                "match_type": match_type,
                "teams": teams,
                "start_date": start_date,
                "total_matches": total_matches,
            }
        )

    rng = random.Random(7)
    stats = defaultdict(
        lambda: {
            "matches": set(),
            "innings": 0,
            "runs": 0,
            "balls": 0,
            "outs": 0,
            "centuries": 0,
            "wickets": 0,
            "runs_conceded": 0,
            "overs": 0.0,
            "catches": 0,
            "stumpings": 0,
        }
    )

    for series in series_records:
        team1_name, team2_name = series["teams"]
        host_venues = [
            venue_name
            for venue_name, _, venue_country, _ in VENUES
            if venue_country == series["host_country"]
        ]
        if not host_venues:
            host_venues = [VENUES[-1][0]]

        for match_number in range(1, series["total_matches"] + 1):
            team1_id = team_ids[team1_name]
            team2_id = team_ids[team2_name]
            match_date = series["start_date"] + timedelta(days=(match_number - 1) * 4)
            venue_name = host_venues[(match_number - 1) % len(host_venues)]
            venue_id = venue_ids[venue_name]
            toss_winner = team1_id if rng.random() > 0.5 else team2_id
            toss_decision = "bat" if rng.random() > 0.45 else "bowl"

            if match_date > date.today():
                status = "upcoming"
                winner = None
                margin_value = None
                margin_type = None
            elif (date.today() - match_date).days <= 2 and series["series_name"] == "Current Form Cup 2026" and match_number >= 5:
                status = "live" if match_number == 5 else "upcoming"
                winner = None
                margin_value = None
                margin_type = None
            else:
                status = "completed"
                home_bias = 0.58 if series["host_country"] in (team1_name, team2_name) else 0.5
                if series["host_country"] == team1_name:
                    winner = team1_id if rng.random() < home_bias else team2_id
                elif series["host_country"] == team2_name:
                    winner = team2_id if rng.random() < home_bias else team1_id
                else:
                    winner = team1_id if rng.random() < 0.5 else team2_id
                margin_type = "runs" if rng.random() > 0.5 else "wickets"
                margin_value = rng.randint(12, 95) if margin_type == "runs" else rng.randint(1, 8)

            match_cursor = connection.execute(
                """
                INSERT INTO matches(
                    series_id, match_description, match_date, format, venue_id, team1_id, team2_id,
                    winning_team_id, margin_value, margin_type, status, toss_winner_team_id, toss_decision
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    series["id"],
                    f"{team1_name} vs {team2_name} - Match {match_number}",
                    match_date.isoformat(),
                    series["match_type"],
                    venue_id,
                    team1_id,
                    team2_id,
                    winner,
                    margin_value,
                    margin_type,
                    status,
                    toss_winner,
                    toss_decision,
                ),
            )
            match_id = match_cursor.lastrowid

            if status != "completed":
                continue

            first_batting = team1_name if toss_decision == "bat" and toss_winner == team1_id else team2_name
            if toss_decision == "bowl":
                first_batting = team2_name if toss_winner == team1_id else team1_name
            innings_order = [
                (first_batting, team2_name if first_batting == team1_name else team1_name),
                (team2_name if first_batting == team1_name else team1_name, first_batting),
            ]

            innings_totals = []
            for innings_number, (batting_team_name, bowling_team_name) in enumerate(innings_order, start=1):
                if series["match_type"] == "T20I":
                    base_total = rng.randint(145, 215)
                    overs = 20.0
                elif series["match_type"] == "ODI":
                    base_total = rng.randint(210, 340)
                    overs = 50.0
                else:
                    base_total = rng.randint(260, 520)
                    overs = 90.0

                if innings_number == 2 and winner:
                    winning_team_name = team1_name if winner == team1_id else team2_name
                    if batting_team_name == winning_team_name and margin_type == "wickets":
                        base_total = max(base_total, innings_totals[0] + rng.randint(1, 7))
                    elif batting_team_name == winning_team_name and margin_type == "runs":
                        base_total = max(120, innings_totals[0] - rng.randint(12, 45))
                    elif batting_team_name != winning_team_name and margin_type == "runs":
                        base_total = max(120, innings_totals[0] - rng.randint(12, 45))
                    else:
                        base_total = innings_totals[0] + rng.randint(1, 5)

                wickets = rng.randint(4, 10)
                innings_cursor = connection.execute(
                    """
                    INSERT INTO innings(
                        match_id, innings_number, batting_team_id, bowling_team_id, total_runs, wickets, overs
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        match_id,
                        innings_number,
                        team_ids[batting_team_name],
                        team_ids[bowling_team_name],
                        base_total,
                        wickets,
                        overs,
                    ),
                )
                innings_id = innings_cursor.lastrowid
                innings_totals.append(base_total)

                create_batting_scorecards(
                    connection,
                    rng,
                    innings_id,
                    match_id,
                    series["match_type"],
                    base_total,
                    wickets,
                    player_ids_by_team[batting_team_name],
                    stats,
                )
                create_bowling_scorecards(
                    connection,
                    rng,
                    innings_id,
                    match_id,
                    series["match_type"],
                    overs,
                    wickets,
                    player_ids_by_team[bowling_team_name],
                    stats,
                )
                create_fielding_scorecards(
                    connection,
                    rng,
                    match_id,
                    player_ids_by_team[bowling_team_name],
                    wickets,
                    stats,
                )

                for player_id in player_ids_by_team[batting_team_name]:
                    stats[(player_id, series["match_type"])]["matches"].add(match_id)
                for player_id in player_ids_by_team[bowling_team_name]:
                    stats[(player_id, series["match_type"])]["matches"].add(match_id)

    populate_player_format_stats(connection, stats)


def create_batting_scorecards(
    connection,
    rng: random.Random,
    innings_id: int,
    match_id: int,
    match_format: str,
    total_runs: int,
    wickets: int,
    player_ids: list[int],
    stats,
) -> None:
    weights = [0.17, 0.14, 0.13, 0.12, 0.11, 0.09, 0.08, 0.06, 0.04, 0.035, 0.025]
    raw_runs = [max(0, int(total_runs * weight + rng.randint(-10, 18))) for weight in weights]
    difference = total_runs - sum(raw_runs)
    raw_runs[0] += difference
    if raw_runs[0] < 0:
        raw_runs[0] = 0

    for position, player_id in enumerate(player_ids, start=1):
        runs = raw_runs[position - 1]
        balls_multiplier = 1.0 if match_format == "Test" else (0.95 if match_format == "ODI" else 0.75)
        balls = max(10 if position <= 6 else 4, int(runs * balls_multiplier + rng.randint(0, 18)))
        fours = max(0, runs // 18 + rng.randint(0, 3))
        sixes = max(0, runs // 35 + rng.randint(0, 2))
        how_out = "not out" if position > wickets else rng.choice(
            ["caught", "bowled", "lbw", "run out", "stumped"]
        )

        connection.execute(
            """
            INSERT INTO batting_scorecards(
                innings_id, player_id, batting_position, runs, balls, fours, sixes, how_out
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (innings_id, player_id, position, runs, balls, fours, sixes, how_out),
        )

        key = (player_id, match_format)
        stats[key]["innings"] += 1
        stats[key]["runs"] += runs
        stats[key]["balls"] += balls
        if how_out != "not out":
            stats[key]["outs"] += 1
        if runs >= 100:
            stats[key]["centuries"] += 1


def create_bowling_scorecards(
    connection,
    rng: random.Random,
    innings_id: int,
    match_id: int,
    match_format: str,
    innings_overs: float,
    wickets: int,
    bowler_ids: list[int],
    stats,
) -> None:
    main_bowlers = bowler_ids[4:11]
    selected_bowlers = [main_bowlers[0], main_bowlers[1], main_bowlers[2], main_bowlers[3], bowler_ids[6]]
    if match_format == "T20I":
        overs_plan = [4.0, 4.0, 4.0, 4.0, 4.0]
    elif match_format == "ODI":
        overs_plan = [10.0, 10.0, 10.0, 10.0, 10.0]
    else:
        overs_plan = [18.0, 18.0, 18.0, 18.0, 18.0]

    wickets_left = wickets
    for index, player_id in enumerate(selected_bowlers):
        overs_bowled = overs_plan[index]
        if index == len(selected_bowlers) - 1 and match_format == "Test":
            overs_bowled = innings_overs - sum(overs_plan[:-1])
        runs_conceded = int((overs_bowled * rng.uniform(4.5, 6.8)) if match_format != "T20I" else (overs_bowled * rng.uniform(6.5, 9.4)))
        if match_format == "Test":
            runs_conceded = int(overs_bowled * rng.uniform(2.8, 4.2))
        if index == len(selected_bowlers) - 1:
            bowler_wickets = max(0, wickets_left)
        else:
            bowler_wickets = rng.randint(0, min(4, wickets_left))
        wickets_left -= bowler_wickets
        maidens = rng.randint(0, 3 if match_format != "T20I" else 1)
        economy_rate = round(runs_conceded / max(overs_bowled, 1), 2)

        connection.execute(
            """
            INSERT INTO bowling_scorecards(
                innings_id, player_id, overs_bowled, maidens, runs_conceded, wickets, economy_rate
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (innings_id, player_id, overs_bowled, maidens, runs_conceded, bowler_wickets, economy_rate),
        )

        key = (player_id, match_format)
        stats[key]["wickets"] += bowler_wickets
        stats[key]["runs_conceded"] += runs_conceded
        stats[key]["overs"] += overs_bowled


def create_fielding_scorecards(connection, rng, match_id: int, fielding_team_players: list[int], wickets: int, stats) -> None:
    keeper_id = fielding_team_players[5]
    wicket_events = max(1, wickets - rng.randint(0, 2))
    for _ in range(wicket_events):
        player_id = keeper_id if rng.random() < 0.12 else rng.choice(fielding_team_players[0:8])
        catches = 0 if player_id == keeper_id and rng.random() < 0.5 else 1
        stumpings = 1 if player_id == keeper_id and catches == 0 else 0
        run_outs = 1 if rng.random() < 0.08 else 0
        connection.execute(
            """
            INSERT INTO fielding_scorecards(match_id, player_id, catches, stumpings, run_outs)
            VALUES (?, ?, ?, ?, ?)
            """,
            (match_id, player_id, catches, stumpings, run_outs),
        )

        player_row = connection.execute("SELECT team_name FROM teams WHERE id = (SELECT team_id FROM players WHERE id = ?)", (player_id,)).fetchone()
        team_name = player_row["team_name"]
        for format_row in connection.execute(
            """
            SELECT format FROM matches WHERE id = ?
            """,
            (match_id,),
        ):
            key = (player_id, format_row["format"])
            stats[key]["catches"] += catches
            stats[key]["stumpings"] += stumpings


def populate_player_format_stats(connection, stats) -> None:
    for (player_id, match_format), values in stats.items():
        matches_played = len(values["matches"])
        if matches_played == 0:
            continue
        batting_average = round(
            values["runs"] / max(values["outs"], 1),
            2,
        )
        strike_rate = round(
            (values["runs"] * 100) / max(values["balls"], 1),
            2,
        )
        bowling_average = (
            round(values["runs_conceded"] / values["wickets"], 2) if values["wickets"] else None
        )
        economy_rate = (
            round(values["runs_conceded"] / max(values["overs"], 1), 2) if values["overs"] else None
        )
        connection.execute(
            """
            INSERT INTO player_format_stats(
                player_id, format, matches_played, innings_batted, runs_scored, batting_average,
                strike_rate, centuries, wickets_taken, bowling_average, economy_rate, catches, stumpings
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                player_id,
                match_format,
                matches_played,
                values["innings"],
                values["runs"],
                batting_average,
                strike_rate,
                values["centuries"],
                values["wickets"],
                bowling_average,
                economy_rate,
                values["catches"],
                values["stumpings"],
            ),
        )


def store_api_match_snapshots(connection, matches: list[dict], source: str = "notebook") -> int:
    fetched_at = datetime.utcnow().isoformat(timespec="seconds")
    inserted = 0
    for match in matches:
        connection.execute(
            """
            INSERT INTO api_match_snapshots(
                source, fetched_at, external_match_id, series_name, team_1, team_2,
                status, score_summary, venue, raw_payload
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                source,
                fetched_at,
                str(match.get("match_id") or match.get("id") or ""),
                match.get("series") or match.get("series_name") or "",
                match.get("team_1") or match.get("team1") or "",
                match.get("team_2") or match.get("team2") or "",
                match.get("status") or "",
                match.get("score") or match.get("score_summary") or "",
                match.get("venue") or "",
                json.dumps(match, default=str),
            ),
        )
        inserted += 1
    return inserted
