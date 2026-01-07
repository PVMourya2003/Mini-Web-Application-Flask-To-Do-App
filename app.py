from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# In-memory task storage
tasks = []
task_id_counter = 1

# HTML template (kept simple and inline)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        li { margin: 8px 0; }
        .done { text-decoration: line-through; color: gray; }
        button { margin-left: 5px; }
    </style>
</head>
<body>
    <h1>Task Manager</h1>

    <form action="/add" method="post">
        <input type="text" name="title" placeholder="New task" required>
        <button type="submit">Add</button>
    </form>

    <ul>
        {% for task in tasks %}
        <li>
            <span class="{{ 'done' if task.completed else '' }}">
                {{ task.title }}
            </span>
            <a href="/toggle/{{ task.id }}">
                <button>✓</button>
            </a>
            <a href="/delete/{{ task.id }}">
                <button>🗑</button>
            </a>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    global task_id_counter
    title = request.form["title"]
    tasks.append({
        "id": task_id_counter,
        "title": title,
        "completed": False
    })
    task_id_counter += 1
    return redirect(url_for("index"))

@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
