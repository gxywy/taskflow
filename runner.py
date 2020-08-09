import os, subprocess, time
from threading import Timer
import csv

class TaskRunner():
    def __init__(self):
        self.task_queue = []
        self.task_log_queue = []
        self.global_run = False
        self.now_task = None
        self.timer = None
        self.proc = None

    def load_tasks(self, dir='./tasklists/', filename='main.txt'):
        self.reset()
        if not os.path.exists(dir):
            os.makedirs(dir)
        if not os.path.exists(dir + filename):
            ## os.mknod is not available on Windows
            f = open(dir + filename, 'w')
            f.close()
        csv_file = open(dir + filename, 'r')
        reader = csv.DictReader(csv_file)
        for row in reader:
            self.add(row['name'], row['cmd'], row['timeout'])

    def save_tasks(self, dir='./tasklists/', filename='main.txt'):
        csv_file = open(dir + filename, 'w')
        writer = csv.DictWriter(csv_file, fieldnames=('name', 'cmd', 'timeout'), lineterminator = '\n')
        writer.writeheader()
        for task in self.task_queue:
            epinfo = {"name": task['name'], "cmd": task['cmd'], "timeout": task['timeout']}
            writer.writerow(epinfo)

    def add(self, name, cmd, timeout):
        task = {'name': name, 'cmd': cmd, 'timeout': timeout, 'pid': None, 'status': 'ready', 'start_time': None}
        self.task_queue.append(task)
        self.task_log_queue.append("")
        self.save_tasks()
    
    def kill_task(self):
        self.proc.kill()
        self.proc.terminate()
        #os.system("TASKKILL /PID " + str(self.now_task['pid']) + " /F /T")

    def run(self, index=-1):
        self.now_task = None
        now_task_index = 0

        if index == -1:     # global run
            self.global_run = True
            for task in self.task_queue:
                if task['status'] == 'ready':
                    self.now_task = task
                    now_task_index = self.task_queue.index(task)
                    break
            if self.now_task is None:
                return
        else:               # single run
            self.global_run = False
            self.now_task = self.task_queue[index]
            now_task_index = index

        # run task
        self.now_task['status'] = 'running'
        self.now_task['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        self.proc = subprocess.Popen(self.now_task['cmd'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.now_task['pid'] = self.proc.pid
        
        # set timer or not
        if self.now_task['timeout'] != 'inf':
            self.timer = Timer(int(self.now_task['timeout']), self.kill_task)
            self.timer.start()
            stdout, stderr = self.proc.communicate()
            self.timer.cancel()
        else:
            stdout, stderr = self.proc.communicate()
        
        # after run
        self.task_log_queue[now_task_index] = stdout

        if self.global_run:
            self.now_task['status'] = 'done'
            self.run()
        else:
            self.now_task['status'] = 'ready'

    def stop(self):
        self.global_run = False
        if self.timer is not None:
            self.timer.cancel()
        self.kill_task()

    def reset_status(self):
        for task in self.task_queue:
            task['status'] = 'ready'
    
    def is_alldone(self):
        for task in self.task_queue:
            if task['status'] != 'done':
                return False
        return True

    def reset(self):
        self.global_run = False
        self.task_queue = []
        self.task_log_queue = []

    def delete(self, index):
        self.task_queue.pop(int(index))
        self.task_log_queue.pop(int(index))
        self.save_tasks()

    def edit(self, index, name, cmd, timeout):
        index = int(index)
        self.task_queue[index]['name'] = name
        self.task_queue[index]['cmd'] = cmd
        self.task_queue[index]['timeout'] = timeout
        self.save_tasks()
    
    def get(self, index):
        index = int(index)
        return self.task_queue[index]['name'], self.task_queue[index]['cmd'], self.task_queue[index]['timeout']

    def get_log(self, index):
        return self.task_log_queue[int(index)]

if __name__ == "__main__":
    runner = TaskRunner()
    runner.load_tasks()
    runner.run()