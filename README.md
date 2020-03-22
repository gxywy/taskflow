# task-scheduler

You can run any script or program automatically.

**You can use this python script to run machine learning training experiments automatically**.

You can also use this script for secondary development.

## Usage

- First, edit  `task_list`, write down the task and set timeout like this

  > name,cmd,timeout,pid
  > train_priority,python "F:\ML\A3C\my-a3c-priority\main.py" --log-dir "F:/ML/A3C/logs/" --exp-name "max" --num-process 2,14400
  >
  > train_replay,python "F:\ML\A3C\my-a3c-replay\main.py" --log-dir "F:/ML/A3C/logs/" --exp-name "replay" --num-process 2,14400
  >
  > plot,python -m rl_plotter.plotter --average_group --shaded_err --shaded_std,3

 - run `tasker.py`

- done

## TODO

- [ ] add a task-manager
- [ ] add a callback function for task
- [ ] add advance timer feature