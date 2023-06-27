#•••••••••• TASK 17 CAPSTONE PROJECT REFACTOR PROGRAMME ••••••••••••••



# ******** IMPORTING LIBRARIES/MODULES *********
import csv
import os
from datetime import datetime, date

#••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.
#••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••

# Decalring Date and time string format
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Dictionary to store usernames and passwords
username_password = {}


'''Refactored Programme By Creating (9) functions.
The following 8 functions are called when User enters abbreviation
in main menu:'''

# (1) Function to load the usernames and passwords from the user.txt file
def load_users():
    
    # Check if the file exists
    if not os.path.exists("user.txt"):
        print("User file does not exist.")
        return

    # Generate and open file user.txt file
    with open("user.txt", "r") as user_file:
        reader = csv.reader(user_file, delimiter=";")
        for row in reader:
            # Extract the username and password from each row
            username = row[0]
            password = row[1]
            # Add the username and password to the username_password dictionary
            username_password[username] = password
    
   
# (2) Registering New User Function
def reg_user():
    """
    Allows a user to register by entering a new username and password.
    The function prompts the user for a new username, password, and confirmation,
    validates the inputs, and appends the username and password to the "user.txt" file.
    Returns True upon successful registration.
    """

    # loop used if user enter invalid inputs
    while True:
        #  Prompt the user for new username, password, and confirmation
        new_username = input("New Username: ")
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

        if new_username == "":
            print("Error!: User cannot be empty, try again")
            continue
        
        elif not new_password or not confirm_password:
            print("Error: Password fields cannot be empty")
            continue
        
        elif new_password == confirm_password:

            # Check if the username already exists in the user.txt file
            with open("user.txt", "r") as user_file:
                existing_users = user_file.read().splitlines()
                existing_usernames = [line.split(";")[0] for line in existing_users]
                
                if new_username in existing_usernames:
                    print("Error: Username already exists, please choose a different username")
                    continue

            # Open the user.txt file in append mode and write the new username and password
            with open("user.txt", "a") as user_file:
             user_file.write(f"\n{new_username};{new_password}")
            break
        
        else:
         print("Passwords do not match Please Try again")
        continue
    
    return True   

# (3) Adding Task Function
def add_task():
    """
    Allows the user to add a new task by entering the necessary details.
    The function prompts the user for the person to whom the task is assigned,
    the task title, description, and due date. It validates the inputs and
    appends the task details to the "tasks.txt" file. Returns True upon
    successful addition of the task.
    """

    # Read the user.txt file and update the username_password dictionary
    with open("user.txt", "r") as user_file:
        for line in user_file:
            username, password = line.strip().split(";")
            username_password[username] = password

    #loop to ensure user enters correct person to assing task to
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in [username for username in username_password.keys()]:
            print("User does not exist. Please enter a valid username")
            continue
        else:
            break

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    
    #exception handling to input correct date format
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT).date()
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Getting current date.
    curr_date = date.today()

    # Adding data to task.txt with 'No' to indicate task completion status
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "assigned_date": curr_date,
        "due_date": due_date_time,
        "completed": False
    }

    # Updating task to tasks.txt file
    task_list.append(new_task)
    with open("tasks.txt", "a") as task_file:
        task_str = (
        f"\n{task_username.strip()};{task_title.strip()};{task_description.strip()};"
        f"{curr_date.strftime(DATETIME_STRING_FORMAT)};{due_date_time.strftime(DATETIME_STRING_FORMAT)};No"
        )
        task_file.write(task_str)
    print("\n--------------------------")
    print("Task added successfully") 
    print("--------------------------\n")   
    return True

