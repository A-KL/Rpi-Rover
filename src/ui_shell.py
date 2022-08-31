from math import fabs
import os

from os import listdir
from os.path import isfile, join
import threading

from gui.components.ui_tile import *
from  gui.components.ui_colors import *

import subprocess

class RunnableContext:
    def __init__(self):
        self._lock = threading.Lock()
        self.list = list()
        self.active = True

    def set_list(self, list):
        self.list = list

    def get_list(self):
        return self.list

    def is_active(self):
        return self.active

    def cancel(self):
        self.active = False

class RunnableWidget:
    def __init__(self, shell: str, filePath: str, font_path: str):
        self.process = None
        self.filePath = filePath
        self.shell = shell
        self.darkGrayTileStyle = UITileStyle(UITileBackgroundStyle(DarkGray, Black, DarkGray), UITileForegroundStyle(font_path, Black, DarkGray))
        self.lightGreenTileStyle = UITileStyle(UITileBackgroundStyle(LightGreen, Black, LightGreen), UITileForegroundStyle(font_path, Black, LightGreen))
        self.tile = UITile(185, 120, "state", "IDLE", os.path.basename(filePath), self.darkGrayTileStyle)
        
    def hit(self, position):
        return self.tile.hit(position)

    def update(self, context: RunnableContext):
        count = 0
        for id, name, cmd in context.get_list():
            if self.filePath in cmd:
                count = count + 1

        if count > 0:
            self.tile.style = self.lightGreenTileStyle
            self.tile.text = "RUNNING"
            self.tile.caption = "instances:" + str(count)
        else:
            self.tile.style = self.darkGrayTileStyle
            self.tile.text = "IDLE"
            self.tile.caption = ""

    def click(self):
        pass

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

def active(filter: str):
    if  os.name == 'nt':
        import wmi
        f = wmi.WMI()
        for process in f.Win32_Process(name="python.exe"):
            if process.CommandLine is not None and process.CommandLine.endswith(filter):
                yield (process.ProcessId, process.Name, process.CommandLine)

def watch_processes_function(filter: str, context: RunnableContext):
    while context.is_active():
        context.set_list(list(active(filter)))

def has_extension(fileName, extension) :
    return extension == os.path.splitext(fileName)[1]

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


    # runing_ids, running_names, runing_files = active(".py")
    runnable_files = [f for f in listdir(current_path) if (isfile(join(current_path, f)) and current_path != __file__ and has_extension(f, ".py"))]

    widgets = [RunnableWidget("python", f, font_path) for f in runnable_files]

    # xbox_service = Runnable('python', join(current_path, 'xbox_service.py'))
    # xbox_service.run()
    # xbox_service.update()
    # xbox_service.wait()

    columns = 4
    rows = 3
    padding = 12

    watcher_context = RunnableContext()
    watcher_thread = threading.Thread(target=watch_processes_function, args=(".py", watcher_context,))
    watcher_thread.start()

    loop = True

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
            widget.update(watcher_context)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                for widget in widgets:
                    if widget.hit(pygame.mouse.get_pos()):
                        widget.click()

            if event.type == pygame.QUIT or event.type == 1792:
                print(event)
                watcher_context.cancel()
                watcher_thread.join()
                loop = False
        
        pygame.display.update()
    

