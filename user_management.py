import sqlite3
from habit_management import main_menu
from datetime import datetime, date, timedelta, time

current_user_id = None

def start():
    print("Welcome to the habits tracking app")
    print("1. Choose user")
    print("2. Add new user")
    print("3. Delete existing user")
    print("4. Exit")
    start_choice = input("Enter your choice: ")
    
    if start_choice == '1':
        choose_user()
    elif start_choice == '2':
        add_user()
    elif start_choice == '3':
        delete_user()
    elif start_choice == '4':    
        exit_app()  # Call exit_app() to terminate the program
    else:
        print("Invalid choice.")
        start()  # Restart the menu if the choice is invalid

def choose_user():
    global current_user_id  # Declare as global to modify it

    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT User_id, User_name FROM Users")
    users = cursor.fetchall()

    if not users:
        print("No users found. Please add a user first.")
        add_user()
        conn.close()
        return

    print("Users:")
    if not users:
        print("No users found.")
    else:
        for i, user in enumerate(users, start=1):
            print(f"{i}. {user[1]}")  # Print the user name with an index

    chosen_index = input("Enter the number of the user to log in: ")
    try:
        chosen_index = int(chosen_index)  # Convert input to integer
        if 1 <= chosen_index <= len(users):
            current_user_id = users[chosen_index - 1][0]  # Get the User_id
            print(f"Welcome: {users[chosen_index - 1][1]}!")  # Welcome message
            update_habits_on_login(current_user_id) # update
            main_menu(current_user_id)  # Call the main menu with the user ID
        else:
            print("Invalid choice. Please try again.")
            choose_user()
    except ValueError:
        print("Invalid input. Please enter a number.")
        choose_user()

    conn.close()

def add_user():
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    
    new_user = input("Enter the new user's name: ")
    
    try:
        cursor.execute("INSERT INTO Users (User_name) VALUES (?)", (new_user,))
        conn.commit()
        print(f"New user created: {new_user}!")
    except sqlite3.IntegrityError:
        print("User  already exists. Please choose a different name.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
        start()

def delete_user():
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT User_id, User_name FROM Users")
    users = cursor.fetchall()

    if not users:
        print("No users found to delete.")
        conn.close()
        return

    print("Users which can be deleted:")
    for user in users:
        print(user[1])

    chosen_username = input("Enter the username which You want to delete: ")
    cursor.execute("SELECT User_id FROM Users WHERE User_name = ?", (chosen_username,))
    user = cursor.fetchone()

    if user:
        confirm = input(f"Are you sure you want to delete the user '{chosen_username}'? (yes/no): ").lower()
        if confirm == 'yes':
            cursor.execute("DELETE FROM Users WHERE User_id = ?", (user[0],))
            conn.commit()
            print(f"User  '{chosen_username}' has been deleted.")
        else:
            print("Deletion cancelled.")
    else:
        print("User  not found.")

    conn.close()
    start()

def exit_app():
    
    print("Exiting the application...")
    exit()  # Exit the program with a status code of 0 (indicating success)

def update_habit_strike(habit_id, completion_date, completion_time, periodicity):
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    
    # Check if the habit was completed on the previous day/week
    if periodicity == 'daily':
        previous_day = completion_date - timedelta(days=1)
        cursor.execute('''
        SELECT COUNT(*)
        FROM Habit_Completion
        WHERE Habit_id = ? AND Completion_date = ?
        ''', (habit_id, previous_day))
    elif periodicity == 'weekly':
        previous_week_start = completion_date - timedelta(weeks=1)
        cursor.execute('''
        SELECT COUNT(*)
        FROM Habit_Completion
        WHERE Habit_id = ? AND Completion_date >= ? AND Completion_date < ?
        ''', (habit_id, previous_week_start, completion_date))
    
    previous_period_completion = cursor.fetchone()[0]
    
    # Convert completion_time to string format
    completion_time_str = completion_time.strftime("%H:%M:%S")  # Convert time to string
    
    # Update the Habit_Completion table
    cursor.execute('''
    INSERT INTO Habit_Completion (Habit_id, Completion_date, Completion_time)
    VALUES (?, ?, ?)
    ''', (habit_id, completion_date, completion_time_str))  # Use the string format for time
    
    # Update the Habits table
    if previous_period_completion > 0:
        # Habit was completed on the previous day/week, so increment the current strike
        cursor.execute('''
        UPDATE Habits
        SET Current_strike = Current_strike + 1
        WHERE Habit_id = ?
        ''', (habit_id,))
        
        # Update the Longest_strike if necessary
        cursor.execute('''
        SELECT Current_strike, Longest_strike
        FROM Habits
        WHERE Habit_id = ?
        ''', (habit_id,))
        
        current_strike, longest_strike = cursor.fetchone()
        
        if current_strike > longest_strike:
            cursor.execute('''
            UPDATE Habits
            SET Longest_strike = Current_strike
            WHERE Habit_id = ?
            ''', (habit_id,))
    else:
        # Habit was not completed on the previous day/week, so reset the current strike
        cursor.execute('''
        UPDATE Habits
        SET Current_strike = 0
        WHERE Habit_id = ?
        ''', (habit_id,))
    
    conn.commit()
    conn.close()

def update_habits_on_login(user_id):
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    
    # Retrieve all habits for the user
    cursor.execute('''
    SELECT Habit_id, Periodicity, Current_strike
    FROM Habits
    WHERE User_id = ?
    ''', (user_id,))
    
    habits = cursor.fetchall()
    
    # Get today's date and time
    today = date.today()
    current_time = datetime.now().time()
    
    # Update each habit
    for habit in habits:
        habit_id, periodicity, current_strike = habit
        
        # Check if the habit needs to be updated
        if periodicity == 'daily':
            # Check if the habit was completed yesterday
            last_completion_date = today - timedelta(days=1)
            update_habit_strike(habit_id, last_completion_date, current_time, periodicity)
        elif periodicity == 'weekly':
            # Check if the habit was completed in the last week
            last_completion_date = today - timedelta(weeks=1)
            update_habit_strike(habit_id, last_completion_date, current_time, periodicity)
    print("Habits has been updated")
    conn.commit()
    conn.close()