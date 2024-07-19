import sys

# TEMP SOL, FIX
BACKEND_FILE = "C:/Users/james/New folder/SupplyChain/Backend/ModelCreation"

sys.path.append(BACKEND_FILE)


from ModelClasses import Classes


from flask import Flask, render_template, request
from flaskwebgui import FlaskUI
import json
import os
import sys
import asyncio


app = Flask(__name__, static_folder="static", template_folder="templates")

MODELS_DATA_FILE = os.path.join(app.static_folder, '/ModelFiles')


SELECTED_MODEL_DIR = None

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/test")
def hello2():
    return render_template('base.html')

@app.route('/classes/data/all', methods=['GET'])
async def getAllClassData():
    
    data = json.loads(request.data)
    
    final_file =  await asyncio.gather()
    # Just make sure that the coroutine should not  having any blocking calls inside it. 
    return Response(
        mimetype='application/json',
        status=200
    )
if __name__ == "main":
    uiapp = FlaskUI(app=app, server="flask", width=100, height=2000)

    uiapp.run()
