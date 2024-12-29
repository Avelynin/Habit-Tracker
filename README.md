
<a id="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src=https://github.com/user-attachments/assets/325d32d8-fae5-4eea-a328-8e7fe109ce76 alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Habit Tracker App</h3>
</div>




<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#testing-and-usage">Testing and Usage</a></li>
      <ul>
        <li><a href="#user-menagment">User Menagment</a></li>
        <li><a href="#habit-menagment">Habit Menagment</a></li>
        <li><a href="#analysis-module">Analysis Module</a></li>
      </ul>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

The Habit Tracker App is a Python-based application designed to help users develop and maintain productive habits. <br> This app includes functionality for creating, managing, and analyzing habits. Sample data from 2nd-29th December 2024, is provided for testing purposes.<br> This README guides you through the installation, usage, and testing of the app.<br>

### Built With

**Programming Language:**  
&nbsp;&nbsp;&nbsp;&nbsp;- Python  

**Frameworks:**  
&nbsp;&nbsp;&nbsp;&nbsp;- SQLite  

**Libraries:**  
&nbsp;&nbsp;&nbsp;&nbsp;- datetime  
&nbsp;&nbsp;&nbsp;&nbsp;- sqlite3  

**Development Environment:**  
&nbsp;&nbsp;&nbsp;&nbsp;- **Version Control:** GitHub  
&nbsp;&nbsp;&nbsp;&nbsp;- **IDE:** Jupyter Notebook  

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

-Python 3.13 or higher<br>
-SQLite (pre-installed with Python)<br>
-A console or terminal for running the app<br>

### Installation
This instalation script will be showing instalation base on included sample database.
If You want to create Your own habit to tracke them the best way is to create a new user.

1. Save all of the files from the repository to your hard drive.
2. Install Python 3.13 if you haven’t installed it yet:
   ```sh
   https://www.python.org/downloads/
   ```
3. Navigate via the Python console to the folder with the saved program. For example, it could be:
   ```sh
   cd C:\Habit app
   ```
