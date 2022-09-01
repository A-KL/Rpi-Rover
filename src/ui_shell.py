from logging import handlers
from math import fabs
import os

from os import listdir
from os.path import isfile, join
import threading

from gui.components.ui_tile import *
from  gui.components.ui_colors import *

import subprocess

class Runnable:
    def __init__(self, shell, fileName):
        self.process = None
        self.pid = None
        self.fileName = fileName
        self.shell = shell

    def run(self):
        if not self.running():
            self.process = subprocess.Popen([self.shell, self.fileName], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def running(self):
        if self.process == None:
            return False
        if self.process.poll() == None:
            return True
        return False

    def update(self):
        if self.process == None:
            return        
        stdout_data, stderr_data = self.process.communicate()
        print(stdout_data)

    def terminate(self):
        if not self.running():
            return        
        self.process.terminate()
        self.process.wait()

    def returncode(self):
        if self.process == None:
            return 0
        return self.process.returncode

class RunnableWidget:
    def __init__(self, runnable: Runnable, fontPath: str):
        
        self.darkGrayTileStyle = UITileStyle(UITileBackgroundStyle(DarkGray, Black, DarkGray), UITileForegroundStyle(fontPath, Black, DarkGray))
        self.lightGreenTileStyle = UITileStyle(UITileBackgroundStyle(LightGreen, Black, LightGreen), UITileForegroundStyle(fontPath, Black, LightGreen))
        self.lightYellowTileStyle = UITileStyle(UITileBackgroundStyle(LightYellow, Black, LightYellow), UITileForegroundStyle(fontPath, Black, LightYellow))

        self.fileName = os.path.basename(runnable.fileName)
        self.runnable = runnable
        
        self.tile = UITile(185, 120, self.fileName, "IDLE", "instances", self.darkGrayTileStyle)
        self.runnable
        
    def hit(self, position):
        return self.tile.hit(position)

    def click(self):
        self.tile.style = self.lightYellowTileStyle

        if self.runnable.running():          
            self.tile.text = "STOPPING"
            self.runnable.terminate()
        else:
            self.tile.text = "STARTING"
            self.runnable.run()

    def update(self, results):
        count = 0
        for id, name, cmd in results:
            if self.fileName in cmd:
                count = count + 1

        if count > 0:
            self.tile.style = self.lightGreenTileStyle
            self.tile.text = "RUNNING"
            
        else:
            self.tile.style = self.darkGrayTileStyle
            self.tile.text = "IDLE"

        self.tile.footer = "instances:" + str(count)

class ProcessWatcher:
    def __init__(self, processToWatch: str = "python.exe"):
        self.results = list()
        self.handlers = list()
        self.processToWatch = processToWatch
        self.active = False
        self.watcher_thread = threading.Thread(target=self.watch_processes_function, args=()) 

    def begin(self):
        self.active = True
        self.watcher_thread.start()

    def is_active(self):
        return self.active

    def cancel(self):
        self.active = False
        self.watcher_thread.join()

    def scan(self):
        if  os.name == 'nt':
            import wmi
            f = wmi.WMI()
            for process in f.Win32_Process(name=self.processToWatch):
                if process.CommandLine is not None and process.CommandLine.endswith(".py"):
                    yield (process.ProcessId, process.Name, process.CommandLine)

    def watch_processes_function(self):
        while self.is_active():
            self.results = list(self.scan())

        for handler in self.handlers:
            if self.is_active():
                handler(self, self.results)

def list_files(path: str, ext: str):
    for file in listdir(path):
        if path == __file__ :
            continue
        if ext != os.path.splitext(file)[1]:
            continue
        fileName = join(path, file)
        if isfile(fileName):
            yield fileName

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 480
    DISPLAY = (SCREEN_WIDTH,SCREEN_HEIGHT)

    screen = pygame.display.set_mode(DISPLAY)	
    screen.fill(pygame.Color('#000000'))

    current_path = os.path.dirname(os.path.abspath(__file__))

    font_path = join(current_path, '..', 'assets', 'fonts', 'whitrabt.ttf')

    runnables = [Runnable("python", f) for f in list_files(current_path, ".py")]
    widgets = [RunnableWidget(runnable, font_path) for runnable in runnables]

    watcher = ProcessWatcher("python.exe")
    watcher.begin()

    loop = True
    columns = 4
    rows = 3
    padding = 12

    while loop:

      for y in range(0, rows):
        for x in range(0, columns):

            index = y * columns + x
            if index>= len(widgets):
                continue

            widget = widgets[index]
            widget.tile.blit(screen, 
                (
                    padding * (x + 1) + widget.tile.surface.get_width() * x,
                    padding * (y + 1) + widget.tile.surface.get_height() * y
                )
            )
            widget.update(watcher.results)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                for widget in widgets:
                    if widget.hit(pygame.mouse.get_pos()):
                        widget.click()

            if event.type == pygame.QUIT or event.type == 1792:
                print(event)
                watcher.cancel()
                loop = False
        
        pygame.display.update()
    

