import sqlite3
from habit_management import main_menu
from datetime import datetime, date, timedelta, time

current_user_id = None

def start():  # Start app and User Menu
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
        exit_app()
    else:
        print("Invalid choice.")
        start()

def choose_user(): # Choose user(login function)
    global current_user_id  

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
            print(f"{i}. {user[1]}") 

    chosen_index = input("Enter the number of the user to log in: ")
    try:
        chosen_index = int(chosen_index)  
        if 1 <= chosen_index <= len(users):
            current_user_id = users[chosen_index - 1][0]  
            print(f"Welcome: {users[chosen_index - 1][1]}!") 
            update_habits_on_login(current_user_id) 
            main_menu(current_user_id) 
        else:
            print("Invalid choice. Please try again.")
            choose_user()
    except ValueError:
        print("Invalid input. Please enter a number.")
        choose_user()

    conn.close()

def add_user(): # Add user
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

def delete_user(): # Delete user
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

def exit_app(): # Exit App
    
    print("Exiting the application...")
    exit()  # Exit the program with a status code of 0 (indicating success)

def update_habit_strike(habit_id, completion_date, completion_time, periodicity):  # Update single habit
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    
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
    
    completion_time_str = completion_time.strftime("%H:%M:%S") 
    
    cursor.execute('''
    INSERT INTO Habit_Completion (Habit_id, Completion_date, Completion_time)
    VALUES (?, ?, ?)
    ''', (habit_id, completion_date, completion_time_str))  
    
    if previous_period_completion > 0:
        cursor.execute('''
        UPDATE Habits
        SET Current_strike = Current_strike
        WHERE Habit_id = ?
        ''', (habit_id,))
        
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
        cursor.execute('''
        UPDATE Habits
        SET Current_strike = 0
        WHERE Habit_id = ?
        ''', (habit_id,))
    
    conn.commit()
    conn.close()

def update_habits_on_login(user_id): # Update all habits strike during log in
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT Habit_id, Periodicity, Current_strike
    FROM Habits
    WHERE User_id = ?
    ''', (user_id,))
    
    habits = cursor.fetchall()
    
    today = date.today()
    current_time = datetime.now().time()
    
    for habit in habits:
        habit_id, periodicity, current_strike = habit
        
        if periodicity == 'daily':
            last_completion_date = today - timedelta(days=1)
            update_habit_strike(habit_id, last_completion_date, current_time, periodicity)
        elif periodicity == 'weekly':
            last_completion_date = today - timedelta(weeks=1)
            update_habit_strike(habit_id, last_completion_date, current_time, periodicity)
    print("Habits has been updated")
    conn.commit()
    conn.close()