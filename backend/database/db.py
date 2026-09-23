from pathlib import Path
import sqlite3
import json


ROOT = Path(__file__).resolve().parents[2]

DATABASE = (
    ROOT /
    "database" /
    "nlp_shield.db"
)


def init_db():

    DATABASE.parent.mkdir(
        exist_ok=True
    )

    with sqlite3.connect(
        DATABASE
    ) as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                result_json TEXT NOT NULL,
                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()


def save_analysis(
    text,
    result
):

    init_db()

    with sqlite3.connect(
        DATABASE
    ) as connection:

        cursor = connection.execute(
            """
            INSERT INTO analyses
            (text, result_json)
            VALUES (?, ?)
            """,
            (
                text,
                json.dumps(
                    result
                )
            )
        )

        connection.commit()

        return cursor.lastrowid


def get_recent(
    limit=20
):

    init_db()

    with sqlite3.connect(
        DATABASE
    ) as connection:

        rows = connection.execute(
            """
            SELECT
                id,
                text,
                result_json,
                created_at
            FROM analyses
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                limit,
            )
        ).fetchall()

    return [
        {
            "id": row[0],
            "text": row[1],
            "result": json.loads(
                row[2]
            ),
            "created_at": row[3]
        }
        for row in rows
    ]
