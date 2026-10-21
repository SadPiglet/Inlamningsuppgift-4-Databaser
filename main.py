import sqlite3
from datetime import date

def calculate_age(date_of_birth):
  birth_date = date.fromisoformat(date_of_birth)
  today = date.today()

  age = today.year - birth_date.year

  if (today.month, today.day) < (birth_date.month, birth_date.day):
    age -= 1

  return age

def create_tables(connection):
  connection.execute("""
    CREATE TABLE IF NOT EXISTS Users (
      user_id INTEGER PRIMARY KEY AUTOINCREMENT,
      first_name TEXT NOT NULL,
      last_name TEXT NOT NULL,
      date_of_birth TEXT NOT NULL,
      personal_number TEXT NOT NULL UNIQUE
    )
  """)

  connection.execute("""
    CREATE TABLE IF NOT EXISTS SummerTrips (
      trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
      airline TEXT NOT NULL,
      booking_number TEXT NOT NULL UNIQUE,
      user_id INTEGER NOT NULL,
      FOREIGN KEY (user_id) REFERENCES Users (user_id)
    )
  """)

  connection.commit()

def generate_personal_number(connection, date_of_birth):
  date_parts = date_of_birth.split("-")

  year = date_parts[0]
  month = date_parts[1]
  day = date_parts[2]

  date_prefix = f"{year[-2:]}{month}{day}"

  cursor = connection.execute("""
    SELECT personal_number
    FROM Users
    WHERE personal_number LIKE ?
  """, (f"{date_prefix}-%",))

  existing_numbers = cursor.fetchall()
  next_number = len(existing_numbers) + 1

  return f"{date_prefix}-{next_number:04d}"


def add_user(connection):
  first_name = input("Enter first name: ").strip()
  last_name = input("Enter last name: ").strip()
  date_of_birth = input("Enter date of birth (YYYY-MM-DD): ").strip()

  if not first_name or not last_name or not date_of_birth:
    print("All fields are required.")
    return

  try:
    age = calculate_age(date_of_birth)
    personal_number = generate_personal_number(connection, date_of_birth)

    connection.execute("""
      INSERT INTO Users (
        first_name, 
        last_name, 
        date_of_birth, 
        personal_number
      )
      VALUES (?, ?, ?, ?)
    """, (first_name, last_name, date_of_birth, personal_number))

    connection.commit()

    print(f"User's age is: {age}")
    print(f"User {first_name} {last_name} added successfully.")

  except ValueError:
    print("Error: Invalid date format. Please use YYYY-MM-DD.")

  except sqlite3.IntegrityError:
    print("Error: Personal number must be unique. This user may already exist.")

def add_summer_trip(connection):
  print("\nRegistered Users:")

  users = connection.execute("""
    SELECT user_id, first_name, last_name
    FROM Users
    ORDER BY user_id
  """).fetchall()

  if not users:
    print("No users found. Please add a user first.")
    return

  for user in users:
    print(f"{user[0]}: {user[1]} {user[2]}")

  try:
    user_id = int(input("Enter the user ID for the summer trip: ").strip())
  except ValueError:
    print("Error: Invalid user ID. Please enter a valid integer.")
    return

  selected_user = connection.execute(
    "SELECT user_id FROM Users WHERE user_id = ?", (user_id,)
  ).fetchone()

  if selected_user is None:
    print("Error: User ID not found. Please select a valid user ID.")
    return

  airline = input("Enter airline: ").strip()
  booking_number = input("Enter booking number: ").strip()

  if not airline or not booking_number:
    print("All fields are required.")
    return

  try:
    connection.execute("""
      INSERT INTO SummerTrips (
        airline, 
        booking_number, 
        user_id
      )
      VALUES (?, ?, ?)
    """, (airline, booking_number, user_id))

    connection.commit()

    print(f"Summer trip for user ID {user_id} added successfully.")

  except sqlite3.IntegrityError:
    print("Error: Booking number must be unique. This trip may already exist.")

def show_first_three_users(connection):
  print("\nFirst three registered users:")
  users = connection.execute("""
    SELECT user_id, first_name, last_name, date_of_birth, personal_number
    FROM Users
    ORDER BY user_id
    LIMIT 3
  """).fetchall()

  if not users:
    print("No users found.")
    return

  for user in users:
    print(
      f"ID: {user[0]}, "
      f"Name: {user[1]} {user[2]}, "
      f"Date of Birth: {user[3]}, "
      f"Personal Number: {user[4]}"
    )

def show_all_users(connection):
  users = connection.execute("""
    SELECT user_id, first_name, last_name, date_of_birth, personal_number
    FROM Users
    ORDER BY user_id
  """).fetchall()

  if not users:
    print("No users found.")
    return

  print("\nAll registered users:")
  for user in users:
    print(
      f"ID: {user[0]}, "
      f"Name: {user[1]} {user[2]}, "
      f"Date of Birth: {user[3]}, "
      f"Personal Number: {user[4]}"
    )
# -- Meny --
def manage_users(connection):
  while True:
    print("\n=== User Management Menu ===")
    print("1. Add user")
    print("2. Remove user")
    print("3. Show all users")
    print("4. Show first three users")
    print("5. Back to Main Menu")

    choice = input("Enter your choice (1-5): ").strip()

    if choice == "1":
      add_user(connection)
    elif choice == "2":
      remove_user(connection)
    elif choice == "3":
      show_all_users(connection)
    elif choice == "4":
      show_first_three_users(connection)
    elif choice == "5":
      break
    else:
      print("Invalid choice. Please try again.")

def manage_summer_trips(connection):
  while True:
    print("\n=== Summer Trip Management Menu ===")
    print("1. Add summer trip")
    print("2. Remove summer trip")
    print("3. Show all summer trips")
    print("4. Back to Main Menu")

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
      add_summer_trip(connection)
    elif choice == "2":
      remove_summer_trip(connection)
    elif choice == "3":
      show_all_summer_trips(connection)
    elif choice == "4":
      break
    else:
      print("Invalid choice. Please try again.")

def view_database_information(connection):
  while True:
    print("\n=== Database Information Menu ===")
    print("1. Show all users")
    print("2. Show all summer trips with user information")
    print("3. Show first three users")
    print("4. Back to Main Menu")

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
      show_all_users(connection)
    elif choice == "2":
      show_all_summer_trips(connection)
    elif choice == "3":
      show_first_three_users(connection)
    elif choice == "4":
      break
    else:
      print("Invalid choice. Please try again.")

def main_menu(connection):
  while True:
    print("\n=== Main Menu ===")
    print("1. Manage Users")
    print("2. Manage Summer Trips")
    print("3. View Database Information")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
      manage_users(connection)
    elif choice == "2":
      manage_summer_trips(connection)
    elif choice == "3":
      view_database_information(connection)
    elif choice == "4":
      print("Goodbye!")
      break
    else:
      print("Invalid choice. Please try again.")

connection = sqlite3.connect("users.db")
print("Database created and successfully connected to SQLite")

if __name__ == "__main__":
  connection = sqlite3.connect("users.db")

  try:
    connection.execute("PRAGMA foreign_keys = ON")
    create_tables(connection)
    print("Database connected and tables created successfully.")
    main_menu(connection)
  finally:
    connection.close()
    print("Database connection closed.")