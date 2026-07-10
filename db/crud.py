import sqlite3

from db.database import get_db_connection


def get_user_credits(email: str) -> int:
    """التحقق من رصيد المستخدم."""
    conn = get_db_connection()
    user = conn.execute(
        "SELECT credits FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user["credits"] if user else 0


def create_user_if_not_exists(email: str):
    """إنشاء مستخدم جديد بـ 5 أرصدة مجانية إذا لم يكن مسجلاً."""
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO users (email, credits) VALUES (?, 5)", (email,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()


def deduct_credit(email: str) -> bool:
    """خصم رصيد بعد استخدام الأداة."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET credits = credits - 1 WHERE email = ? AND credits > 0",
        (email,),
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