4. Run the program via the console:
   ```js
   Python main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Testing and Usage

**For testing purposes, the "Krzysztof" account should be used as it already contains 4 weeks of data.**<br>
These are current values for Krzysztof account.<br><br>
![image](https://github.com/user-attachments/assets/f50cd7ae-4dad-4bf0-862e-51add28396c8)<br><br>
**IMPORTANT** After login, the current streak will be set to 0 as the database is updated after login, and the last habit was checked in on 29.12.2024.

### User menagment

#### Create New User
1. Choose option 2 in start menu<br>
  ![image](https://github.com/user-attachments/assets/67d92fb0-edba-4454-8164-7995c9dc65c4)

2. Choose number of new user name and confirm<br>
   ![image](https://github.com/user-attachments/assets/e838c93d-6b6a-4002-bef2-bbc92d6aec29)

#### Delete Existing User
1. Choose option 3 in start menu<br>
  ![image](https://github.com/user-attachments/assets/67d92fb0-edba-4454-8164-7995c9dc65c4)
2. Enter the username you want to delete:<br>
![image](https://github.com/user-attachments/assets/e455ce5e-b086-4722-add9-30d5fd844962)
2. Confirm it by typing "yes"<br>
![image](https://github.com/user-attachments/assets/41171ffd-402b-472d-a475-d80b3a5a0fa2)

#### Choose User(log in)
1. Choose option 1 in start menu<br>
  ![image](https://github.com/user-attachments/assets/67d92fb0-edba-4454-8164-7995c9dc65c4)
2. Choose number of new user name and confirm<br>
![image](https://github.com/user-attachments/assets/56696b97-b4fc-46f9-b853-f703d045b2a3)
3. After login, you will reach the main menu of the application.<br>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Habit Menagment

#### Add Habit
1. Choose option 1 in main menu<br>
![image](https://github.com/user-attachments/assets/77cc5271-cf08-4fa3-903e-3f0e7d84d77a)
2. Choose option 1 in habit menu<br>
![image](https://github.com/user-attachments/assets/a81cfcbc-5a42-45b6-8c5b-204224b856c2)
3. Choose name for new habit.<br>
   **It cannot be the same as an already created habit!**<br>
 ![image](https://github.com/user-attachments/assets/65153af6-a10a-4413-99ad-4affddfdc974)
4. Choose periodicity for Your habit.<br>
  ![image](https://github.com/user-attachments/assets/ab44a102-6ff7-448a-aaed-827a79ed457a)
4. Choose goal for Your habit.<br>
![image](https://github.com/user-attachments/assets/478cd5d2-0584-46e2-be4b-ad2d4c9fc06b)

#### Delete Habit
1. Choose option 1 in main menu<br>
![image](https://github.com/user-attachments/assets/77cc5271-cf08-4fa3-903e-3f0e7d84d77a)
2. Choose option 2 in habit menu<br>
![image](https://github.com/user-attachments/assets/a81cfcbc-5a42-45b6-8c5b-204224b856c2)
3. Enter the name of the habit you want to delete<br>
![image](https://github.com/user-attachments/assets/86a77160-d49d-49d2-b083-b39953cf0601)
4. Confirm<br>
![image](https://github.com/user-attachments/assets/4b42d399-5d8d-410e-968a-fea672caa923)
   
#### Habit Check-Off
1. Choose option 2 in main menu<br>
![image](https://github.com/user-attachments/assets/77cc5271-cf08-4fa3-903e-3f0e7d84d77a)
2. Choose option 1 in Check-off habit menu<br>
![image](https://github.com/user-attachments/assets/009bc4ea-0de8-45ba-a0af-e941a560ff4f)
3. Choose the number of the habit to check off<br>
![image](https://github.com/user-attachments/assets/d656e891-72f1-41a2-bad7-634b07f560aa)

#### Habit Progress Check
1. Choose option 2 in main menu<br>
![image](https://github.com/user-attachments/assets/77cc5271-cf08-4fa3-903e-3f0e7d84d77a)
2. Choose option 2 in the Check-off habit menu<br>
![image](https://github.com/user-attachments/assets/009bc4ea-0de8-45ba-a0af-e941a560ff4f)
3. Results will be displayed<br>
![image](https://github.com/user-attachments/assets/47235a70-4391-43ec-895d-535a2aa6f4d9)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Analysis Module

#### List of Tracked Habits
1. Choose option 3 in main menu<br>
![image](https://github.com/user-attachments/assets/77cc5271-cf08-4fa3-903e-3f0e7d84d77a)
2. Choose option 1 in analysis module<br>
![image](https://github.com/user-attachments/assets/c7d154a8-4243-4410-80c6-5b11dc8eb7f3)
3. Results will be displayed<br>
![image](https://github.com/user-attachments/assets/8122bc55-ad71-42e9-ae00-e36de092e99c)

#### List of Tracked Habits for Choosen Periodicity
1. Choose option 3 in main menu<br>
![image](https://github.com/user-attachments/assets/77cc5271-cf08-4fa3-903e-3f0e7d84d77a)
2. Choose option 2 in analysis module<br>
![image](https://github.com/user-attachments/assets/c7d154a8-4243-4410-80c6-5b11dc8eb7f3)
2. Choose number for periodicity<br>
![image](https://github.com/user-attachments/assets/2b23ebbf-dac1-4d71-91f4-3f4d479560f8)
4. Results will be displayed<br>
![image](https://github.com/user-attachments/assets/e2681953-f9bd-419d-a8a7-515522892867)

#### Longest Run Streak for All Habits
1. Choose option 3 in main menu<br>
![image](https://github.com/user-attachments/assets/77cc5271-cf08-4fa3-903e-3f0e7d84d77a)
2. Choose option 3 in analysis module<br>
![image](https://github.com/user-attachments/assets/c7d154a8-4243-4410-80c6-5b11dc8eb7f3)
3. Results will be displayed<br>
![image](https://github.com/user-attachments/assets/241ea4d5-066b-4671-9d24-d09726edfa67)

#### Longest Run Streak for All Habits
1. Choose option 3 in main menu<br>
![image](https://github.com/user-attachments/assets/77cc5271-cf08-4fa3-903e-3f0e7d84d77a)
2. Choose option 4 in analysis module<br>
![image](https://github.com/user-attachments/assets/c7d154a8-4243-4410-80c6-5b11dc8eb7f3)
3. Choose number for habit <br>
![image](https://github.com/user-attachments/assets/6d286452-9572-4440-8bb3-4e002339882c)
4.Results will be displayed<br>
![image](https://github.com/user-attachments/assets/63850313-7a58-40c8-86b7-ff75ba15fd08)



<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Krzysztof Grodzki - krzysztof.grodzki@hotmail.com

Project Link: https://github.com/Avelynin/Habit-Tracker/

<p align="right">(<a href="#readme-top">back to top</a>)</p>

