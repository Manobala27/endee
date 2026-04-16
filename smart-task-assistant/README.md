![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)
![AI](https://img.shields.io/badge/Type-Agentic%20AI-orange)



# Agentic AI: Weekly Planner Assistant

A comprehensive task management system with day-based planning, conversational intelligence, and a modern tabbed dashboard.

## 📅 Weekly Planning Features

- **Day-Specific Schedules**: Plan your entire week by assigning tasks to specific days (Monday through Sunday).
- **Sunday Special Logic**: Sunday tasks automatically prioritize relaxation, defaulting to 'Personal' type and lower priority.
- **Dynamic Suggestions**: The agent knows the current day and suggests tasks from your schedule accordingly.
- **Workflow Management**: Track tasks through their lifecycle: **Unlisted** -> **Pending** -> **Completed**.
- **Tabbed Dashboard**:
  - **📅 Weekly Plan**: A bird's eye view of your week, grouped by day.
  - **⏳ Pending Tasks**: A focused list of everything you need to do.
  - **✅ Completed Tasks**: A record of your productivity.

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Launch the Assistant**:
   ```bash
   python app.py
   ```
3. **Open the Dashboard**: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 💬 Command Examples

- **Planning**: `"add task Study AI on Monday"`, `"remind me to go gym on Sunday"`
- **Review**: `"show weekly plan"`, `"show tasks for Tuesday"`, `"show completed tasks"`
- **Interaction**: `"What should I do today?"`, `"Hi there!"`
- **Management**: `"complete task study"`, `"delete task gym"`

## 🎨 Design Aesthetics

- **Glassmorphism UI**: A premium dark-mode interface with translucent panels and vibrant accents.
- **Interactive Tabs**: Smooth transitions between different views of your productivity.
- **Proactive Agent**: An assistant that understands context and helps you stay on track.
