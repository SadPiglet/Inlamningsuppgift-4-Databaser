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

def generate_personal_number(date_of_birth):
  date_parts = date_of_birth.split("-")

  year = date_parts[0]
  month = date_parts[1]
  day = date_parts[2]

  return f"{year[-2:]}{month}{day}-0000"


def add_user(connection):
  first_name = input("Enter first name: ").strip()
  last_name = input("Enter last name: ").strip()
  date_of_birth = input("Enter date of birth (YYYY-MM-DD): ").strip()
  age = calculate_age(date_of_birth)
  print(f"User's age is: {age}")
  personal_number = generate_personal_number(date_of_birth)

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

  print(f"User {first_name} {last_name} added successfully.")


connection = sqlite3.connect("users.db")
print("Database created and successfully connected to SQLite")

create_tables(connection)
add_user(connection)

connection.close()