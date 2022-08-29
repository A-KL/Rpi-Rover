from math import fabs
import os

from os import listdir
from os.path import isfile, join

import subprocess

class Runnable:

    def __init__(self, shell, fileName):
        self.process = None
        self.fileName = fileName
        self.shell = shell

    def run(self):
        if self.process == None:
            self.process = subprocess.Popen([self.shell, self.fileName], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def isRunning(self):
        if self.process == None:
            return False
        if self.process.poll() == None:
            return True
        return True

    def wait(self):
        if self.process == None:
            return
        self.process.wait()

    def update(self):
        if self.process == None:
            return        
        stdout_data, stderr_data = self.process.communicate()
        print(stdout_data)
        print(stderr_data)

    def terminate(self):
        if self.process == None:
            return        
        self.process.terminate()

    def returncode(self):
        if self.process == None:
            return 0
        return self.process.returncode

def has_extension(fileName, extension) :
    return extension == os.path.splitext(fileName)[1]

current_file = __file__
current_path = os.path.dirname(os.path.abspath(__file__))

onlyfiles = [f for f in listdir(current_path) if (isfile(join(current_path, f)) and current_path != current_file and has_extension(f, ".py"))]

xbox_service = Runnable('python', join(current_path, 'xbox_service.py'))
xbox_service.run()
xbox_service.update()
xbox_service.wait()

print(onlyfiles)