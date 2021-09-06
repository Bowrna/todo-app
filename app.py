from models import Schema
from service import ToDoService
from flask import Flask, request, jsonify

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

if __name__ == "__main__":
    Schema()
    app.run(debug=True)
