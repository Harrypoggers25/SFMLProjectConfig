import os
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QLineEdit

class PropertyManager:
    @staticmethod
    def getFile(window: QMainWindow):
        filepath, _ = QFileDialog.getOpenFileName(window, 'Select Solution File', '', 'Solution File (*.sln)')
        if filepath:
            filename = os.path.basename(filepath)[:-len('.sln')]
            filedir = filepath[:-len('/' + filename + '.sln')]
            return {'name': filename, 'path': filepath, 'dir': filedir}
        return None
    
    @staticmethod
    def getPath(window: QMainWindow, initial_dir = None):
        folderPath = QFileDialog.getExistingDirectory(window, 'Select Folder', initial_dir) if initial_dir else QFileDialog.getExistingDirectory(window, 'Select Folder')
        if folderPath:
            return folderPath
        return None
    
    @staticmethod
    def updateSoltDir(window: QMainWindow, textbox: QLineEdit):
        file = PropertyManager.getFile(window)
        if file:
            textbox.setText(file['dir'])
    
    @staticmethod
    def updatePath(window: QMainWindow, textbox: QLineEdit):
        folder = PropertyManager.getPath(window, textbox.text())
        if folder:
            textbox.setText(folder)

    @staticmethod
    def getRelPath(pathName: str):
        return (os.path.join(os.path.dirname(os.path.abspath(__file__)), pathName)).replace('\\', '/')
    
    @staticmethod
    def getLinkers():
        return 'sfml-graphics.lib\nsfml-system.lib\nsfml-window.lib\nsfml-network.lib\nsfml-audio.lib\n'