
import json
import os

DB_PATH = "database.json"

def load_db():
    """Database-г унших."""
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)

    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    """Database-г хадгалах."""
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def create_user(user_id):
    """Шинэ тоглогч үүсгэх."""
    db = load_db()

    if str(user_id) in db:
        return False  # аль хэдийн бүртгэлтэй

    db[str(user_id)] = {
        "moonstone": 5000,   # шинэ тоглогч wallet-д (төвч: moon)
        "exp": 0,
        "level": 0,
        "bank": 0,
        # cooldown талбарууд (ISO дататай)
        "last_daily": None,
        "last_slot": None,
        "last_roulette": None,
        "last_raid": None,
        "last_robbank": None,
        "last_action": None,
        "username": None
    }

    save_db(db)
    return True

def get_user(user_id):
    """Тоглогчийн мэдээлэл авах."""
    db = load_db()
    return db.get(str(user_id), None)

def update_user(user_id, key, value):
    """Тодорхой property-г шинэчлэх (set)."""
    db = load_db()
    if str(user_id) not in db:
        return False

    db[str(user_id)][key] = value
    save_db(db)
    return True

def inc_user(user_id, key, amount):
    """Тоо нэмэх/хасах (increment)."""
    db = load_db()
    if str(user_id) not in db:
        return False
    db[str(user_id)].setdefault(key, 0)
    db[str(user_id)][key] = db[str(user_id)].get(key, 0) + amount
    save_db(db)
    return True
