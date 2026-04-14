SQL_QUERIES = {
    1: {
        "title": "Players representing India",
        "level": "Beginner",
        "sql": """
            SELECT p.full_name, p.playing_role, p.batting_style, p.bowling_style
            FROM players p
            JOIN teams t ON t.id = p.team_id
            WHERE t.team_name = 'India'
            ORDER BY p.full_name;
        """,
    },
    2: {
        "title": "Matches played in the last 30 days",
        "level": "Beginner",
        "sql": """
            SELECT
                m.match_description,
                t1.team_name AS team_1,
                t2.team_name AS team_2,
                v.venue_name || ', ' || v.city AS venue,
                m.match_date
            FROM matches m
            JOIN teams t1 ON t1.id = m.team1_id
            JOIN teams t2 ON t2.id = m.team2_id
            JOIN venues v ON v.id = m.venue_id
            WHERE DATE(m.match_date) >= DATE('now', '-30 day')
            ORDER BY DATE(m.match_date) DESC;
        """,
    },
    3: {
        "title": "Top 10 ODI run scorers",
        "level": "Beginner",
        "sql": """
            SELECT
                p.full_name,
                s.runs_scored AS total_runs,
                s.batting_average,
                s.centuries
            FROM player_format_stats s
            JOIN players p ON p.id = s.player_id
            WHERE s.format = 'ODI'
            ORDER BY s.runs_scored DESC
            LIMIT 10;
        """,
    },
    4: {
        "title": "Venues above 50,000 capacity",
        "level": "Beginner",
        "sql": """
            SELECT venue_name, city, country, capacity
            FROM venues
            WHERE capacity > 50000
            ORDER BY capacity DESC;
        """,
    },
    5: {
        "title": "Matches won by each team",
        "level": "Beginner",
        "sql": """
            SELECT t.team_name, COUNT(*) AS total_wins
            FROM matches m
            JOIN teams t ON t.id = m.winning_team_id
            WHERE m.status = 'completed'
            GROUP BY t.team_name
            ORDER BY total_wins DESC, t.team_name;
        """,
    },
    6: {
        "title": "Player count by role",
        "level": "Beginner",
        "sql": """
            SELECT playing_role, COUNT(*) AS player_count
            FROM players
            GROUP BY playing_role
            ORDER BY player_count DESC, playing_role;
        """,
    },
    7: {
        "title": "Highest individual batting score per format",
        "level": "Beginner",
        "sql": """
            SELECT
                m.format,
                MAX(b.runs) AS highest_score
            FROM batting_scorecards b
            JOIN innings i ON i.id = b.innings_id
            JOIN matches m ON m.id = i.match_id
            GROUP BY m.format
            ORDER BY m.format;
        """,
    },
    8: {
        "title": "Series started in 2024",
        "level": "Beginner",
        "sql": """
            SELECT series_name, host_country, match_type, start_date, total_matches_planned
            FROM series
            WHERE strftime('%Y', start_date) = '2024'
            ORDER BY start_date;
        """,
    },
    9: {
        "title": "All-rounders with 1000+ runs and 50+ wickets",
        "level": "Intermediate",
        "sql": """
            SELECT
                p.full_name,
                SUM(s.runs_scored) AS total_runs,
                SUM(s.wickets_taken) AS total_wickets,
                GROUP_CONCAT(s.format, ', ') AS formats
            FROM player_format_stats s
            JOIN players p ON p.id = s.player_id
            WHERE p.playing_role = 'All-rounder'
            GROUP BY p.id, p.full_name
            HAVING SUM(s.runs_scored) > 1000 AND SUM(s.wickets_taken) > 50
            ORDER BY total_runs DESC;
        """,
    },
    10: {
        "title": "Last 20 completed matches",
        "level": "Intermediate",
        "sql": """
            SELECT
                m.match_description,
                t1.team_name AS team_1,
                t2.team_name AS team_2,
                wt.team_name AS winning_team,
                m.margin_value,
                m.margin_type,
                v.venue_name
            FROM matches m
            JOIN teams t1 ON t1.id = m.team1_id
            JOIN teams t2 ON t2.id = m.team2_id
            JOIN teams wt ON wt.id = m.winning_team_id
            JOIN venues v ON v.id = m.venue_id
            WHERE m.status = 'completed'
            ORDER BY DATE(m.match_date) DESC
            LIMIT 20;
        """,
    },
    11: {
        "title": "Player performance across formats",
        "level": "Intermediate",
        "sql": """
            SELECT
                p.full_name,
                SUM(CASE WHEN s.format = 'Test' THEN s.runs_scored ELSE 0 END) AS test_runs,
                SUM(CASE WHEN s.format = 'ODI' THEN s.runs_scored ELSE 0 END) AS odi_runs,
                SUM(CASE WHEN s.format = 'T20I' THEN s.runs_scored ELSE 0 END) AS t20i_runs,
                ROUND(AVG(s.batting_average), 2) AS overall_batting_average
            FROM player_format_stats s
            JOIN players p ON p.id = s.player_id
            GROUP BY p.id, p.full_name
            HAVING COUNT(DISTINCT s.format) >= 2
            ORDER BY overall_batting_average DESC, p.full_name;
        """,
    },
    12: {
        "title": "Home vs away wins",
        "level": "Intermediate",
        "sql": """
            WITH team_match_view AS (
                SELECT m.id AS match_id, t1.id AS team_id, t1.team_name, t1.country AS team_country,
                       v.country AS venue_country, m.winning_team_id
                FROM matches m
                JOIN teams t1 ON t1.id = m.team1_id
                JOIN venues v ON v.id = m.venue_id
                WHERE m.status = 'completed'
                UNION ALL
                SELECT m.id AS match_id, t2.id AS team_id, t2.team_name, t2.country AS team_country,
                       v.country AS venue_country, m.winning_team_id
                FROM matches m
                JOIN teams t2 ON t2.id = m.team2_id
                JOIN venues v ON v.id = m.venue_id
                WHERE m.status = 'completed'
            )
            SELECT
                team_name,
                SUM(CASE WHEN team_country = venue_country AND winning_team_id = team_id THEN 1 ELSE 0 END) AS home_wins,
                SUM(CASE WHEN team_country <> venue_country AND winning_team_id = team_id THEN 1 ELSE 0 END) AS away_wins
            FROM team_match_view
            GROUP BY team_id, team_name
            ORDER BY home_wins DESC, away_wins DESC;
        """,
    },
    13: {
        "title": "100+ batting partnerships",
        "level": "Intermediate",
        "sql": """
            SELECT
                p1.full_name AS batter_one,
                p2.full_name AS batter_two,
                (b1.runs + b2.runs) AS partnership_runs,
                i.innings_number,
                m.match_description
            FROM batting_scorecards b1
            JOIN batting_scorecards b2
              ON b1.innings_id = b2.innings_id
             AND b2.batting_position = b1.batting_position + 1
            JOIN players p1 ON p1.id = b1.player_id
            JOIN players p2 ON p2.id = b2.player_id
            JOIN innings i ON i.id = b1.innings_id
            JOIN matches m ON m.id = i.match_id
            WHERE (b1.runs + b2.runs) >= 100
            ORDER BY partnership_runs DESC;
        """,
    },
    14: {
        "title": "Bowling performance by venue",
        "level": "Intermediate",
        "sql": """
            SELECT
                p.full_name,
                v.venue_name,
                ROUND(AVG(bs.economy_rate), 2) AS average_economy_rate,
                SUM(bs.wickets) AS total_wickets,
                COUNT(DISTINCT m.id) AS matches_played
            FROM bowling_scorecards bs
            JOIN innings i ON i.id = bs.innings_id
            JOIN matches m ON m.id = i.match_id
            JOIN venues v ON v.id = m.venue_id
            JOIN players p ON p.id = bs.player_id
            WHERE bs.overs_bowled >= 4
            GROUP BY p.id, p.full_name, v.id, v.venue_name
            HAVING COUNT(DISTINCT m.id) >= 3
            ORDER BY total_wickets DESC, average_economy_rate ASC;
        """,
    },
    15: {
        "title": "Player performance in close matches",
        "level": "Intermediate",
        "sql": """
            WITH close_matches AS (
                SELECT id
                FROM matches
                WHERE status = 'completed'
                  AND (
                    (margin_type = 'runs' AND margin_value < 50)
                    OR (margin_type = 'wickets' AND margin_value < 5)
                  )
            )
            SELECT
                p.full_name,
                ROUND(AVG(b.runs), 2) AS average_runs,
                COUNT(DISTINCT m.id) AS close_matches_played,
                SUM(CASE WHEN m.winning_team_id = i.batting_team_id THEN 1 ELSE 0 END) AS wins_when_batting
            FROM close_matches cm
            JOIN innings i ON i.match_id = cm.id
            JOIN batting_scorecards b ON b.innings_id = i.id
            JOIN matches m ON m.id = i.match_id
            JOIN players p ON p.id = b.player_id
            GROUP BY p.id, p.full_name
            HAVING COUNT(DISTINCT m.id) >= 3
            ORDER BY average_runs DESC;
        """,
    },
    16: {
        "title": "Yearly batting performance since 2020",
        "level": "Intermediate",
        "sql": """
            SELECT
                p.full_name,
                strftime('%Y', m.match_date) AS match_year,
                ROUND(AVG(b.runs), 2) AS average_runs_per_match,
                ROUND(AVG((b.runs * 100.0) / NULLIF(b.balls, 0)), 2) AS average_strike_rate,
                COUNT(DISTINCT m.id) AS matches_played
            FROM batting_scorecards b
            JOIN innings i ON i.id = b.innings_id
            JOIN matches m ON m.id = i.match_id
            JOIN players p ON p.id = b.player_id
            WHERE DATE(m.match_date) >= DATE('2020-01-01')
            GROUP BY p.id, p.full_name, strftime('%Y', m.match_date)
            HAVING COUNT(DISTINCT m.id) >= 5
            ORDER BY match_year DESC, average_runs_per_match DESC;
        """,
    },
    17: {
        "title": "Toss advantage analysis",
        "level": "Advanced",
        "sql": """
            SELECT
                toss_decision,
                COUNT(*) AS matches_count,
                SUM(CASE WHEN toss_winner_team_id = winning_team_id THEN 1 ELSE 0 END) AS toss_winner_wins,
                ROUND(
                    100.0 * SUM(CASE WHEN toss_winner_team_id = winning_team_id THEN 1 ELSE 0 END) / COUNT(*),
                    2
                ) AS toss_winner_win_percentage
            FROM matches
            WHERE status = 'completed'
              AND toss_winner_team_id IS NOT NULL
            GROUP BY toss_decision;
        """,
    },
    18: {
        "title": "Most economical bowlers in ODI and T20I",
        "level": "Advanced",
        "sql": """
            SELECT
                p.full_name,
                ROUND(SUM(bs.runs_conceded) / SUM(bs.overs_bowled), 2) AS overall_economy_rate,
                SUM(bs.wickets) AS total_wickets,
                COUNT(DISTINCT m.id) AS matches_bowled
            FROM bowling_scorecards bs
            JOIN innings i ON i.id = bs.innings_id
            JOIN matches m ON m.id = i.match_id
            JOIN players p ON p.id = bs.player_id
            WHERE m.format IN ('ODI', 'T20I')
            GROUP BY p.id, p.full_name
            HAVING COUNT(DISTINCT m.id) >= 10
               AND (SUM(bs.overs_bowled) / COUNT(DISTINCT m.id)) >= 2
            ORDER BY overall_economy_rate ASC, total_wickets DESC;
        """,
    },
    19: {
        "title": "Most consistent batsmen since 2022",
        "level": "Advanced",
        "sql": """
            WITH batting_sample AS (
                SELECT
                    p.full_name,
                    b.runs,
                    b.balls,
                    COUNT(*) OVER (PARTITION BY p.id) AS innings_count,
                    AVG(b.runs) OVER (PARTITION BY p.id) AS avg_runs,
                    AVG(b.runs * b.runs) OVER (PARTITION BY p.id) AS avg_square_runs
                FROM batting_scorecards b
                JOIN innings i ON i.id = b.innings_id
                JOIN matches m ON m.id = i.match_id
                JOIN players p ON p.id = b.player_id
                WHERE DATE(m.match_date) >= DATE('2022-01-01')
                  AND b.balls >= 10
            )
            SELECT DISTINCT
                full_name,
                ROUND(avg_runs, 2) AS average_runs,
                ROUND(SQRT(MAX(avg_square_runs - (avg_runs * avg_runs), 0)), 2) AS run_std_dev,
                innings_count
            FROM batting_sample
            WHERE innings_count >= 10
            ORDER BY run_std_dev ASC, average_runs DESC;
        """,
    },
    20: {
        "title": "Matches played and batting average by format",
        "level": "Advanced",
        "sql": """
            SELECT
                p.full_name,
                SUM(CASE WHEN s.format = 'Test' THEN s.matches_played ELSE 0 END) AS test_matches,
                SUM(CASE WHEN s.format = 'ODI' THEN s.matches_played ELSE 0 END) AS odi_matches,
                SUM(CASE WHEN s.format = 'T20I' THEN s.matches_played ELSE 0 END) AS t20_matches,
                ROUND(MAX(CASE WHEN s.format = 'Test' THEN s.batting_average END), 2) AS test_average,
                ROUND(MAX(CASE WHEN s.format = 'ODI' THEN s.batting_average END), 2) AS odi_average,
                ROUND(MAX(CASE WHEN s.format = 'T20I' THEN s.batting_average END), 2) AS t20_average
            FROM player_format_stats s
            JOIN players p ON p.id = s.player_id
            GROUP BY p.id, p.full_name
            HAVING SUM(s.matches_played) >= 20
            ORDER BY (test_matches + odi_matches + t20_matches) DESC, p.full_name;
        """,
    },
    21: {
        "title": "Weighted player performance rankings",
        "level": "Advanced",
        "sql": """
            SELECT
                s.format,
                p.full_name,
                ROUND(
                    (s.runs_scored * 0.01) + (s.batting_average * 0.5) + (s.strike_rate * 0.3) +
                    (s.wickets_taken * 2) +
                    ((50 - COALESCE(s.bowling_average, 50)) * 0.5) +
                    ((6 - COALESCE(s.economy_rate, 6)) * 2) +
                    (s.catches * 3) +
                    (s.stumpings * 5),
                    2
                ) AS weighted_score
            FROM player_format_stats s
            JOIN players p ON p.id = s.player_id
            ORDER BY s.format, weighted_score DESC;
        """,
    },
    22: {
        "title": "Head-to-head match prediction analysis",
        "level": "Advanced",
        "sql": """
            WITH recent_matches AS (
                SELECT *
                FROM matches
                WHERE status = 'completed'
                  AND DATE(match_date) >= DATE('now', '-3 year')
            ),
            pairs AS (
                SELECT
                    CASE WHEN team1_id < team2_id THEN team1_id ELSE team2_id END AS team_a_id,
                    CASE WHEN team1_id < team2_id THEN team2_id ELSE team1_id END AS team_b_id,
                    id,
                    winning_team_id,
                    margin_value,
                    margin_type,
                    toss_decision,
                    venue_id
                FROM recent_matches
            )
            SELECT
                ta.team_name AS team_a,
                tb.team_name AS team_b,
                COUNT(*) AS total_matches,
                SUM(CASE WHEN p.winning_team_id = p.team_a_id THEN 1 ELSE 0 END) AS team_a_wins,
                SUM(CASE WHEN p.winning_team_id = p.team_b_id THEN 1 ELSE 0 END) AS team_b_wins,
                ROUND(AVG(CASE WHEN p.winning_team_id = p.team_a_id THEN p.margin_value END), 2) AS avg_margin_team_a_wins,
                ROUND(AVG(CASE WHEN p.winning_team_id = p.team_b_id THEN p.margin_value END), 2) AS avg_margin_team_b_wins,
                ROUND(100.0 * SUM(CASE WHEN p.winning_team_id = p.team_a_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS team_a_win_pct,
                ROUND(100.0 * SUM(CASE WHEN p.winning_team_id = p.team_b_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS team_b_win_pct,
                SUM(CASE WHEN p.toss_decision = 'bat' THEN 1 ELSE 0 END) AS batting_first_matches,
                SUM(CASE WHEN p.toss_decision = 'bowl' THEN 1 ELSE 0 END) AS bowling_first_matches
            FROM pairs p
            JOIN teams ta ON ta.id = p.team_a_id
            JOIN teams tb ON tb.id = p.team_b_id
            GROUP BY p.team_a_id, p.team_b_id
            HAVING COUNT(*) >= 5
            ORDER BY total_matches DESC, team_a, team_b;
        """,
    },
    23: {
        "title": "Recent player form and momentum",
        "level": "Advanced",
        "sql": """
            WITH recent_scores AS (
                SELECT
                    p.id AS player_id,
                    p.full_name,
                    b.runs,
                    b.balls,
                    ROW_NUMBER() OVER (PARTITION BY p.id ORDER BY DATE(m.match_date) DESC, i.innings_number DESC) AS rn
                FROM batting_scorecards b
                JOIN innings i ON i.id = b.innings_id
                JOIN matches m ON m.id = i.match_id
                JOIN players p ON p.id = b.player_id
            ),
            last_ten AS (
                SELECT *
                FROM recent_scores
                WHERE rn <= 10
            )
            SELECT
                full_name,
                ROUND(AVG(CASE WHEN rn <= 5 THEN runs END), 2) AS avg_last_5,
                ROUND(AVG(runs), 2) AS avg_last_10,
                ROUND(AVG((runs * 100.0) / NULLIF(balls, 0)), 2) AS recent_strike_rate,
                SUM(CASE WHEN runs >= 50 THEN 1 ELSE 0 END) AS fifties_in_last_10,
                CASE
                    WHEN AVG(runs) >= 55 THEN 'Excellent Form'
                    WHEN AVG(runs) >= 42 THEN 'Good Form'
                    WHEN AVG(runs) >= 28 THEN 'Average Form'
                    ELSE 'Poor Form'
                END AS form_category
            FROM last_ten
            GROUP BY player_id, full_name
            HAVING COUNT(*) = 10
            ORDER BY avg_last_10 DESC;
        """,
    },
    24: {
        "title": "Best batting partnerships",
        "level": "Advanced",
        "sql": """
            WITH consecutive_pairs AS (
                SELECT
                    CASE WHEN b1.player_id < b2.player_id THEN b1.player_id ELSE b2.player_id END AS player_a_id,
                    CASE WHEN b1.player_id < b2.player_id THEN b2.player_id ELSE b1.player_id END AS player_b_id,
                    b1.runs + b2.runs AS partnership_runs
                FROM batting_scorecards b1
                JOIN batting_scorecards b2
                  ON b1.innings_id = b2.innings_id
                 AND b2.batting_position = b1.batting_position + 1
            )
            SELECT
                p1.full_name AS player_a,
                p2.full_name AS player_b,
                ROUND(AVG(cp.partnership_runs), 2) AS average_partnership_runs,
                SUM(CASE WHEN cp.partnership_runs > 50 THEN 1 ELSE 0 END) AS partnerships_above_50,
                MAX(cp.partnership_runs) AS highest_partnership,
                ROUND(100.0 * SUM(CASE WHEN cp.partnership_runs > 50 THEN 1 ELSE 0 END) / COUNT(*), 2) AS success_rate
            FROM consecutive_pairs cp
            JOIN players p1 ON p1.id = cp.player_a_id
            JOIN players p2 ON p2.id = cp.player_b_id
            GROUP BY cp.player_a_id, cp.player_b_id
            HAVING COUNT(*) >= 5
            ORDER BY success_rate DESC, average_partnership_runs DESC;
        """,
    },
    25: {
        "title": "Quarterly performance evolution",
        "level": "Advanced",
        "sql": """
            WITH quarterly_stats AS (
                SELECT
                    p.id AS player_id,
                    p.full_name,
                    strftime('%Y', m.match_date) || '-Q' ||
                    CAST(((CAST(strftime('%m', m.match_date) AS INTEGER) - 1) / 3) + 1 AS INTEGER) AS quarter_label,
                    MIN(DATE(m.match_date)) AS quarter_start,
                    COUNT(DISTINCT m.id) AS matches_in_quarter,
                    AVG(b.runs) AS avg_runs,
                    AVG((b.runs * 100.0) / NULLIF(b.balls, 0)) AS avg_strike_rate
                FROM batting_scorecards b
                JOIN innings i ON i.id = b.innings_id
                JOIN matches m ON m.id = i.match_id
                JOIN players p ON p.id = b.player_id
                GROUP BY p.id, p.full_name, quarter_label
                HAVING COUNT(DISTINCT m.id) >= 3
            ),
            enriched AS (
                SELECT
                    *,
                    LAG(avg_runs) OVER (PARTITION BY player_id ORDER BY quarter_start) AS prev_avg_runs,
                    COUNT(*) OVER (PARTITION BY player_id) AS quarter_count
                FROM quarterly_stats
            )
            SELECT
                full_name,
                quarter_label,
                ROUND(avg_runs, 2) AS avg_runs,
                ROUND(avg_strike_rate, 2) AS avg_strike_rate,
                ROUND(prev_avg_runs, 2) AS previous_quarter_avg_runs,
                CASE
                    WHEN prev_avg_runs IS NULL THEN 'Starting Phase'
                    WHEN avg_runs > prev_avg_runs + 5 THEN 'Improving'
                    WHEN avg_runs < prev_avg_runs - 5 THEN 'Declining'
                    ELSE 'Stable'
                END AS quarter_trend,
                CASE
                    WHEN quarter_count >= 4 AND avg_runs > COALESCE(prev_avg_runs, avg_runs) + 5 THEN 'Career Ascending'
                    WHEN quarter_count >= 4 AND avg_runs < COALESCE(prev_avg_runs, avg_runs) - 5 THEN 'Career Declining'
                    WHEN quarter_count >= 4 THEN 'Career Stable'
                    ELSE 'Developing Sample'
                END AS career_phase
            FROM enriched
            WHERE quarter_count >= 4
            ORDER BY full_name, quarter_start;
        """,
    },
}
