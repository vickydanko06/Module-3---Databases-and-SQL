"""
Exercise: Build Your Own Database
Module 3 | Lesson 1 | ~30 min

Objective:
  Connect to an in-memory SQLite database, create two related tables,
  insert sample data, and query across them with a JOIN.

  ~Header that is given with starter code ~
"""

"""
I am making my first database that will be about music
"""

import sqlite3

# ── Database setup ────────────────────────────────────────────────────────────
# Using ":memory:" creates a temporary database that lives only for this run.
# No file is written to disk — great for experiments.
conn = sqlite3.connect("music.db")

# PRAGMA foreign_keys must be ON for FK constraints to be enforced in SQLite.
conn.execute("PRAGMA foreign_keys = ON")
conn.row_factory = sqlite3.Row  # Lets us access columns by name: row["title"]


# ── Your tasks ────────────────────────────────────────────────────────────────


def create_tables(conn: sqlite3.Connection) -> None:
    """
    Create the 'artists' and 'albums' tables.

    Schema:
      artists: id INTEGER PRIMARY KEY, name TEXT NOT NULL
      albums:  id INTEGER PRIMARY KEY, title TEXT NOT NULL,
               year INTEGER, artist_id INTEGER (FK -> artists.id)
    """
    # TODO: write and execute two CREATE TABLE statements
    # Hint: use conn.executescript() for multiple statements, or two conn.execute() calls
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS artists(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL 
                 )
                 """)
    conn.execute("""
                     CREATE TABLE IF NOT EXISTS albums(
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        year INTEGER,
                        artist_id INTEGER
                     )
                     """)

    conn.commit()
    print("artist & album table created")

    pass


def insert_data(conn: sqlite3.Connection) -> None:
    """
    Insert at least 3 artists and 6 albums into the database.
    Use any real or fictional music you like.
    """
    # TODO: insert rows into 'artists', then into 'albums'
    # Hint: use parameterized queries — conn.execute("INSERT INTO ... VALUES (?,?,?)", (val1, val2, val3))
    # Remember to conn.commit() when done

    artists_input = [("Evanescence",), ("Spiritbox",), ("MGK",), ("Nova Twins",)]
    albums_input = [
        ("Fallen", 2003, 1),
        ("Sanctuary", 2026, 1),
        ("Eternal Blue", 2021, 2),
        ("Tsunami Sea", 2025, 2),
        ("Tickets to my Downfall", 2020, 3),
        ("Mainstream Sellout", 2022, 3),
        ("Lost Americana", 2025, 3),
        ("Parasites & Butterflies", 2025, 4),
    ]
    conn.executemany("""
    INSERT INTO artists (name) VALUES (?)
""", artists_input)
    conn.executemany("""
    INSERT INTO albums (title, year, artist_id) VALUES (?, ?, ?)
""", albums_input)

    conn.commit()
    print("artists and albums inserted")

    pass


def query_albums(conn: sqlite3.Connection) -> list:
    """
    Return a list of all albums with their artist names.
    Each row should include: album title, year, and artist name.
    Order results by artist name, then by year.
    """
    # TODO: write a SELECT with a JOIN between albums and artists
    # Hint: SELECT albums.title, albums.year, artists.name FROM albums JOIN artists ...
    
    cursor = conn.execute("""
        SELECT albums.title,
               albums.year,
               artists.name
        FROM albums
        JOIN artists
            ON albums.artist_id = artists.id
        ORDER BY artists.name, albums.year
    """)

    return cursor.fetchall()
    pass


# ── Test block ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    create_tables(conn)

    insert_data(conn)

    results = query_albums(conn)
    print("Albums by artist:")
    for row in results:
        print(f"  {row['name']} — {row['title']} ({row['year']})")

conn.close()

# Expected output (example — yours will differ based on your data):
# Albums by artist:
#   The Beatles — Abbey Road (1969)
#   The Beatles — Revolver (1966)
#   David Bowie — Ziggy Stardust (1972)
#   ...
