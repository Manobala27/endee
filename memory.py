import json
import os
from datetime import datetime

MEMORY_FILE = os.path.join("data", "memory.json")

def load_memory():
    """Load tasks from the JSON file."""
    if not os.path.exists(MEMORY_FILE):
        return {"tasks": []}
    
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            tasks = data if isinstance(data, list) else data.get("tasks", [])
            # Fix schema for migration
            now_day = datetime.now().strftime("%A")
            for task in tasks:
                if "priority" not in task: task["priority"] = "medium"
                if "status" not in task: task["status"] = "pending"
                if "reminder_time" not in task: task["reminder_time"] = None
                if "day" not in task: task["day"] = now_day
            return {"tasks": tasks}
    except (json.JSONDecodeError, IOError):
        return {"tasks": []}

def save_memory(memory_data):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory_data, f, indent=4)
        return True
    except IOError as e:
        print(f"Error saving memory: {e}")
        return False

def add_task(task_text, task_type, priority="medium", day=None, reminder_time=None):
    memory_data = load_memory()
    tasks = memory_data.get("tasks", [])
    
    if not day:
        day = datetime.now().strftime("%A")
        
    # Check for duplicates on the same day
    for task in tasks:
        if task["text"].lower() == task_text.lower() and task["day"] == day and task["status"] == "pending":
            return False, f"This task is already in your {day} plan."
    
    new_task = {
        "text": task_text,
        "day": day,
        "type": task_type,
        "priority": priority,
        "status": "pending",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reminder_time": reminder_time.strftime("%Y-%m-%d %H:%M:%S") if reminder_time else None
    }
    
    tasks.append(new_task)
    memory_data["tasks"] = tasks
    if save_memory(memory_data):
        return True, "Task added successfully."
    return False, "Failed to save task."

def mark_complete(task_text):
    memory_data = load_memory()
    tasks = memory_data.get("tasks", [])
    
    # Try exact match first, then fuzzy match for pending
    found = False
    for task in tasks:
        if task["text"].lower() == task_text.lower() and task["status"] == "pending":
            task["status"] = "completed"
            found = True
            break
            
    if not found:
        # Check if task text is contained in any task description
        for task in tasks:
            if task_text.lower() in task["text"].lower() and task["status"] == "pending":
                task["status"] = "completed"
                found = True
                task_text = task["text"] # update for message
                break

    if found:
        save_memory(memory_data)
        return True, f"Great job! Task '{task_text}' is now completed."
    return False, f"I couldn't find a pending task named '{task_text}'."

def delete_task(task_text):
    memory_data = load_memory()
    initial_count = len(memory_data["tasks"])
    memory_data["tasks"] = [t for t in memory_data["tasks"] if t["text"].lower() != task_text.lower()]
    
    if len(memory_data["tasks"]) < initial_count:
        save_memory(memory_data)
        return True, f"Deleted '{task_text}'."
    return False, "Task not found."

def get_analytics():
    """Calculate task statistics."""
    data = load_memory()
    tasks = data.get("tasks", [])
    total = len(tasks)
    if total == 0:
        return {"total": 0, "completed": 0, "pending": 0, "percentage": 0}
        
    completed = len([t for t in tasks if t["status"] == "completed"])
    pending = total - completed
    percentage = round((completed / total) * 100)
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "percentage": percentage
    }

def clear_memory():
    return save_memory({"tasks": []}), "All tasks cleared."
