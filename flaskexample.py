from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, Flask on Ubuntu 22.04! 🚀"

if __name__ == "__main__":
    app.run(debug=True)

