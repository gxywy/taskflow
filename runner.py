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
        logging.basicConfig(level=logging.INFO, format='[TaskRunner] %(levelname)s %(message)s at %(asctime)s')

    def load_tasks(self, dir='./', file_name='tasklist'):
        csv_file = open(dir + file_name, 'r')
        reader = csv.DictReader(csv_file)
        for row in reader:
            self.append(row['name'], row['cmd'], row['timeout'])

    def append(self, name, cmd, timeout):
        task = {'name': name, 'cmd': cmd, 'timeout': int(timeout), 'pid': None}
        self.task_queue.append(task)
    
    def timeout_callback(self):
        now_task = self.task_queue.pop(0)
        logging.warning("Task [" + now_task['name'] + "] is terminated by Timer after " + str(now_task['timeout']) + "s")
        os.system("TASKKILL /PID " + str(now_task['pid']) + " /F /T")

        # run next task
        time.sleep(3)
        self.run()

    def run(self):
        now_task = self.task_queue[0]
        logging.warning("Task [" + now_task['name'] + '] started')
        proc = subprocess.Popen(now_task['cmd'])
        timer = Timer(now_task['timeout'], self.timeout_callback)
        now_task['pid'] = proc.pid
        try:
            timer.start()
            stdout, stderr = proc.communicate()
            logging.warning("Task [" + now_task['name'] + "] terminated, Timer canceled")
        finally:
            timer.cancel()


if __name__ == "__main__":
    runner = TaskRunner()
    runner.load_tasks()
    runner.run()