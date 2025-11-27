#borrow function
def borrow_movies():
    users = load_csv(USERS_FILE)
    movies = load_csv(MOVIES_FILE)
    borrowings = load_csv(BORROW_FILE)

    user_id = input("User ID: ").strip()
    if not any(str(u["id"]) == user_id for u in users):
        print("User not found.")
        return

    movie_ids = [mid.strip() for mid in input("Enter Movie IDs (comma separated): ").split(",") if mid.strip()]
    movies_dict = {str(m["id"]): m for m in movies}
    
    # Check all requested movies for validity and availability
    unavailable = []
    for mid in movie_ids:
        movie = movies_dict.get(mid)
        if not movie:
            unavailable.append(f"{mid} (not found)")
        elif int(movie["copies"]) <= 0:
            unavailable.append(f"{mid} ({movie['title']} - no copies)")
    
    if unavailable:
        print("\nUnavailable:")
        for u in unavailable:
            print(" -", u)
        print("No movies have been borrowed.")
        return    # abort if ANY are unavailable
    
    # ALL requested movies are available -> proceed to borrow
    for mid in movie_ids:
        movies_dict[mid]["copies"] = str(int(movies_dict[mid]["copies"]) - 1)

    # Update/add borrowing record for the user
    record = next((b for b in borrowings if b["user_id"] == user_id), None)
    if record:
        current = set(record["movie_ids"].split(",")) if record["movie_ids"].strip() else set()
        new_borrowed = current.union(movie_ids)
        record["movie_ids"] = ",".join(new_borrowed)
        # Optionally, update date to current
        record["date"] = datetime.now().strftime("%Y-%m-%d")
    else:
        borrowings.append({
            "user_id": user_id,
            "movie_ids": ",".join(movie_ids),
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    
    # Save updates
    save_csv(MOVIES_FILE, list(movies_dict.values()), ["id", "title", "director", "year", "copies"])
    save_csv(BORROW_FILE, borrowings, ["user_id", "movie_ids", "date"])
    
    print("Movies borrowed successfully!")


#return
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
            # Only update if the movie exists (robustness)
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
        # All movies returned, so remove the borrowing record
        borrowings = [b for b in borrowings if b["user_id"] != user_id]

    save_csv(MOVIES_FILE, list(movies_dict.values()),
             ["id", "title", "director", "year", "copies"])
    # Remove any records where movie_ids is empty
    borrowings = [b for b in borrowings if b.get("movie_ids", "").strip()]
    save_csv(BORROW_FILE, borrowings, ["user_id", "movie_ids", "date"])

    print("Movies returned successfully!")

    #list borrowed movies for a user

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