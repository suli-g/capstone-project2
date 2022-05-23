'''Capstone template project for FCS Task 19 Compulsory task 1.
This template provides a skeleton code to start compulsory task 1 only.
Once you have successfully implemented compulsory task 1 it will be easier to
add a code for compulsory task 2 to complete this capstone'''

#=====importing libraries===========
import os
from datetime import datetime
from typing import List
#====Login Section====
# Declare file paths in the global scope so that they can be referred to more easily later.
# Use the path.join(__file__, file) pattern so that the program runs even if the working directory is different from the file directory.
user_txt = os.path.join(os.path.dirname(__file__), "user.txt")                      
tasks_txt = os.path.join(os.path.dirname(__file__), "tasks.txt")

# Keep logged_in, username in scope because we need them later.
logged_in: bool = False           
credentials: List[str] = []
username: str = ''
with open(user_txt, 'r') as userdata:      # Use the with-open pattern since userdata won't be necessary for the entire program and for all users.                        # We won't need the password later either.
    while not logged_in:
        while not username:
            user_attempt = input("username: ")
            for line in userdata:
                credentials = line.strip().split(', ')           # Remove the newline character before splitting.
                if user_attempt == credentials[0]:
                    username = user_attempt
                    break
            if user_attempt != credentials[0]:                                # Check that the user_attempt is incorrect after checking all lines in userdata.
                print(f"The user '{user_attempt}' does not exist.")
                
        if input("password: ") == credentials[1]:                             # Avoid storing the password in memory
            logged_in = True
            break
        else:
            print("Incorrect password entered")

# Define the templates on the top-level so the indents don't look weird later.
template = '''\
-------------------------------------------
Task:               {0}
Assigned to:        {1}
Date assigned:      {2}
Due date:           {3}
Task complete?      {4}
Task description:
 {5}
-------------------------------------------'''
stats_template = '''\
--------------------------
Statistics
  Users:{0}
  Tasks:{1}
--------------------------'''
while logged_in:
    # Only show the user what they are authorised to do
    menu_options = "Select one of the following Options below:\n"
    if username == 'admin':
        menu_options += (
            "r - Registering a user\n"
            + "s - Show statistics\n"
            )
    menu_options += ("a - Adding a task\n"
        + "va - View all tasks\n"
        + "vm - view my task\n"
        + "e - Exit\n"
        + ": ")
    # Presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    menu = input(menu_options).lower()

    if menu == 'r' and username == 'admin':
        # This option is used by 'admin' to register new users.
        # Any other user will not be given an indication that it exists.
        with open(user_txt, 'a') as userdata:
            new_user = input("username: ")
            password = input("password: ")
            if input("confirm password: ") != password:                 # Password confirmation doesn't need to be stored, just tested.
                print("'password' must match 'confirm password'", end = '\n\n')
            else:
                userdata.write('\n')                                    # Avoid adding an unnecessary newline to users.txt
                userdata.write(", ".join([new_user, password]))
                print(f"User {new_user} created successfully!")

    elif menu == 's' and username == 'admin':
        # This option is used by 'admin' user to show program  statistics (total amount of users, total amount of tasks given)
        # Any other user will not be given an indication that it exists.
        stats = (stats_template)
        
        with open(user_txt, 'r') as users, open(tasks_txt, 'r') as tasks:
            num_users = str(len(users.readlines()))
            num_tasks = str(len(tasks.readlines()))
            print(stats.format(num_users, num_tasks))

    elif menu == 'a' and username == 'admin':
        # This option is used by the 'admin' user to assign a task to a user
        assign_to = input("Assign task to (username): ")
        task = input(f"What should {assign_to} do? ")
        description = input(f"How should {assign_to} complete this task? ")
        print("By when should this task be completed? ")
        # Use the `datetime` module so that the date can be validated with minimal effort.
        due_year = int(input("year (YYYY): "))
        due_month = int(input("month: "))
        due_day = int(input("day of the month(dd): "))
        due_date = datetime(due_year, due_month, due_day)
        due_date = due_date.strftime("%d %b %Y")
        date_created = datetime.now().strftime("%d %b %Y")
        # Only open tasks.txt once all the variables have been set.
        with open(tasks_txt, 'a') as tasks:
            tasks.write(f"\n{assign_to}, {task}, {description}, {date_created}, {due_date}, No")
            print(f"Task created successfully (due: {due_date})")

    elif menu == 'va':
        # This option is used to view all tasks assigned to all users.
        with open(tasks_txt, 'r', encoding='utf8') as tasks:
            for line in tasks:
                current_task = template
                assigned_to, task, description, date_assigned, due_date, completed = line.split(', ')
                print(current_task.format(task, assigned_to, date_assigned, due_date, completed, description))

    elif menu == 'vm':
        # This option is used to display all tasks assigned to the current user.
        with open(tasks_txt, 'r') as tasks:
            for line in tasks:
                assigned_to, task, description, date_assigned, due_date, completed = line.split(', ')
                if assigned_to == username:     # Check that the current user and the assigned user are the same for each task
                    current_task = template
                    print(current_task.format(task, assigned_to, date_assigned, due_date, completed, description))

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
