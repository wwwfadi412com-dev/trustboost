import os
import sqlite3


# نستخدم /tmp في السحابة (Streamlit Cloud)، أو المجلد الحالي في الجهاز المحلي.
DB_NAME = "/tmp/trustboost.db" if os.path.isdir("/tmp") else "trustboost.db"


def get_db_connection():
    """إنشاء اتصال بقاعدة البيانات مع إرجاع الصفوف كـ Dictionary."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """إنشاء الجداول إذا لم تكن موجودة."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            credits INTEGER DEFAULT 5
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS search_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT UNIQUE NOT NULL,
            results_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()
