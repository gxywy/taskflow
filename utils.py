import os

def get_tasklists(path='./tasklists/'):
    tasklists = []
    files = os.listdir(path)
    for file in files:
        if not os.path.isdir(file):
            tasklists.append(file)
    return path, tasklists

def delete_tasklist(dir='./tasklists/', filename='main.txt'):
    if filename != 'main.txt':
        os.remove(dir + filename)

def get_password(filename='password'):
    if not os.path.exists(filename):
        ## os.mknod is not available on Windows
        f = open(filename, 'w')
        f.write('admin')
        f.close()
    f = open(filename, 'r')
    password = f.read()
    f.close()
    return password