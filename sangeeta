import csv
import os
from datetime import datetime

USERS_FILE = "source_files/users.csv"
MOVIES_FILE = "source_files/movies.csv"
BORROW_FILE = "source_files/borrowings.csv"

# ================================
# CSV HELPERS
# ================================

def load_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_csv(filename, data, fieldnames):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def generate_new_id(records):
    if not records:
        return 1
    return max(int(r["id"]) for r in records) + 1

# ================================
# USER MANAGEMENT
# ================================

def add_user():
    users = load_csv(USERS_FILE)
    name = input("Enter user name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    user_id = generate_new_id(users)
    users.append({"id": user_id, "name": name})
    save_csv(USERS_FILE, users, ["id", "name"])

    print(f"User added with ID: {user_id}")

def view_users():
    users = load_csv(USERS_FILE)
    if not users:
        print("No users found.")
        return

    print("\n--- USERS ---")
    for u in users:
        print(f"{u['id']}: {u['name']}")
    print("-------------")

# ================================
# MOVIE MANAGEMENT
# ================================

def add_movie():
    movies = load_csv(MOVIES_FILE)

    title = in
