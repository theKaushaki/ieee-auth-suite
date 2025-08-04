import sqlite3
import os

DATABASE_FILE = 'certificates.db'

def init_db(schema_file='schema.sql'):
    if os.path.exists(DATABASE_FILE):
        print("Database already exists. Skipping initialization.")
        return
    
    print("Initializing new database...")
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            with open(schema_file, 'r') as f:
                conn.executescript(f.read())
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def article_exists(article_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM certificates WHERE article_name = ?", (article_name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# 

def add_certificate(cert_id, author, article, timestamp, pdf_path):
    """
    Adds a new certificate record and generates a unique public_id, exist kareni jadi
    """
    conn = get_db_connection()
    public_id = None
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO certificates (certificate_id, author_name, article_name, generation_timestamp, pdf_path) VALUES (?, ?, ?, ?, ?)",
                (cert_id, author, article, timestamp, pdf_path)
            )

            last_id = cursor.lastrowid

            public_id = f"IEEE-RP-{last_id:04d}" # Change the format later, vella id
            conn.execute(
                "UPDATE certificates SET public_id = ? WHERE id = ?",
                (public_id, last_id)
            )

        print(f"Successfully added record for '{article}' with Public ID: {public_id}")
        return public_id

    except sqlite3.IntegrityError:
        print(f"Record for '{article}' already exists. Skipping.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()