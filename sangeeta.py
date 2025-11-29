import csv # this code helps to load the users.csv and movies.csv files
import os  # this help create directories in the operating system (to create new csv filess kind of like pandas interacts directly with the terminal)
from datetime import datetime #

users_file = "source_files/users.csv" # directory inside files. the adress for .csv file for users
movies_file = "source_files/movies.csv"  #"                                           " for movies
borrow_file = "source_files/borrowings.csv" # calls to the creation of a new file with the borrowing history of the movies
# FIELDNAMES 
# ================================
user_fieldnames = ["user_id", "user_name"]
movie_fieldnames = ["movie_id", "title","director","year","available_copies"]      
borrow_fieldnames = ["user_id", "movie_id", "borrow_date","return_date"] 
# ================================
# CSV HELPERS                       # changed the file names for the functions have to change the 
# ================================

def load_csv(users_file): #USERS_FILE is changed to the users_file
    if not os.path.exists(users_file):
        return []
    with open(users_file, newline="", encoding="utf-8") as file: # newline is specifically for windows  , utf - ensures special characters work 
        reader = csv.DictReader(file)
        return list(reader)

def save_csv(users_file, data, fieldnames):
    with open(users_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def generate_new_id(records,id_field):
    if not records:
        return 1
    return max(int(r[id_field]) for r in records) + 1

# ================================
# USER MANAGEMENT
# ================================

# --------------- First load the .csv file and create new id then replace file name with the names of the files--------


def add_user():
    users = load_csv(users_file)
    name = input("Enter user name: ").strip() # removes spaces 
    if not name:
        print("Name cannot be empty.")
        return

    user_id = generate_new_id(users,"user_id")
    users.append({"user_id":str(user_id), "user_name":name})
    save_csv(users_file, users, ["user_id", "user_name"])
    print(f"User added with ID: {user_id}")

    #  -------------- this part is for printing the users and also the error management system ---- 

def view_users():
    users = load_csv(users_file)
    if not users:
        print("No users found.")
        return

    print("\n---☻☺☻☺☻☺ THESE ARE OUR CURRENT USERS  ☺☻☺☻☺☻ ---") # Header for the information don bellow  /n iss ssignaling the program for a new line in the printed information
    for u in users:
        print(f"{u['user_id']}: {u['user_name']}")
    print("-----••••••-----")  #

# ================================
# MOVIE MANAGEMENT
# ================================

def add_movie():
    movies = load_csv(movies_file)

    title = input("Enter movie title: ").strip()
    director = input("Enter director: ").strip()
    year = input("Enter release year: ").strip()
    copies = input("Enter number of copies: ").strip()

    if not title or not director or not year.isdigit() or not copies.isdigit():
        print("Invalid input.")
        return

    movie_id = generate_new_id(movies,"movie_id") #generating new movie id
    movies.append({
        "movie_id": str(movie_id),
        "title": title,
        "director": director,
        "year": year,
        "available_copies": copies
    })

    save_csv(movies_file, movies, movie_fieldnames)
    print(f"Movie added with ID: {movie_id}")

def view_movies():
    movies = load_csv(movies_file)
    if not movies:
        print("No movies found.")
        return

    print("\n--- movies ---")
    for m in movies:
        print(f"{m['movie_id']} | {m['title']} | {m['director']} | {m['year']} | Copies: {m['available_copies']}")
    print("--------------")

# ================================
# BORROWING MOVIES
# ================================

def borrow_movies():
    users = load_csv(users_file)
    movies = load_csv(movies_file)
    borrowings = load_csv(borrow_file)

    user_id = input("User ID: ").strip()
    if not any(u["user_id"]== user_id for u in users):
        print("User not found.")
        return

    movie_ids = [mid.strip() for mid in input("Enter Movie IDs (comma separated): ").split(",") if mid.strip()]
    movies_dict = {str(m["movie_id"]): m for m in movies}
    
    unavailable = []
    for mid in movie_ids:
        movie = movies_dict.get(mid)
        if not movie:
            unavailable.append(f"{mid} (not found)")
        elif int(movie["available_copies"]) <= 0:
            unavailable.append(f"{mid} ({movie['title']} - no copies)")

    if unavailable:
        print("\nUnavailable:")
        for u in unavailable:
            print(" -", u)
        print("No movies have been borrowed.")
        return
    # Deduct copies and create borrow records
    today = datetime.now().strftime("%Y-%m-%d")
    for mid in movie_ids:
        movies_dict[mid]["available_copies"] = str(int(movies_dict[mid]["available_copies"]) - 1) # Deduct available copies
    
    # Add a new row in borrow CSV
        borrowings.append({
            "user_id": user_id,
             "movie_id": mid,
             "borrow_date": today,
             "return_date": "" # empty until returned
    }) 
  
    save_csv(movies_file, list(movies_dict.values()), movie_fieldnames)
    save_csv(borrow_file, borrowings, borrow_fieldnames)
    print("Movies borrowed successfully!")

# ================================
# RETURN MOVIES
# ================================

def return_movies():
    movies = load_csv(MOVIES_FILE)
    movies_dict = {str(m["id"]): m for m in movies}
    borrowings = load_csv(BORROW_FILE)

    user_id = input("User ID: ").strip()
    record = next((b for b in borrowings if b["user_id"] == user_id), None)
    if not record:
        print("User has no borrowings.")
        return

    to_return = [mid.strip() for mid in input("Enter Movie IDs to return: ").split(",") if mid.strip()]
    borrowed = set(record["movie_ids"].split(",")) if record["movie_ids"].strip() else set()
    actually_returned = []

    for mid in to_return:
        if mid in borrowed:
            if mid in movies_dict:
                movies_dict[mid]["copies"] = str(int(movies_dict[mid]["copies"]) + 1)
            borrowed.remove(mid)
            actually_returned.append(mid)

    if not actually_returned:
        print("No valid movies returned.")
        return

    if borrowed:
        record["movie_ids"] = ",".join(borrowed)
    else:
        borrowings = [b for b in borrowings if b["user_id"] != user_id]

    save_csv(MOVIES_FILE, list(movies_dict.values()), ["id", "title", "director", "year", "copies"])
    borrowings = [b for b in borrowings if b.get("movie_ids", "").strip()]
    save_csv(BORROW_FILE, borrowings, ["user_id", "movie_ids", "date"])
    print("Movies returned successfully!")

# ================================
# LIST BORROWED MOVIES
# ================================

def list_borrowed_movies():
    movies = load_csv(MOVIES_FILE)
    movies_dict = {str(m['id']): m for m in movies}
    borrowings = load_csv(BORROW_FILE)

    user_id = input("User ID: ").strip()
    record = next((b for b in borrowings if b["user_id"] == user_id), None)
    if not record or not record.get("movie_ids", "").strip():
        print("No borrowings found for this user.")
        return

    borrowed_ids = [mid for mid in record["movie_ids"].split(",") if mid.strip()]
    print("\n--- Borrowed Movies ---")
    print("Borrowing Date:", record.get("date", "N/A"))
    for mid in borrowed_ids:
        movie = movies_dict.get(mid)
        if movie:
            print(f"{mid}: {movie['title']}")
        else:
            print(f"{mid}: [Movie not found]")
    print("-----------------------")

# ================================
# MENU
# ================================

def main_menu():
    while True:
        print("\n===== MOVIE MANAGEMENT SYSTEM (CSV) =====")
        print("1. Add User")
        print("2. View Users")
        print("3. Add Movie")
        print("4. View Movies")
        print("5. Borrow Movies")
        print("6. Return Movies")
        print("7. List Borrowed Movies")
        print("8. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            add_user()
        elif choice == "2":
            view_users()
        elif choice == "3":
            add_movie()
        elif choice == "4":
            view_movies()
        elif choice == "5":
            borrow_movies()
        elif choice == "6":
            return_movies()
        elif choice == "7":
            list_borrowed_movies()
        elif choice == "8":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main_menu()

