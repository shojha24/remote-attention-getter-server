from flask import Flask, request, jsonify
import json
import firebase_admin
from firebase_admin import db, credentials
import datetime

cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://so-attention-getter-default-rtdb.firebaseio.com/"})

app = Flask(__name__)

ref = db.reference('/')

def increment_calls(current_value):
    return current_value + 1

@app.route('/teacher', methods=['GET'])
def teacher_call():
    data = request.get_json()
    group = data['group']
    mid = data['id']

    if data:
        try:
            
            curr_ref = db.reference(f'/{group}/{mid}/{datetime.datetime.now().strftime("%m-%d")}')

            if curr_ref.get() is None:
                curr_ref.set(1)
            else:
                curr_ref.transaction(increment_calls)

            return data
        except ValueError:
            return "Invalid number."
    return "Invalid number"

@app.route('/student', methods=['GET'])
def student_call():
    data = request.get_json()
    group = data['group']
    mid = data['id']

    if data:
        try:
            count = 0
            
            curr_ref = db.reference(f'/{group}/{mid}/{datetime.datetime.now().strftime("%m-%d")}')

            if curr_ref.get() is None:
                pass
            else:
                count = int(curr_ref.get())

            return str(count)
        except ValueError:
            return "Invalid number."
    return "Invalid number"

@app.route('/adv-get', methods=['GET'])
def advanced_get():
    data = request.get_json()
    group = data['group']
    mid = data['id']
    date = data['date']

    print(data)
    try:
        count = 0
        curr_ref = db.reference(f'/{group}/{mid}/{date}')

        if curr_ref.get() is None:
            pass
        else:
            count = int(curr_ref.get())

        return str(count)
    except ValueError:
        return "Invalid number."

@app.route('/adv-set', methods=['GET'])
def advanced_set():
    data = request.get_json()
    group = data['group']
    mid = data['id']
    date = data['date']

    print(data)
    try:
        curr_ref = db.reference(f'/{group}/{mid}/{date}')

        if curr_ref.get() is None:
            curr_ref.set(1)
        else:
            curr_ref.transaction(increment_calls)

        return data
    except ValueError:
        return "Invalid number."

@app.route('/student-set', methods=['GET'])
def student_set():
    data = request.get_json
    group = data['group']
    mid = data['id']
    name = data['name']

    print(data)
    try:
        curr_ref = db.reference(f'/{group}/{mid}/name')
        curr_ref.set(name)

        return data
    except ValueError:
        return "Invalid name"

@app.route('/student-get', methods=['GET'])
def student_get():
    data = request.get_json
    group = data['group']
    mid = data['id']

    print(data)
    try:
        curr_name = None
        curr_ref = db.reference(f'/{group}/{mid}/name')

        if curr_ref.get() is None:
            pass
        else:
            curr_name = curr_ref.get()

        return str(curr_name)
    except ValueError:
        return "Error!!"
    
if __name__ == '__main__':
    app.run(debug=True)