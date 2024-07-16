from flask import Flask
from flaskwebgui import FlaskUI


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello"

@app.route("/test")
def hello2():
    return render_template('index.html')

if __name__ == "main":
    FlaskUI(app=app, server="flask", width=800, height=600).run()
