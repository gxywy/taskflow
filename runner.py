#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import os, subprocess, time
from threading import Timer
import logging
import csv

class TaskRunner():
    def __init__(self):
        self.task_queue = []
        self.task_log_queue = []
        self.now_task = None
        self.timer = None

    def load_tasks(self, dir='./', file_name='tasklist.txt'):
        csv_file = open(dir + file_name, 'r')
        reader = csv.DictReader(csv_file)
        for row in reader:
            self.add(row['name'], row['cmd'], row['timeout'])

    def save_tasks(self, dir='./', file_name='tasklist.txt'):
        csv_file = open(dir + file_name, 'w')
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
    
    def timeout_callback(self):
        os.system("TASKKILL /PID " + str(self.now_task['pid']) + " /F /T")

    def run(self):
        self.now_task = None
        now_task_index = 0
        for task in self.task_queue:
            if task['status'] == 'ready':
                self.now_task = task
                now_task_index = self.task_queue.index(task)
                break
        if self.now_task is None:
            return
        self.now_task['status'] = 'running'
        self.now_task['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        
        proc = subprocess.Popen(self.now_task['cmd'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.now_task['pid'] = proc.pid
        
        if self.now_task['timeout'] != 'inf':
            self.timer = Timer(int(self.now_task['timeout']), self.timeout_callback)
            try:
                self.timer.start()
                stdout, stderr = proc.communicate()
            finally:
                self.timer.cancel()
        else:
            stdout, stderr = proc.communicate()
        self.task_log_queue[now_task_index] = stdout

        # run next task
        #self.task_queue.pop(0)
        self.now_task['status'] = 'done'
        self.run()

    def stop(self):
        self.timer.cancel()
        for task in self.task_queue:
            task['status'] = 'done'

    def reset(self):
        for task in self.task_queue:
            task['status'] = 'ready'
    
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

    def get_log(self, index):
        return self.task_log_queue[int(index)]

if __name__ == "__main__":
    runner = TaskRunner()
    runner.load_tasks()
    runner.run()