from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

tasks = []
BASE_URL = '/api/v1/'


@app.route('/')
def home():
    return 'Welcome to my To-Do List'

@app.route('/api/v1/tasks', methods=['POST'])
def create_task():
    if not request.json:
        abort(404, error='Missing body')
    print(request.json)
    objects=request.json.keys()
    if "name" in objects and "category" in objects and len(objects)<3:
        this_time = datetime.now()

        task = {
            'id': len(tasks)+1,
            'name': request.json['name'],
            'category': request.json['category'],
            'status': False,
            'created': this_time,
            'updated': this_time
        }
        tasks.append(task)
        return jsonify({'task': task}), 201
    else:
        return jsonify({'Response': "Error al mandar, solo se necesita name y category"}), 201

@app.route(BASE_URL + 'tasks', methods=['GET'])
def get_Tasks():
    return jsonify({'tasks': tasks}), 201

@app.route(BASE_URL + 'tasks/<int:id>', methods=['GET'])
def get_Task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404, error='id not found!')
    return jsonify({'task': this_task[0]})

@app.route(BASE_URL + 'tasks/<int:id>', methods=['PUT'])
def check_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404, error='ID not found!')

    this_task[0]['status'] = not this_task[0]['status']

    return jsonify({'task': this_task[0]})

@app.route(BASE_URL + 'tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404, error='ID not Found!')
    tasks.remove(this_task[0])
    return jsonify({'result': True})

if __name__== "__main__":
    app.run(debug=True)