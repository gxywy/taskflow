from flask import Flask
from flask import render_template, request, jsonify, send_from_directory
from runner import TaskRunner, get_tasklists, delete_tasklist
import time

app = Flask(__name__)
runner = TaskRunner()
runner.load_tasks()

# global
@app.route('/')
def dashboard():
    return render_template('index.html', records=runner.task_queue)

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    return render_template('dashboard.html', records=runner.task_queue)

# for task
@app.route('/get_task', methods=['POST'])
def get_task():
    name, cmd, timeout = runner.get(request.form['index'])
    return {'name': name, 'cmd': cmd, 'timeout': timeout}

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

# for main
@app.route('/global_start', methods=['GET'])
def run():
    if not runner.is_running():
        runner.reset_status()
    runner.run()
    return 'start'

@app.route('/global_stop', methods=['GET'])
def stop():
    runner.stop()
    return 'stop'

@app.route('/backup', methods=['POST'])
def backup():
    if request.form['use_time'] == '0':
        filename = request.form['filename']
    else:
        filename = time.strftime("%Y%m%d-%H%M%S", time.localtime()) 
    runner.save_tasks(filename=filename + '.txt')
    return 'backup'

@app.route('/get_lists', methods=['GET'])
def get_lists():
    path, lists = get_tasklists()
    return dict(path=path, files=lists)

@app.route('/load_list', methods=['POST'])
def load_list():
    runner.load_tasks(filename=request.form['filename'])
    return 'load'

@app.route('/delete_list', methods=['POST'])
def delete_list():
    delete_tasklist(filename=request.form['filename'])
    return 'delete tasklist'

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory('tasklists', filename, as_attachment=True) 

if __name__ == '__main__':
    app.debug = False
    app.run()