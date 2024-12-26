import sqlite3
from datetime import datetime, date, timedelta, time
from analysis import analysis_screen_menu

current_user_id = None

def main_menu(current_user_id):  # Main menu
    while True:
        print("Main Menu")
        print("1. Add/delete habit")
        print("2. Check-off Habit")
        print("3. Analysis Screen")
        print("4. Exit Program")
        main_menu_choice = input("Enter your choice: ")

        if main_menu_choice == '1':
            list_of_habits_menu(current_user_id)
        elif main_menu_choice == '2':
            check_off_habit_menu(current_user_id)
        elif main_menu_choice == '3':
            analysis_screen_menu(current_user_id)
        elif main_menu_choice == '4':
            print("You have been logged out.")
            break 
        else:
            print("Invalid choice.")

def list_of_habits_menu(current_user_id): # Habits menu
    while True:
        print("Add/delete Habits")
        print("1. Add habit")
        print("2. Delete habit")
        print("3. Main Menu")
        habit_choice = input("Enter your choice: ")

        if habit_choice == '1':
            add_habit(current_user_id)
        elif habit_choice == '2':
            delete_habit(current_user_id)
        elif habit_choice == '3':
            break 
        else:
            print("Invalid choice.")
            time.sleep(1)  

def add_habit(current_user_id):  # Add habit
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT Habit_name FROM Habits WHERE User_id = ?
    ''', (current_user_id,))

    results = cursor.fetchall()

    print("Habits already created:")
    if not results:
        print("No habits found.")
    else:
        for i, habit in enumerate(results, start=1):
            print(f"{i}. {habit[0]}")

    habit_name = input("Enter the name of Your habit: ")
    
    while True:
        periodicity = input("Enter the periodicity of the habit (daily or weekly): ").strip().lower()
        if periodicity in ['daily', 'weekly']:
            break
        else:
            print("Invalid input. Please enter 'daily' or 'weekly'.")

    while True:
        goal = input("Enter the goal for the habit (number of times per period): ")
        if goal.isdigit() and int(goal) > 0:
            goal = int(goal)  # Convert to integer
            break
        else:
            print("Invalid input. Please enter a positive integer.")

    creation_date = datetime.now().strftime('%Y-%m-%d')  
    current_strike = 0  
    longest_strike = 0  

    try:
        cursor.execute('''
            INSERT INTO Habits (User_id, Habit_name, Periodicity, Goal, Creation_date, Current_strike, Longest_strike)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (current_user_id, habit_name, periodicity, goal, creation_date, current_strike, longest_strike))
        
        conn.commit()
        print("New habit created successfully!")
    except sqlite3.IntegrityError:
        print("An error occurred: Integrity error. Please check your input.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def delete_habit(current_user_id): # Delete habit
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Habit_name FROM Habits WHERE User_id = ?', (current_user_id,))
    results = cursor.fetchall()

    print("Habits which can be deleted:")
    if not results:
        print("No habits found for deletion.")
    else:
        for i, habit in enumerate(results, start=1):
            print(f"{i}. {habit[0]}") 
            
    habit_name = input("Enter the name of the habit you want to delete: ")
    
    try:
        cursor.execute('SELECT * FROM Habits WHERE Habit_name = ? AND User_id = ?', (habit_name, current_user_id))
        habit = cursor.fetchone()
        
        if habit:
            # Ask for confirmation
            confirm = input(f"Are you sure you want to delete the habit '{habit_name}'? (yes/no): ").strip().lower()
            if confirm == 'yes':
                cursor.execute('DELETE FROM Habits WHERE Habit_name = ? AND User_id = ?', (habit_name, current_user_id))
                conn.commit()
                print(f"Habit '{habit_name}' deleted successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print(f"No habit found with the name '{habit_name}' for the current user.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        conn.close()

def check_off_habit_menu(current_user_id): # Check off menu
    while True:
        print("Check-off Habit Menu")
        print("1. Habit Check-off")
        print("2. Check Progress")
        print("3. Main Menu")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            check_off_habit(current_user_id)
        elif choice == '2':
            check_progress(current_user_id)
        elif choice == '3':
            break 
        else:
            print("Invalid choice.")
            time.sleep(1)  

def check_off_habit(current_user_id): # Check off
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT Habit_name FROM Habits WHERE User_id = ?
    ''', (current_user_id,))
    
    results = cursor.fetchall()

    print("Habits which can be checked off:")
    if not results:
        print("No habits found.")
        return  

    for i, habit in enumerate(results, start=1):
        print(f"{i}. {habit[0]}") 

    habit_choice = input("Enter the number of the habit you want to check off: ")

    try:
        habit_index = int(habit_choice) - 1 
        if 0 <= habit_index < len(results):
            habit_name = results[habit_index][0] 
            
            cursor.execute('''
                SELECT Habit_id, Current_strike, Longest_strike, Goal, Periodicity FROM Habits 
                WHERE Habit_name = ? AND User_id = ?
            ''', (habit_name, current_user_id))
            
            habit = cursor.fetchone()
            
            if habit:
                habit_id, current_strike, longest_strike, goal, periodicity = habit
                
                today = datetime.now().strftime('%Y-%m-%d')
                cursor.execute('''
                    SELECT COUNT(*) FROM Habit_Completion 
                    WHERE Habit_id = ? AND Completion_date = ?
                ''', (habit_id, today))
                
                completion_count = cursor.fetchone()[0]
                
                if completion_count >= goal:
                    print(f"You have already met your goal of {goal} for '{habit_name}' today.")
                else:
                    cursor.execute('''
                        INSERT INTO Habit_Completion (Habit_id, Completion_date, Completion_time)
                        VALUES (?, ?, ?)
                    ''', (habit_id, today, datetime.now().strftime('%H:%M:%S')))
                    
                    completion_count += 1
                    
                    if completion_count == goal:
                        current_strike += 1
                        if current_strike > longest_strike:
                            longest_strike = current_strike
                    
                    cursor.execute('''
                        UPDATE Habits 
                        SET Current_strike = ?, Longest_strike = ?
                        WHERE Habit_id = ?
                    ''', (current_strike, longest_strike, habit_id))
                    
                    conn.commit()
                    print(f"Habit '{habit_name}' checked off successfully!")
            else:
                print(f"No habit found with the name '{habit_name}' for the current user.")
        else:
            print("Invalid choice. Please try again.")
    
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        conn.close()

def check_progress(current_user_id, completion_date=None): # Progress check
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    
    if completion_date is None:
        completion_date = datetime.now().date()

    try:
        cursor.execute('''
            SELECT Habit_id, Habit_name, Goal FROM Habits WHERE User_id = ?
        ''', (current_user_id,))
        
        habits = cursor.fetchall()
        
        if not habits:
            print("No habits found for this user.")
            return
        
        print(f"Progress check on {completion_date}:")
        for i, habit in enumerate(habits, start=1):
            habit_id, habit_name, goal = habit
            
            cursor.execute('''
                SELECT COUNT(*) FROM Habit_Completion 
                WHERE Habit_id = ? AND Completion_date = ?
            ''', (habit_id, completion_date))
            
            done = cursor.fetchone()[0]
            progress_percentage = (done / goal) * 100 if goal > 0 else 0
            
            print(f"{i}. {habit_name}, Done: {done}, Goal: {goal}, Progress: {progress_percentage:.2f}%")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()