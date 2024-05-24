import sqlite3

def create_connection():
    return sqlite3.connect('urls.db')

def setup_database():
    conn = create_connection()
    with conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY,
            original TEXT NOT NULL,
            short TEXT NOT NULL
        )
        ''')
    conn.close()

if __name__ == '__main__':
    setup_database()
