from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():    
    print("Hello World")
    return "Hello World"

@app.route("/<name>")
def hello_name(name):
    return "Hello "+ name

@app

if __name__ == "__main__":
    app.run(debug=True)