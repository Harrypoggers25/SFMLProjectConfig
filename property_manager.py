import os
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QLineEdit, QTextEdit

class PropertyManager:
    def __init__(self):
        self.linkers = ['sfml-graphics.lib', 'sfml-system.lib', 'sfml-window.lib', 'sfml-network.lib', 'sfml-audio.lib']
        self.dlinkers = ['sfml-graphics-d.lib', 'sfml-system-d.lib', 'sfml-window-d.lib', 'sfml-network-d.lib', 'sfml-audio-d.lib']
        self.project_name = None

    def setLinkers(self, textbox: QTextEdit):
        self.linkers = [line.strip() for line in textbox.toPlainText().split('\n') if line.strip()]
    
    def setDLinkers(self, textbox: QTextEdit):
        self.dlinkers = [line.strip() for line in textbox.toPlainText().split('\n') if line.strip()]

    def getFile(self, window: QMainWindow):
        filepath, _ = QFileDialog.getOpenFileName(window, 'Select Solution File', '', 'Solution File (*.sln)')
        if filepath:
            filename = os.path.basename(filepath)[:-len('.sln')]
            self.project_name = filename
            filedir = filepath[:-len('/' + filename + '.sln')]
            return {'name': filename, 'path': filepath, 'dir': filedir}
        return None
    
    def getPath(self, window: QMainWindow, initial_dir = None):
        folderPath = QFileDialog.getExistingDirectory(window, 'Select Folder', initial_dir) if initial_dir else QFileDialog.getExistingDirectory(window, 'Select Folder')
        if folderPath:
            return folderPath
        return None
    
    def updateSoltDir(self, window: QMainWindow, textbox: QLineEdit):
        file = self.getFile(window)
        if file:
            textbox.setText(file['dir'])
    
    def updatePath(self, window: QMainWindow, textbox: QLineEdit):
        folder = self.getPath(window, textbox.text())
        if folder:
            textbox.setText(folder)

    def getRelPath(self, pathName: str):
        path = (os.path.join(os.path.dirname(os.path.abspath(__file__)), pathName)).replace('\\', '/')
        return path[:path.find(':')].upper() + path[path.find(':'):]
         
    def getLinkers(self):
        return '\n'.join(self.linkers) + '\n'
    
    def getDLinkers(self):
        return '\n'.join(self.dlinkers) + '\n'