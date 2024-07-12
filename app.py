#!/usr/bin/env python3

from flask import Flask, request, jsonify
from uuid import uuid4
from models.task import Task

app = Flask(__name__)

# CRUD: CREATE, READ, UPDATE, DELETE

tasks = []

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks_as_dict = list(map(lambda task: task.to_dict(), tasks))
    output = { "tasks": tasks_as_dict, "total_tasks": len(tasks) }
    return jsonify(output)

@app.route("/tasks/<uuid(strict=False):task_id>", methods=["GET"])
def get_task(task_id):
    task = next(filter(lambda task: task.id == task_id, tasks), None)
    
    if task: 
        return jsonify(task.to_dict())

    return jsonify({"message": "Task not found"}), 404

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    id = uuid4()
    title = data["title"]
    description = data["description"]
    completed = False
    task = Task(id, title, description, completed)
    tasks.append(task)
    return jsonify(task.to_dict()), 201

@app.route("/tasks/<uuid(strict=False):task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    task = next(filter(lambda task: task.id == task_id, tasks), None)

    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    task.title = data["title"]
    task.description = data["description"]
    task.completed = data["completed"]
    return jsonify(task.to_dict())

@app.route("/tasks/<uuid(strict=False):task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = next(filter(lambda task: task.id == task_id, tasks), None)
    if task:
        tasks.remove(task)
        return jsonify({"message": "Task deleted"})
    return jsonify({"message": "Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
