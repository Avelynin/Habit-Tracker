import sqlite3

def analysis_screen_menu(current_user_id):
    while True:
        print("Analysis Screen")
        print("1. List of tracked habits")
        print("2. List of habits with the same periodicity")
        print("3. Longest run streak of all defined habits")
        print("4. Longest run streak of chosen habit")
        print("5. Main Menu")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            list_of_tracked_habits(current_user_id)
        elif choice == '2':
            list_of_habits_with_the_same_periodicity(current_user_id)
        elif choice == '3':
            longest_run_streak_of_all_defined_habits(current_user_id)    
        elif choice == '4':
            longest_run_streak_of_chosen_habit(current_user_id)  
        elif choice == '5':
            break  # Go back to the main menu
        else:
            print("Invalid choice.")
            time.sleep(1)  # Pause for 1 second before showing the menu again

def list_of_tracked_habits(current_user_id):
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Habit_name FROM Habits WHERE User_id = ?', (current_user_id,))
    
    results = cursor.fetchall()
    print("Your current tracked habits:")
    
    if not results:
        print("No habits found.")
    else:
        for i, habit in enumerate(results, start=1):
            print(f"{i}. {habit[0]}")
    
    conn.close()

def list_of_habits_with_the_same_periodicity(current_user_id):
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    
    print("Choose the type of habits you want to see:")
    print("1. Daily habits")
    print("2. Weekly habits")
    print("3. All habits")
    
    choice = input("Enter the number of your choice: ")
    
    if choice == "1":
        cursor.execute('SELECT Habit_name FROM Habits WHERE User_id = ? AND Periodicity = "daily"', (current_user_id,))
        results = cursor.fetchall()
        print("Your current daily tracked habits:")
    elif choice == "2":
        cursor.execute('SELECT Habit_name FROM Habits WHERE User_id = ? AND Periodicity = "weekly"', (current_user_id,))
        results = cursor.fetchall()
        print("Your current weekly tracked habits:")
    elif choice == "3":
        cursor.execute('SELECT Habit_name FROM Habits WHERE User_id = ?', (current_user_id,))
        results = cursor.fetchall()
        print("Your current tracked habits:")
    else:
        print("Invalid choice. Please try again.")
        return
    
    if not results:
        print("No habits found.")
    else:
        for i, habit in enumerate(results, start=1):
            print(f"{i}. {habit[0]}")
    
    conn.close()

def longest_run_streak_of_all_defined_habits(current_user_id):    
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT Habit_name, Longest_strike FROM Habits WHERE User_id = ?', (current_user_id,))
    
    results = cursor.fetchall()
    
    if not results:
        print("No habits found.")
    else:
        max_streak = 0
        max_streak_habit = ""
        
        for habit in results:
            if habit[1] > max_streak:
                max_streak = habit[1]
                max_streak_habit = habit[0]
        
        print(f"The longest run streak of all defined habits is {max_streak} for the habit '{max_streak_habit}'")
    
    conn.close()

def longest_run_streak_of_chosen_habit(current_user_id):  
    conn = sqlite3.connect('Habbit_app.db')
    cursor = conn.cursor()
    
    print("Choose a habit to see its longest run streak:")
    cursor.execute('SELECT Habit_name FROM Habits WHERE User_id = ?', (current_user_id,))
    
    results = cursor.fetchall()
    
    if not results:
        print("No habits found.")
    else:
        for i, habit in enumerate(results, start=1):
            print(f"{i}. {habit[0]}")
        
        choice = input("Enter the number of the habit: ")
        
        if choice.isdigit() and 1 <= int(choice) <= len(results):
            chosen_habit = results[int(choice) - 1][0]
            cursor.execute('SELECT Longest_strike FROM Habits WHERE User_id = ? AND Habit_name = ?', (current_user_id, chosen_habit))
            
            longest_strike = cursor.fetchone()[0]
            print(f"The longest run streak of '{chosen_habit}' is {longest_strike}.")
        else:
            print("Invalid choice. Please try again.")
    
    conn.close()