import memory
import utils
import random
import re
from datetime import datetime

def classify_task(task_text, day=None):
    text = task_text.lower()
    # Sunday Special Logic
    if day == "Sunday":
        return "personal"
    
    if any(k in text for k in ["study", "read", "learn", "exam", "course"]): return "study"
    if any(k in text for k in ["work", "assignment", "project", "meeting", "report"]): return "work"
    return "personal"

def classify_priority(task_text, day=None):
    # Sunday Special Logic: Default to low unless specified
    text = task_text.lower()
    if day == "Sunday" and not any(k in text for k in ["urgent", "must", "!"]):
        return "low"
    
    if any(k in text for k in ["urgent", "important", "asap", "deadline", "!", "must"]): return "high"
    if any(k in text for k in ["maybe", "later", "whenever"]): return "low"
    return "medium"

def agent_response(user_input):
    text = user_input.lower().strip()
    now_day = datetime.now().strftime("%A")
    
    # 1. Greetings & Current Context
    if any(text == g for g in ["hi", "hello", "hey"]):
        greetings = [
            f"Hello! Happy {now_day}! 🚀",
            f"Hey there! Ready to crush some goals this {now_day}?",
            f"Hi! It's {now_day}. How can I help you stay organized?",
            "Greetings! I'm here to manage your schedule."
        ]
        resp = random.choice(greetings) + " "
        
        data = memory.load_memory()
        today_tasks = [t for t in data["tasks"] if t["day"] == now_day and t["status"] == "pending"]
        if today_tasks:
            resp += f"You have {len(today_tasks)} tasks planned for today, including '{today_tasks[0]['text']}'."
        else:
            resp += "You have no tasks for today yet."
        return resp

    # 2. Show Weekly Plan
    if "weekly plan" in text or "show weekly" in text:
        data = memory.load_memory()
        tasks = [t for t in data["tasks"] if t["status"] == "pending"]
        if not tasks: return "Your weekly planner is empty!"
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        resp = "📅 **Weekly Plan:**\n"
        for day in days:
            day_tasks = [t for t in tasks if t["day"] == day]
            if day_tasks:
                resp += f"\n**{day}**:\n"
                for t in day_tasks:
                    resp += f" - {t['text']} ({t['priority']})\n"
        return resp.strip()

    # 3. Add Task on [Day]
    if text.startswith("add task") or text.startswith("remind me to"):
        prefix = "add task" if text.startswith("add task") else "remind me to"
        raw_content = user_input[len(prefix):].strip()
        
        if not raw_content: return "What task would you like to plan?"
            
        target_day = utils.extract_day(raw_content) or now_day
        rem_time = utils.extract_time(raw_content)
        cleaned_text = utils.clean_task_text(raw_content)
        
        category = classify_task(cleaned_text, target_day)
        priority = classify_priority(raw_content, target_day)
        
        success, msg = memory.add_task(cleaned_text, category, priority, target_day, rem_time)
        if success:
            note = f" I'll remind you at {rem_time.strftime('%H:%M')}." if rem_time else ""
            return f"Planned for {target_day}: '{cleaned_text}' ({category}, {priority}).{note}"
        return msg

    # 4. Show Tasks for [Day]
    for d in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        if f"tasks for {d}" in text:
            day_name = d.capitalize()
            data = memory.load_memory()
            tasks = [t for t in data["tasks"] if t["day"] == day_name and t["status"] == "pending"]
            if not tasks: return f"You have no tasks for {day_name}."
            resp = f"Tasks for {day_name}:\n"
            for t in tasks: resp += f"- {t['text']} ({t['priority']})\n"
            return resp.strip()

    # 5. Pending & Completed Views
    if "pending tasks" in text:
        data = memory.load_memory()
        tasks = [t for t in data["tasks"] if t["status"] == "pending"]
        if not tasks: return "You have no pending tasks. Great job!"
        resp = "⏳ **Pending Tasks:**\n"
        for t in tasks: resp += f"- {t['text']} ({t['day']})\n"
        return resp.strip()

    if "completed tasks" in text:
        data = memory.load_memory()
        tasks = [t for t in data["tasks"] if t["status"] == "completed"]
        if not tasks: return "You haven't completed any tasks yet!"
        resp = "✅ **Completed Tasks:**\n"
        for t in tasks: resp += f"- {t['text']} (on {t['day']})\n"
        return resp.strip()

    # 6. Complete & Delete
    if text.startswith("complete"):
        task_name = re.sub(r"^complete\s+(task\s+)?", "", text)
        return memory.mark_complete(task_name)[1]

    if text.startswith("delete"):
        task_name = re.sub(r"^delete\s+(task\s+)?", "", text)
        return memory.delete_task(task_name)[1]

    # 7. Suggestions (Today-Centric)
    if "what should i do" in text:
        data = memory.load_memory()
        today_tasks = [t for t in data["tasks"] if t["day"] == now_day and t["status"] == "pending"]
        if today_tasks:
            today_tasks.sort(key=lambda x: (0 if x['priority'] == 'high' else (1 if x['priority'] == 'medium' else 2)))
            return f"Since it's {now_day}, I suggest doing this: '{today_tasks[0]['text']}'."
        
        other_tasks = [t for t in data["tasks"] if t["status"] == "pending"]
        if other_tasks:
            return f"No tasks for today, but you have '{other_tasks[0]['text']}' coming up on {other_tasks[0]['day']}."
        
        return "You have no tasks planned. Why not enjoy the moment?"

    if "tired" in text or "stressed" in text:
        empathy = [
            "I'm sorry to hear that. Take a break! Your schedule is flexible. ☕",
            "Remember to breathe. Should I push your tasks to tomorrow?",
            "Rest is also productive. Why not step away for 15 minutes?",
            "You've been working hard. Maybe a short walk would help?"
        ]
        return random.choice(empathy)

    return "I can help with your weekly plan. Try 'add task Study on Monday' or 'show weekly plan'."