#(4) View All Tasks Function 
def view_all_tasks():
    '''Displays all the tasks in the task list along with their details.
    It iterates over each task in the task list and prints the task title,
    assigned username, assigned date, due date, task description, and completion status.
    '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: {t['description']}\n"
        disp_str += f"Completed: \t {'Yes' if t['completed'] else 'No'}\n"
        print("\n---------------------------------------------------------------")
        print(disp_str)
        print("---------------------------------------------------------------\n")


#(5) View My Tasks Function
def view_my_tasks(task_list, curr_user):
    """
    Displays the tasks assigned to the current user.
    It iterates over each task in the task list and prints the task details
    for the tasks assigned to the current user.
    It allows the user to select a task and perform actions like marking the task as complete or editing the task.
    """

    print("\nTasks assigned to you:\n")
    user_tasks = []

    # Iterate over each task in the task list
    for i, t in enumerate(task_list):
        # Check if the task is assigned to the current user
        if t['username'] == curr_user:
            user_tasks.append(t)
            complete_status = "Complete" if t['completed'] else "Incomplete"

            # Print the task details
            print("---------------------------------------------------------------------------------")
            disp_str = f"\nTask {len(user_tasks)}:\n" \
                       f"Title: \t\t {t['title']}\n" \
                       f"Assigned to: \t {t['username']}\n" \
                       f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n" \
                       f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n" \
                       f"Description: \t{t['description']}\n" \
                       f"Completed: \t {complete_status}\n"
            print(disp_str)
            print("---------------------------------------------------------------------------------")

    # If no tasks are assigned to the user, print a message and return
    if not user_tasks:
        print("No Tasks Assigned")
        return
    
    # Additional Menu Choice 
    # Loop to check if user enters valid task number within range
    while True:
        print("Select a task number to perform an action:")
        print("Enter '-1':To Return to the main menu")
       
        task_number = input("Task Number: ")

        if task_number == "-1":
            return
        
        if not task_number.isdigit():
            print("invalid input, please enter valid number")
            continue

        task_number = int(task_number)
        if task_number < 1 or task_number > len(user_tasks):
            print("Invalid Task Number, Please enter a task number within the range")
            continue

        selected_task = user_tasks[int(task_number) - 1]
        break

    # Determine the complete status based on the completion status of the selected task
    if selected_task['completed']:
        complete_status = "Complete"
    else:
        complete_status = "Incomplete"

    # Print the selected task details
    print(f"\nSelected Task: {task_number} \n")
    print("---------------------------------------------------------------------------------------")
    print(f"Title:\t\t\t {selected_task['title']}")
    print(f"Assigned to:\t\t {selected_task['username']}")
    print(f"Date Assigned:\t\t {selected_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
    print(f"Due Date:\t\t {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
    print(f"Description:\t\t{selected_task['description']}")
    print(f"Completed:\t\t {complete_status}")
    print("---------------------------------------------------------------------------------------\n")
    
    #loop used - if user enters wrong input to ensure programme flows smoothly.
    while True:
        action = input("Select an action (mark as complete/edit): ").lower()

        if action == "mark as complete":
            # Check if the task is already marked as complete
            if selected_task['completed']:
                print("\n-------------------------")
                print("Task is already marked as complete.")
                print("-------------------------\n")
                break
            
             # Mark the task as complete
            selected_task['completed'] = True
            print("\n-------------------------")
            print("Task marked as complete.")
            print("-------------------------\n")
            
            # Update the tasks.txt file to change completeion status 'NO' to 'YES'
            with open("tasks.txt", "r+") as tasks_file:
                lines = tasks_file.readlines()
                tasks_file.seek(0)

                for line in lines:
                    task_data = line.strip().split(';')
                    # Find the task in the file by matching username and title
                    if task_data[0] == selected_task['username'] and task_data[1] == selected_task['title']:
                        task_data[-1] = 'Yes'
                    tasks_file.write(';'.join(task_data) + '\n')

                tasks_file.truncate()
            break

        elif action == "edit":
            # Check if the task is marked as complete
            if selected_task['completed']:
                print("\nYou can only edit tasks that are not marked as complete.\n")
                break

            # Prompt the user for new username and due date    
            new_username = input("Enter the new username (or leave empty to keep the current one): ")
            new_due_date = input("Enter the new due date (or leave empty to keep the current one): ")

            # Update the username and due date if provided
            if new_username:
                selected_task['username'] = new_username
            if new_due_date:
                
                try:
                    # Validate the entered due date format
                    new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                    selected_task['due_date'] = new_due_date
                except ValueError:
                    print("Invalid due date format. Please enter a date in the format YYYY-MM-DD.")
                    continue
    
            print("Task updated.")
            break
        else:
            print("Invalid Action. Please select a valid action.")
            continue

#(6) Generate Reports Function (Additional admin feature)
def generate_report(task_list):
    ''' Records Full Report for the admin. Tracks the data by generating and updating the 
    user_overview.txt and task_overview.txt.
    '''

    # Counting the total number of registered users
    user_count = len(username_password)

    # Creating a dictionary to track the number of tasks assigned to each user
    assigned_tasks = {}
    
    for task in task_list:
        if task['username'] not in assigned_tasks:
            assigned_tasks[task['username']] = {'assigned': 0, 'completed': 0, 'overdue': 0}
        assigned_tasks[task['username']]['assigned'] += 1
        if task['completed']:
            assigned_tasks[task['username']]['completed'] += 1
        if not task['completed'] and task['due_date']:
            assigned_tasks[task['username']]['overdue'] += 1

    # Counting the total number of tasks
    total_tasks = len(task_list)

    # Counting the number of completed tasks
    completed_tasks = sum(1 for task in task_list if task['completed'])

    # Counting the number of uncompleted tasks
    incomplete_tasks = total_tasks - completed_tasks

    # Counting the number of tasks that are overdue and uncompleted
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'])

    # Generate and Writing the user overview to user_overview.txt file
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview\n")
        user_overview_file.write("----------------------------------------------------\n")
        user_overview_file.write(f"Total users registered: {user_count}\n")
        user_overview_file.write(f"Total tasks generated and tracked: {total_tasks}\n")
        user_overview_file.write("----------------------------------------------------\n")

        for username, task_counts in assigned_tasks.items():
            total_user_tasks = task_counts['assigned']
            completed_user_tasks = task_counts['completed']
            overdue_user_tasks = task_counts['overdue']
            incomplete_user_tasks = total_user_tasks - completed_user_tasks
            incomplete_user_percent = (incomplete_user_tasks / total_user_tasks) * 100
            completed_user_percent = (completed_user_tasks / total_user_tasks) * 100
            overdue_user_percent = (overdue_user_tasks / total_user_tasks) * 100

            user_overview_file.write(f"\nUser: {username}\n")
            user_overview_file.write(f"Total tasks assigned: {total_user_tasks}\n")
            user_overview_file.write(f"Percentage of total tasks assigned: {total_user_tasks / total_user_tasks * 100:.2f}%\n")
            user_overview_file.write(f"Percentage of completed tasks: {completed_user_percent:.2f}%\n")
            user_overview_file.write(f"Percentage of tasks to be completed: {incomplete_user_percent:.2f}%\n")
            user_overview_file.write(f"Percentage of overdue tasks: {overdue_user_percent:.2f}%\n")

    # Generate and Writing the task overview to task_overview.txt file
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Task Overview\n")
        task_overview_file.write(f"Total tasks generated and tracked: {total_tasks}\n")
        task_overview_file.write(f"Total completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Total uncompleted tasks: {incomplete_tasks}\n")
        task_overview_file.write(f"Total tasks overdue and uncompleted: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of incomplete tasks: {incomplete_tasks / total_tasks * 100:.2f}%\n")
        task_overview_file.write(f"Percentage of overdue tasks: {overdue_tasks / total_tasks * 100:.2f}%\n")

    # Printing a success message
    print("\n---------------------------------")
    print("Reports generated successfully.")
    print("---------------------------------\n")

#(7) Display Stats Function 
def display_stats():
    
    # Checking if the files exist, and generate if necessary
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as tasks_files:
            pass
    
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as user_files:
            pass
    
    # Reading the reports from files
    # Strip() to account for any whitespaces/empty lines to avoid errors.
    with open ("tasks.txt", "r") as tasks_files:
        tasks_data = [line.strip() for line in tasks_files if line.strip()]
    
    with open ("user.txt", "r") as user_files:
        user_data = [line.strip() for line in user_files if line.strip()]

    # Couting Number of Registered User from user.txt
    user_total = len(user_data)

    # Counting the number of tasks in the system
    total_tasks = len(tasks_data)
    completed_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0

    current_date = date.today()

    # Creating a dictionary to store user-specific task statistics
    user_stats = {}

    for tasks in tasks_data:
        ## Splitting each line using semicolon (;) as the delimiter
        task_parts = [part.strip() for part in tasks.split(";")]
        if len(task_parts) >= 6:
            status = task_parts[-1].lower()  # Extract the status field
            if status == "yes":
                completed_tasks += 1
            else:
                incomplete_tasks += 1
                # Checking for overdue tasks
                due_date = task_parts[-2]
                try:
                    due_date = datetime.strptime(due_date, DATETIME_STRING_FORMAT).date()
                    if due_date < current_date:
                        overdue_tasks += 1
                except ValueError:
                    # Handle incorrect date format gracefully
                    pass

            # Update the user-specific task statistics
            username = task_parts[0]
            if username in user_stats:
                user_stats[username]["total"] += 1
                user_stats[username]["completed"] += 1 if status == 'yes' else 0
                user_stats[username]["incomplete"] += 1 if status == 'no' else 0
                if status == 'no':
                    user_stats[username]["overdue"] += 1 if due_date < current_date else 0
            else:
                user_stats[username] = {
                    "total": 1,
                    "completed": 1 if status == "yes" else 0,
                    "incomplete": 1 if status == "no" else 0,
                    "overdue": 1 if status == "no" and due_date < current_date else 0
                }

    # Calculating percentages
    completed_percentage = (completed_tasks / total_tasks) * 100
    incomplete_percentage = (incomplete_tasks / total_tasks) * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100

    # Displaying statistics to the admin
    if curr_user == "admin":
        print("\nStatistiscs:\n")
        print("-------------------------------------")
        print(f"Total Number of Users: \t\t {user_total}")
        print(f"Total Number of Tasks: \t\t {total_tasks}")
        print("-------------------------------------")

        # Generating additional reports based on user_data and tasks_data
        print("\nTask Completion Statistics:\n")
        print("-----------------------------------")
        print(f"Completed Tasks:\t {completed_tasks} ({completed_percentage:.2f}%)")
        print(f"Incomplete Tasks:\t {incomplete_tasks} ({incomplete_percentage:.2f}%)")
        print(f"Overdue Tasks:\t\t {overdue_tasks} ({overdue_percentage:.2f}%)")
        print("-----------------------------------")

    # For Loop to Print user-specific task statistics 
        print("\nUser Task Statistics:\n")
        for username, stats in user_stats.items():
            total_tasks = stats["total"]
            completed_tasks = stats["completed"]
            incomplete_tasks = stats["incomplete"]
            overdue_tasks = stats["overdue"]
            
            # Caluclating user-specific percentages
            completed_percentage = (completed_tasks / total_tasks) * 100
            incomplete_percentage = (incomplete_tasks / total_tasks) * 100
            overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks != 0 else 0
            user_stats[username]['overdue_percentage'] = overdue_percentage

            print("---------------------------------------")
            print(f"User: {username}")
            print(f"Total tasks: {total_tasks}")
            print(f"Completed tasks: {completed_tasks} ({completed_percentage:.2f}%)")
            print(f"Incomplete tasks: {incomplete_tasks} ({incomplete_percentage:.2f}%)")
            print(f"Overdue tasks: {overdue_tasks} ({overdue_percentage:.2f}%)")
            print("---------------------------------------")

        print("\n.....................................")
        print("Displaying Statistics Completed 100%")
        print(".....................................")

#(8) Login Function 
def login():
    # Prompt the user for username and password
    global curr_user
    curr_user = input("Username: ")
    curr_password = input("Password: ")

    # Check if username or password is empty
    if not curr_user or not curr_password:
        print("Error: Username and password cannot be empty.")
        return False
    
    # Check if the entered username exists in the username_password dictionary
    if curr_user in username_password.keys():
        # Verify the entered password against the stored password for the username
        if username_password[curr_user] == curr_password:
            # Successful login
            return True
        else:
            # Invalid password
            print("Invalid username or password")
            print("ensure your username and password case sensitive")
    else:
        # Invalid username
        print("Invalid username or password.")
        print('Ensure your username and password case sensitive')
    return False


'''Main Function To run the main menu programme '''
def main():
    # Load user data from file (calling function #1)
    load_users()

    # Initialize login status
    logged_in = False

    # Perform login until successful
    while not logged_in:
        print("Login to continue")
        logged_in = login()

    # Initialize task list
    global task_list
    task_list = []

    # Load task data from file
    with open("tasks.txt", "r") as task_file:
        reader = csv.reader(task_file, delimiter=";")
        for row in reader:
            # Using any function to skip empty line in row, 
            # handling occasional index error.
            if any (row):
            # Extract task details from the file
            # Using strip to account for whitespaces
                task_username = row[0].strip()
                task_title = row[1].strip()
                task_description = row[2].strip()
                due_date_time = datetime.strptime(row[4].strip(), DATETIME_STRING_FORMAT)
                assigned_date = datetime.strptime(row[3].strip(), DATETIME_STRING_FORMAT)
                task_completed = True if row[5].strip().lower() == "yes" else False

            # Create task dictionary
            task = {
                "username": task_username,
                "title": task_title,
                "description": task_description,
                "due_date": due_date_time,
                "assigned_date": assigned_date,
                "completed": task_completed
            }

            # Add task to the task list
            task_list.append(task)

    # Main menu loop
    choice = ""
    while choice != "exit":
        print("\nPlease select one of the following options:\n")
        if curr_user == "admin":
            # Admin options
            print("r -  Register User")
            print("a -  Add Task")
            print("va - View All Tasks")
            print("vm - View My Tasks")
            print('gr - Generate Reports')
            print('ds - Display Statistics')
            
        else:
            # User options
            print("r -  Register User")
            print("a -  Add Task")
            print("va - View All Tasks")
            print("vm - View My Tasks")
            
        print("e -  Exit Program\n")    
                
        choice = input("Your selection: ").lower()
        if curr_user == "admin":
            # Admin choices - abbreviation calls functions
            if choice == "r":
                reg_user()
            elif choice == "a":
                add_task()
            elif choice == "va":
                view_all_tasks()
            elif choice == "vm":
                view_my_tasks(task_list, curr_user)
            elif choice == 'gr':
                generate_report(task_list)
            elif choice == 'ds':
                display_stats()
            elif choice == "e":
                break
        else:
            # User choices - abbreviation calls functions
            if choice == "r":
                reg_user()
            elif choice == "a":
                add_task()
            elif choice == "va":
                view_all_tasks()
            elif choice == "vm":
                view_my_tasks(task_list, curr_user)
            elif choice == "e":
                break
    
    print("Goodbye!")

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()


#•••••••••••••••••••• PROGRAMME END ••••••••••••••••••••••••••••