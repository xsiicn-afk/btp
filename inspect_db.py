import sqlite3
from pathlib import Path

# Найдем базу автоматически
candidates = [
    Path("database/database.db"),
    Path("data/database.db"),
    Path("database.db"),
]

db_path = None
for p in candidates:
    if p.exists():
        db_path = p
        break

if db_path is None:
    print("База не найдена.")
    print("Файлы .db в проекте:")
    for p in Path(".").rglob("*.db"):
        print(" ", p)
    raise SystemExit

print(f"База: {db_path}")

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

print("\n=== builds ===")
for row in conn.execute("PRAGMA table_info(builds)"):
    print(tuple(row))

print("\n=== build_items ===")
for row in conn.execute("PRAGMA table_info(build_items)"):
    print(tuple(row))