from models import Schema
from service import ToDoService
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

@app.route("/")
def hello():    
    print("Hello World")
    return "Hello World"

@app.route("/<name>")
def hello_name(name):
    return "Hello "+ name

@app.route("/todo", methods=["GET"])
def list_todo():
    return jsonify(ToDoService().list())

@app.route("/todo", methods=["POST"])
def create_todo():
    return jsonify(ToDoService().create(request.get_json()))

@app.route("/todo/<todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    return jsonify(ToDoService().delete(todo_id))

@app.route("/todo/<todo_id>", methods=["PUT"])
def update_todo(todo_id):
    return jsonify(ToDoService().update(todo_id, request.get_json()))

@app.route("/todo/<todo_id>", methods=["GET"])
def get_todo(todo_id):
    return jsonify(ToDoService().get(todo_id))

if __name__ == "__main__":
    Schema()
    app.run(debug=True)
