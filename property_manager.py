import os
import shutil
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QLineEdit, QTextEdit, QPushButton

class PropertyManager:
    def __init__(self):
        self.linkers = ['sfml-graphics.lib', 'sfml-system.lib', 'sfml-window.lib', 'sfml-network.lib', 'sfml-audio.lib']
        self.dlinkers = ['sfml-graphics-d.lib', 'sfml-system-d.lib', 'sfml-window-d.lib', 'sfml-network-d.lib', 'sfml-audio-d.lib']
        self.project_name = None
        self.file = None

    def setLinkers(self, textbox: QTextEdit):
        self.linkers = [line.strip() for line in textbox.toPlainText().split('\n') if line.strip()]
    
    def setDLinkers(self, textbox: QTextEdit):
        self.dlinkers = [line.strip() for line in textbox.toPlainText().split('\n') if line.strip()]

    def getFile(self, window: QMainWindow):
        filepath, _ = QFileDialog.getOpenFileName(window, 'Select Solution File', '', 'Solution File (*.sln)')
        if filepath:
            filename = os.path.basename(filepath)[:-len('.sln')]
            self.project_name = filename
            filedir = filepath[:-len('/' + filename + '.sln')].replace('/', '\\')
            filepath = filepath.replace('/', '\\')

            self.file = {'name': filename, 'path': filepath, 'dir': filedir}
            return self.file
        return None
    
    def getPath(self, window: QMainWindow, initial_dir = None):
        folderPath = QFileDialog.getExistingDirectory(window, 'Select Folder', initial_dir) if initial_dir else QFileDialog.getExistingDirectory(window, 'Select Folder')
        if folderPath:
            return folderPath.replace('/', '\\')
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
        path = (os.path.join(os.path.dirname(os.path.abspath(__file__)), pathName)).replace('/', '\\')
        return path[:path.find(':')].upper() + path[path.find(':'):]
         
    def getLinkers(self):
        return '\n'.join(self.linkers) + '\n'
    
    def getDLinkers(self):
        return '\n'.join(self.dlinkers) + '\n'
    
    @staticmethod
    def insert_line_in_file(file_path, new_line, position):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        lines.insert(position, new_line + '\n')
        
        with open(file_path, 'w') as file:
            file.writelines(lines)

    @staticmethod
    def find_line_in_file(file_path, line):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines.index(line)

    def configureSFML(self, window: QMainWindow, btn: QPushButton, include_dir, lib_dir, bin_dir):
        btn.setEnabled (False)
        vcxproj_dir = f'{self.file['dir']}/{self.file['name']}'
        vcxproj_path = f'{vcxproj_dir}/{self.file['name']}.vcxproj'

        with open(vcxproj_path, 'r') as file:
            lines = file.readlines()

        new_lines = []
        r = 0
        for i in range(len(lines)):
            if (lines[i].find('<AdditionalIncludeDirectories>') != -1 or 
                lines[i].find('<AdditionalLibraryDirectories>') != -1 or 
                lines[i].find('<AdditionalDependencies>') != -1):
                continue
            if lines[i] == '    </ClCompile>\n':
               new_lines.append(f'      <AdditionalIncludeDirectories>{include_dir}</AdditionalIncludeDirectories>\n')
            if lines[i] == '    </Link>\n':
                new_lines.append(f'      <AdditionalLibraryDirectories>{lib_dir}</AdditionalLibraryDirectories>\n')
                if r % 2 == 0:
                    new_lines.append(f'      <AdditionalDependencies>{';'.join(self.dlinkers) + ';'}</AdditionalDependencies>\n')
                else:
                    new_lines.append(f'      <AdditionalDependencies>{';'.join(self.linkers) + ';'}</AdditionalDependencies>\n')
                r += 1
            new_lines.append(lines[i])
        
        with open(vcxproj_path, 'w') as file:
            file.writelines(new_lines)


        # Copies SFML bin files to project directory
        for item in os.listdir(bin_dir):
            src_item = os.path.join(bin_dir, item)
            dst_item = os.path.join(vcxproj_dir, item)

            if os.path.isdir(src_item):
                shutil.copytree(src_item, dst_item)
            else:
                shutil.copy2(src_item, dst_item)

        window.close()