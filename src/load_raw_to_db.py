import os
import json
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
cur = conn.cursor()

# Create RAW schema and table
cur.execute("""
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT,
    channel_name TEXT,
    message_date TIMESTAMP,
    message_text TEXT,
    views INTEGER,
    forwards INTEGER,
    has_media BOOLEAN,
    image_path TEXT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

# Path to JSON files
RAW_DIR = "data/raw/telegram_messages"

# Insert query
insert_query = """
INSERT INTO raw.telegram_messages (
    message_id,
    channel_name,
    message_date,
    message_text,
    views,
    forwards,
    has_media,
    image_path
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

# Read JSON files and insert data
for root, _, files in os.walk(RAW_DIR):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                messages = json.load(f)

            for msg in messages:
                cur.execute(
                    insert_query,
                    (
                        msg["message_id"],
                        msg["channel_name"],
                        msg["message_date"],
                        msg["message_text"],
                        msg["views"],
                        msg["forwards"],
                        msg["has_media"],
                        msg["image_path"],
                    )
                )

            print(f"Loaded {len(messages)} records from {file_path}")

# Commit and close
conn.commit()
cur.close()
conn.close()

print("✅ Raw Telegram data loaded successfully")
