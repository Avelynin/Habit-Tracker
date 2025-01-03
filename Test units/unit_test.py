import unittest
from unittest.mock import patch
import sqlite3
from io import StringIO
import sys
from habit_management import add_habit, delete_habit
from analysis import (list_of_tracked_habits, 
                      list_of_habits_with_the_same_periodicity, 
                      longest_run_streak_of_all_defined_habits, 
                      longest_run_streak_of_chosen_habit)

class TestHabitApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # test database
        cls.conn = sqlite3.connect(':memory:')  # Use in-memory database for testing
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute('''
            CREATE TABLE Habits (
                Habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                User_id INTEGER,
                Habit_name TEXT UNIQUE,
                Periodicity TEXT,
                Goal INTEGER,
                Creation_date TEXT,
                Current_strike INTEGER,
                Longest_strike INTEGER
            )
        ''')
        cls.cursor.execute('''
            CREATE TABLE Habit_Completion (
                Completion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Habit_id INTEGER,
                Completion_date TEXT,
                Completion_time TEXT
            )
        ''')
        cls.cursor.execute('''
            CREATE TABLE Users (
                User_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT UNIQUE,
                Password TEXT
            )
        ''')
        cls.conn.commit()
        cls.current_user_id = 1  # Simulate a user ID

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        # Reset the database state before each test
        self.cursor.execute('DELETE FROM Habits')
        self.conn.commit()

    def test_add_habit(self): # test for add habit function
        print("1.Test: Add habit")   
        habit_name = "New Exercise"
        periodicity = "daily"
        goal = 1
        add_habit(self.current_user_id, habit_name, periodicity, goal, self.conn)
        
        self.cursor.execute('SELECT * FROM Habits WHERE Habit_name = ?', (habit_name,))
        habit = self.cursor.fetchone()

        self.assertIsNotNone(habit)
        self.assertEqual(habit[2], habit_name)
        self.assertEqual(habit[3], periodicity)
        self.assertEqual(habit[4], goal)
        print(f"Adding habit: {habit_name}, Periodicity: {periodicity}, Goal: {goal}, User ID: {self.current_user_id}")
        print("Test: Add habit successful!\n")
        
    def test_delete_habit(self): # test for delete habit function
        print("2.Test: Delete habit")
        habit_name = "New Exercise"
        periodicity = "daily"
        goal = 1
        delete_habit(self.current_user_id, habit_name, self.conn)

        self.cursor.execute('SELECT * FROM Habits WHERE Habit_name = ?', (habit_name,))
        habit = self.cursor.fetchone()
        self.assertIsNone(habit)  # Habit should be deleted
        print(f"Deleting habit: {habit_name}, Periodicity: {periodicity}, Goal: {goal}, User ID: {self.current_user_id}")
        print("Test: Delete habit successful!\n")

    def test_list_of_tracked_habits(self): # test for List of tracked habits function
        print("4.Test: List of tracked habits")
        self.cursor.execute('INSERT INTO Habits (User_id, Habit_name, Periodicity, Goal, Creation_date, Current_strike, Longest_strike) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (self.current_user_id, 'Exercise', 'daily', 5, '2023-01-01', 0, 10))
        self.cursor.execute('INSERT INTO Habits (User_id, Habit_name, Periodicity, Goal, Creation_date, Current_strike, Longest_strike) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (self.current_user_id, 'Read', 'weekly', 3, '2023-01-01', 0, 5))
        self.conn.commit()

        self.cursor.execute('SELECT * FROM Habits WHERE User_id = ?', (self.current_user_id,))

        output = StringIO()
        sys.stdout = output
        
        list_of_tracked_habits(self.current_user_id, self.conn)
        sys.stdout = sys.__stdout__
        print("List of tracked habits:", output.getvalue())

        self.assertIn("Your current tracked habits:", output.getvalue())
        self.assertIn("Exercise", output.getvalue())
        self.assertIn("Read", output.getvalue())
        print("Test: List of tracked habits successful\n")
        
    def test_list_of_habits_with_same_periodicity_weekly(self):  # test for List of habits with same periodicity function
        print("3.Test: List of habits with same periodicity (weekly)")
        self.cursor.execute('INSERT INTO Habits (User_id, Habit_name, Periodicity, Goal, Creation_date, Current_strike, Longest_strike) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (self.current_user_id, 'Exercise', 'daily', 5, '2023-01-01', 0, 10))
        self.cursor.execute('INSERT INTO Habits (User_id, Habit_name, Periodicity, Goal, Creation_date, Current_strike, Longest_strike) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (self.current_user_id, 'Read', 'weekly', 3, '2023-01-01', 0, 5))
        self.conn.commit()

        self.cursor.execute('SELECT * FROM Habits WHERE User_id = ?', (self.current_user_id,))

        output = StringIO()
        sys.stdout = output
        
        with patch('builtins.input', side_effect=['2']):
            list_of_habits_with_the_same_periodicity(self.current_user_id, self.conn)

        sys.stdout = sys.__stdout__

        print("List of habits with same periodicity weekly:", output.getvalue())  # Debugging line

        self.assertIn("Your current weekly tracked habits:", output.getvalue())
        self.assertIn("Read", output.getvalue())
        self.assertNotIn("Exercise", output.getvalue())
        print("Test: List of habits with same periodicity (weekly) successful\n")
        
    def test_longest_run_streak_of_all_defined_habits(self):  # test for Longest run streak of all defined habits function
        print("5.Test: Longest run streak of all defined habits") 
        self.cursor.execute('INSERT INTO Habits (User_id, Habit_name, Periodicity, Goal, Creation_date, Current_strike, Longest_strike) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (self.current_user_id, 'Exercise', 'daily', 5, '2023-01-01', 0, 10))
        self.cursor.execute('INSERT INTO Habits (User_id, Habit_name, Periodicity, Goal, Creation_date, Current_strike, Longest_strike) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (self.current_user_id, 'Read', 'weekly', 3, '2023-01-01', 0, 5))
        self.cursor.execute('INSERT INTO Habits (User_id, Habit_name, Periodicity, Goal, Creation_date, Current_strike, Longest_strike) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (self.current_user_id, 'Meditate', 'daily', 2, '2023-01-01', 0, 7))
        self.conn.commit()

        output = StringIO()
        sys.stdout = output
        
        longest_run_streak_of_all_defined_habits(self.current_user_id, self.conn)

        sys.stdout = sys.__stdout__

        captured_output = output.getvalue()
        print(captured_output)

        self.assertIn("The longest run streak of all defined habits is 10 for the habit 'Exercise'", captured_output)
        self.assertNotIn("No habits found.", captured_output)
        print("Test: Longest run streak of all defined habits successful\n")
    
    def test_longest_run_streak_of_chosen_habit(self): # test for Longest run streak of chosen habit function
        print("6.Test: Longest run streak of chosen habit")
        self.cursor.execute('INSERT INTO Habits (User_id, Habit_name, Periodicity, Goal, Creation_date, Current_strike, Longest_strike) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (self.current_user_id, 'Read', 'daily', 5, '2023-01-01', 0, 8))
        self.cursor.execute('INSERT INTO Habits (User_id, Habit_name, Periodicity, Goal, Creation_date, Current_strike, Longest_strike) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (self.current_user_id, 'Exercise', 'weekly', 3, '2023-01-01', 0, 5))
        self.conn.commit()

        output = StringIO()
        sys.stdout = output
        
        with patch('builtins.input', side_effect=['1']):
            longest_run_streak_of_chosen_habit(self.current_user_id, self.conn)

        sys.stdout = sys.__stdout__

        captured_output = output.getvalue()
        print(captured_output)

        self.assertIn("The longest run streak of 'Read' is 8.", captured_output)
        self.assertNotIn("No habits found.", captured_output)
        print("Test: Longest run streak of chosen habit\n")
if __name__ == '__main__':
    unittest.main()