import threading
import time
import pyttsx3
from datetime import datetime

# Initialize the text-to-speech engine
engine_lock = threading.Lock()  # Lock to ensure thread-safe access to pyttsx3

# Dictionary to store tasks
tasks = {}
tasks_lock = threading.Lock()  # Lock to ensure thread-safe access to tasks

# Function to announce tasks
def announce_task(task):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Set speech rate
    with engine_lock:  # Ensure thread-safe access to the engine
        for _ in range(3):  # Play the audio 3 times
            engine.say(f"It's time for {task}")
            engine.runAndWait()
            print(f"Announced: {task}")
    
    print("\nTask Scheduler Menu:")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Exit")
    print("Enter your choice: ", end="")
    

# Function to monitor and execute tasks
def task_monitor():
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        with tasks_lock:
            tasks_to_remove = []
            for task, task_time in tasks.items():
                if current_time == task_time:
                    print(f"\n[ALERT] It's time for task: {task}\n")
                    # Start a thread to announce the task
                    threading.Thread(target=announce_task, args=(task,), daemon=True).start()
                    tasks_to_remove.append(task)

            # Remove completed tasks
            for task in tasks_to_remove:
                del tasks[task]

        time.sleep(1)

# Function to add a new task
def add_task():
    task_name = input("Enter the task name: ")
    task_time = input("Enter the time (HH:MM:SS, 24-hour format): ")

    # Validate the time format
    try:
        time.strptime(task_time, "%H:%M:%S")
    except ValueError:
        print("[ERROR] Invalid time format! Please try again.")
        return

    with tasks_lock:
        tasks[task_name] = task_time
    print(f"[SUCCESS] Task '{task_name}' scheduled at {task_time}.")

# Function to list all tasks
def list_tasks():
    with tasks_lock:
        if not tasks:
            print("[INFO] No tasks scheduled.")
        else:
            print("\nScheduled Tasks:")
            for task, task_time in tasks.items():
                print(f"  - {task} at {task_time}")
            print()

# Main menu function
def main_menu():
    while True:
        print("\nTask Scheduler Menu:")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            print("Exiting Task Scheduler. Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice! Please try again.")

# Start the task monitor thread
monitor_thread = threading.Thread(target=task_monitor, daemon=True)
monitor_thread.start()

# Run the main menu
main_menu()
