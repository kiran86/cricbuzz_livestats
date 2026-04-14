# Cricbuzz LiveStats

This project is a Streamlit-based cricket analytics dashboard that combines:

- live match cards with optional API integration
- SQLite-backed cricket data storage
- 25 assignment-aligned SQL analytics queries
- player CRUD operations

## Features

- `Home`: project overview and startup instructions
- `Live Matches`: live and recent match updates
- `Top Player Stats`: batting, bowling, and fielding leaderboards
- `SQL Analytics`: 25 predefined SQL answers plus a custom query editor
- `CRUD Operations`: add, update, delete, and browse player records

## Tech Stack

- Python
- Streamlit
- SQLite
- pandas
- requests

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

The database is created automatically at `data/cricbuzz_livestats.db` the first time the app starts.

## Optional API Configuration

If you have a Cricbuzz-compatible API, set:

```bash
export CRICBUZZ_API_URL="https://your-api-endpoint.example.com/live"
export CRICBUZZ_API_KEY="your-api-key"
```

If these values are not present, the app uses built-in sample live match data so the dashboard still works offline.

## Project Structure

```text
.
├── app.py
├── README.md
├── requirements.txt
├── pages/
│   ├── home.py
│   ├── live_matches.py
│   ├── top_stats.py
│   ├── sql_queries.py
│   └── crud_operations.py
├── utils/
│   └── db_connection.py
├── notebooks/
│   └── data_fetching.ipynb
└── data/
    └── cricbuzz_livestats.db
```

## Notes

- The app seeds realistic demo data across Test, ODI, and T20I formats.
- SQL analytics queries are stored in `sql/queries.py`.
- Database initialization lives in `utils/db_setup.py`.
