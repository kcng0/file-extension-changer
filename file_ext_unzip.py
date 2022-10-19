from os import path, rename, system, walk
from sys import argv, exit

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLineEdit, QListWidget, QMainWindow,
                             QPushButton)


class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(600, 400)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    if path.isdir(str(url.toLocalFile())):
                        for root, dirs, files in walk(str(url.toLocalFile())):
                            for file in files:
                                links.append(path.join(root, file))
                    else:
                        links.append(str(url.toLocalFile()))
            self.addItems(links)
        else:
            event.ignore()

class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('File Extension Changer')
        self.setFixedHeight(400)
        self.setFixedWidth(800)

        self.listbox_view = ListBoxWidget(self)

        

        self.btn2 = QPushButton('Delete Selected', self)
        self.btn2.setGeometry(650, 50, 100, 30)
        self.btn2.clicked.connect(lambda: self.clear_selected())

        self.btn3 = QPushButton('Clear', self)
        self.btn3.setGeometry(650, 100, 100, 30)
        self.btn3.clicked.connect(lambda: self.listbox_view.clear())


        self.btn = QPushButton('Change', self)
        self.btn.setGeometry(650, 200, 100, 30)
        self.btn.clicked.connect(lambda: self.change_file_ext())
        
        self.textbox = QLineEdit(self)
        self.textbox.move(650, 150)
        self.textbox.resize(100, 30)
        self.textbox.setAlignment(Qt.AlignLeft)
        
        self.btn = QPushButton('Unzip', self)
        self.btn.setGeometry(650, 350, 100 ,30)
        self.btn.clicked.connect(lambda: self.unzip_file(self.pwd_box.text()))
        
        self.pwd_box = QLineEdit(self)
        self.pwd_box.move(650, 300)
        self.textbox.resize(100, 30)
        self.textbox.setAlignment(Qt.AlignLeft)
        
        
        
        

    def clear_selected(self):
        for item in self.listbox_view.selectedItems():
            self.listbox_view.takeItem(self.listbox_view.row(item))


    def change_file_ext(self):
        for index in range(self.listbox_view.count()):
            item = self.listbox_view.item(index)
            if item.text().endswith('.' + self.textbox.text()):
                continue
            else:
                base, ext = path.splitext(item.text())
                rename(item.text(), base + '.' + self.textbox.text())
                item.setText(base + '.' + self.textbox.text())
                
    def unzip_file(self, pwd):
        for index in range(self.listbox_view.count()):
            item = self.listbox_view.item(index)
            if pwd != '':
                cmd = "winrar x -y -p" + pwd + " " + item.text()
                system(cmd)
            else:
                cmd = "winrar x -y " + item.text()
                system(cmd)
            

if __name__ == '__main__':
    app = QApplication(argv)

    demo = AppDemo()
    demo.show()

    exit(app.exec_())