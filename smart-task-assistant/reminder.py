import time
import threading
import memory
from datetime import datetime

class ReminderManager:
    def __init__(self):
        self.notification_queue = []
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        """Start the background reminder thread."""
        if not self.thread.is_alive():
            self.thread.start()

    def _run(self):
        """Periodically check for reminders."""
        while not self.stop_event.is_set():
            try:
                self._check_reminders()
            except Exception as e:
                print(f"Reminder Thread Error: {e}")
            time.sleep(10) # Check every 10 seconds

    def _check_reminders(self):
        now = datetime.now()
        data = memory.load_memory()
        tasks = data.get("tasks", [])
        
        changed = False
        for task in tasks:
            # Only remind for pending tasks with a reminder time set
            if task["status"] == "pending" and task["reminder_time"]:
                rem_time = datetime.strptime(task["reminder_time"], "%Y-%m-%d %H:%M:%S")
                
                # If current time is past reminder time
                if now >= rem_time:
                    # Trigger notification
                    msg = f"🔔 Reminder: It's time to '{task['text']}'!"
                    if msg not in self.notification_queue:
                        self.notification_queue.append(msg)
                    
                    # Clear reminder so it doesn't fire again
                    task["reminder_time"] = None
                    changed = True
        
        if changed:
            memory.save_memory(data)

    def get_notifications(self):
        """Retrieve and clear current notifications."""
        notifications = list(self.notification_queue)
        self.notification_queue = []
        return notifications

# Single instance to be shared
reminder_manager = ReminderManager()
