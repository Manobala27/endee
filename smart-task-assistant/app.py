from flask import Flask, render_template, request, jsonify
import agent
import memory
from reminder import reminder_manager

app = Flask(__name__)

# Start the background reminder thread
reminder_manager.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"response": "I didn't catch that."})
    
    response = agent.agent_response(user_input)
    return jsonify({
        "response": response,
        "tasks": memory.load_memory().get("tasks", [])
    })

@app.route("/tasks")
def get_tasks():
    return jsonify(memory.load_memory())

@app.route("/complete", methods=["POST"])
def complete():
    task_text = request.json.get("task", "")
    success, msg = memory.mark_complete(task_text)
    return jsonify({
        "success": success, 
        "message": msg,
        "tasks": memory.load_memory().get("tasks", [])
    })

@app.route("/reminders")
def get_reminders():
    """Endpoint for the UI to poll for new reminder notifications."""
    notifications = reminder_manager.get_notifications()
    return jsonify({"notifications": notifications})

@app.route("/analytics")
def get_analytics():
    """Endpoint for task statistics."""
    return jsonify(memory.get_analytics())

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False) # use_reloader=False to avoid double thread start
