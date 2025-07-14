from flask import Flask, jsonify, abort, request

app = Flask(__name__)
tasks = []
task_id_counter = 1

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        abort(404)
    return jsonify(task), 200

@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_counter
    data = request.json
    if not data or "title" not in data:
        abort(400)
    task_id = task_id_counter
    task_title = data.get("title")
    task_description = data.get("description", "")
    task_completed = data.get("completed", False)
    task = {
        "id": task_id,
        "title": task_title,
        "description": task_description,
        "completed": task_completed
    }
    tasks.append(task)
    task_id_counter += 1
    return jsonify(tasks), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    if not data or "title" not in data:
        abort(400)
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        abort(404)
    task["title"] = data.get("title", task["title"])
    task["description"] = data.get("description", task["description"])
    task["completed"] = data.get("completed", task["completed"])
    return jsonify(task), 200

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        abort(404)
    tasks.remove(task)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
