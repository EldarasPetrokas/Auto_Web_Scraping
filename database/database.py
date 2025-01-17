import sqlite3
import datetime

def init_db():
    """Initialize the database and create the ads table if it doesn't exist."""
    conn = sqlite3.connect('database/ads.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT UNIQUE,
            name TEXT,
            year TEXT,
            price TEXT,
            sent_to_telegram INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_to_database(ads):
    """Save ads to the database, avoiding duplicates."""
    conn = sqlite3.connect('database/ads.db')
    cursor = conn.cursor()

    for ad in ads:
        try:
            cursor.execute("""
                INSERT INTO ads (link, name, year, price) VALUES (?, ?, ?, ?)
            """, (ad['link'], ad['name'], ad['year'], ad['price']))
            conn.commit()
            print(f"Ad saved: {ad['name']} ({ad['link']})")
        except sqlite3.IntegrityError:
            print(f"Ad already exists in database: {ad['link']}")

    conn.close()


def get_unsent_ads():
    """Retrieve all ads that have not been sent to Telegram."""
    conn = sqlite3.connect('database/ads.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT link, name, year, price FROM ads WHERE sent_to_telegram = 0
    """)
    ads = cursor.fetchall()
    conn.close()
    return ads


def mark_as_sent(link):
    """Mark an ad as sent to Telegram."""
    conn = sqlite3.connect('database/ads.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ads SET sent_to_telegram = 1 WHERE link = ?
    """, (link,))
    conn.commit()
    conn.close()


def delete_old_ads(days=30):
    """
    Delete ads older than a certain number of days.

    Args:
        days (int): The number of days to keep ads in the database.
    """
    conn = sqlite3.connect('database/ads.db')
    cursor = conn.cursor()

    # Calculate the timestamp cutoff
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
    cursor.execute("""
        DELETE FROM ads WHERE created_at < ?
    """, (cutoff_date,))
    conn.commit()
    conn.close()
    print(f"Deleted ads older than {days} days.")


