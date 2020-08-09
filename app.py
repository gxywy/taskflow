from flask import Flask
from flask import render_template, request, redirect, url_for, send_from_directory, session
from runner import TaskRunner
from utils import *
import time, os

app = Flask(__name__)
runner = TaskRunner()
runner.load_tasks()

# global
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == get_password():
            session['username'] = username
            session['password'] = password
            return 'success'
        else:
            return 'incorrect'
    return render_template('login.html')

@app.route('/')
def dashboard():
    if 'username' not in session: return render_template('login.html')
    return render_template('index.html', records=runner.task_queue, status=runner.is_alldone)

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    if 'username' in session:
        return render_template('dashboard.html', records=runner.task_queue, status=runner.is_alldone)
    else:
        return '<div class="spinner-grow text-primary" role="status"><span class="sr-only">Loading...</span></div>'

# for task
@app.route('/get_task', methods=['POST'])
def get_task():
    if 'username' not in session: return render_template('login.html')
    name, cmd, timeout = runner.get(request.form['index'])
    return {'name': name, 'cmd': cmd, 'timeout': timeout}

@app.route('/delete_task', methods=['POST'])
def delete():
    if 'username' not in session: return render_template('login.html')
    index = int(request.form['index'])
    runner.delete(index)
    return 'delete'

@app.route('/order_up', methods=['POST'])
def order_up():
    if 'username' not in session: return render_template('login.html')
    runner.order_up(request.form['index'])
    return 'order_up'

@app.route('/order_down', methods=['POST'])
def order_down():
    if 'username' not in session: return render_template('login.html')
    runner.order_down(request.form['index'])
    return 'order_down'

@app.route('/add_task', methods=['POST'])
def add():
    if 'username' not in session: return render_template('login.html')
    runner.add(request.form['name'], request.form['cmd'], request.form['timeout'])
    return 'add'

@app.route('/edit_task', methods=['POST'])
def edit():
    if 'username' not in session: return render_template('login.html')
    runner.edit(request.form['index'], request.form['name'], request.form['cmd'], request.form['timeout'])
    return 'edit'

@app.route('/get_log', methods=['POST'])
def get_log():
    if 'username' not in session: return render_template('login.html')
    return runner.get_log(request.form['index']).decode('gbk', 'ignore')

# for main
@app.route('/global_start', methods=['GET'])
def run():
    if 'username' not in session: return render_template('login.html')
    if runner.is_alldone:
        runner.reset_status()
    runner.run()
    return 'start'

@app.route('/global_stop', methods=['GET'])
def stop():
    if 'username' not in session: return render_template('login.html')
    runner.stop()
    return 'stop'

@app.route('/backup', methods=['POST'])
def backup():
    if 'username' not in session: return render_template('login.html')
    if request.form['use_time'] == '0':
        filename = request.form['filename']
    else:
        filename = time.strftime("%Y%m%d-%H%M%S", time.localtime()) 
    runner.save_tasks(filename=filename + '.txt')
    return 'backup'

@app.route('/get_lists', methods=['GET'])
def get_lists():
    if 'username' not in session: return render_template('login.html')
    path, lists = get_tasklists()
    return dict(path=path, files=lists)

@app.route('/load_list', methods=['POST'])
def load_list():
    if 'username' not in session: return render_template('login.html')
    runner.load_tasks(filename=request.form['filename'])
    return 'load'

@app.route('/delete_list', methods=['POST'])
def delete_list():
    if 'username' not in session: return render_template('login.html')
    delete_tasklist(filename=request.form['filename'])
    return 'delete tasklist'

@app.route("/download/<filename>")
def download(filename):
    if 'username' not in session: return render_template('login.html')
    return send_from_directory('tasklists', filename, as_attachment=True) 

if __name__ == '__main__':
    app.debug = False
    app.secret_key = os.urandom(24)
    app.run()