def load_file(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print(f"Error: {filename} is corrupted. Initializing with empty data.")
            return []
