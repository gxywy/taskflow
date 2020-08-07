from flask import Flask
from flask import render_template, request, jsonify
from runner import TaskRunner

app = Flask(__name__)
runner = TaskRunner()
runner.load_tasks()

@app.route('/')
def dashboard():
    return render_template('index.html', records=runner.task_queue)

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    return render_template('dashboard.html', records=runner.task_queue)

@app.route('/delete_task', methods=['POST'])
def delete():
    runner.delete(request.form['index'])
    return 'delete'

@app.route('/add_task', methods=['POST'])
def add():
    runner.add(request.form['name'], request.form['cmd'], request.form['timeout'])
    return 'add'

@app.route('/edit_task', methods=['POST'])
def edit():
    runner.edit(request.form['index'], request.form['name'], request.form['cmd'], request.form['timeout'])
    return 'edit'

@app.route('/get_log', methods=['POST'])
def get_log():
    return runner.get_log(request.form['index'])

@app.route('/global_start', methods=['GET'])
def run():
    runner.reset()
    runner.run()
    return 'start'

@app.route('/global_stop', methods=['GET'])
def stop():
    runner.stop()
    return 'stop'

if __name__ == '__main__':
    app.debug = False
    app.run()