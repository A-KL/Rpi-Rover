import os
import threading
import subprocess

from math import fabs
from os import listdir
from os.path import isfile, join
from gui.components.ui_tile import *
from  gui.components.ui_colors import *

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
        
        self.darkGrayTileStyle = UITileStyle(UITileBackgroundStyle(DarkGray, DarkGray, Black, DarkGray), UITileForegroundStyle(fontPath, LightGray, LightGray))
        self.lightGreenTileStyle = UITileStyle(UITileBackgroundStyle(LightGreen, LightGreen, Black, LightGreen), UITileForegroundStyle(fontPath, Black, LightGreen))
        self.lightYellowTileStyle = UITileStyle(UITileBackgroundStyle(LightYellow, LightYellow, Black, LightYellow), UITileForegroundStyle(fontPath, Black, LightYellow))

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

    def on_change(self, sender, results):
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

    def update(self):
        pass

class ProcessWatcher:
    def __init__(self, processToWatch: str = "python"):
        self.results = list()
        self.callbacks = []
        self.processToWatch = processToWatch
        self.active = False
        self.watcher_thread = threading.Thread(target=self.watch_processes_function, args=()) 

    def begin(self):
        self.active = True
        self.watcher_thread.start()

    def isActive(self):
        return self.active

    def cancel(self):
        self.active = False
        self.watcher_thread.join()

    def onChange(self, callback):
        self.callbacks.append(callback)

    def scan(self):
        print(os.name)
        if  os.name == 'nt':
            import wmi
            f = wmi.WMI()
            for process in f.Win32_Process(name=self.processToWatch):
                if process.CommandLine is not None and process.CommandLine.endswith(".py"):
                    yield (process.ProcessId, process.Name, process.CommandLine)
        if os.name == 'posix':
            subprocess.run(['ps', 'aux' , '|', 'grep', self.processToWatch], capture_output=True, text=True).stdout

    def watch_processes_function(self):
        while self.isActive():
            self.results = list(self.scan())
            for callbacks in self.callbacks:
                callbacks(self, self.results)

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
    pygame.mouse.set_visible(os.name == 'nt')
    
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

    for widget in widgets:
        watcher.onChange(widget.on_change)

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
            widget.update()

        for event in pygame.event.get():

            if event.type == 1792:
                pos = (int(event.x * SCREEN_WIDTH), int(event.y * SCREEN_HEIGHT))
                for widget in widgets:
                    if widget.hit(pos):
                        widget.click()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for widget in widgets:
                    if widget.hit(pos):
                        widget.click()

            if event.type == pygame.QUIT:
                print(event)
                watcher.cancel()
                loop = False
        
        pygame.display.update()