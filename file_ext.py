import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


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
                    if os.path.isdir(str(url.toLocalFile())):
                        for root, dirs, files in os.walk(str(url.toLocalFile())):
                            for file in files:
                                links.append(os.path.join(root, file))
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

        self.btn = QPushButton('Change', self)
        self.btn.setGeometry(650, 300, 100, 30)
        self.btn.clicked.connect(lambda: self.change_file_ext())

        self.btn2 = QPushButton('Delete Selected', self)
        self.btn2.setGeometry(650, 50, 100, 30)
        self.btn2.clicked.connect(lambda: self.clear_selected())

        self.btn3 = QPushButton('Clear', self)
        self.btn3.setGeometry(650, 100, 100, 30)
        self.btn3.clicked.connect(lambda: self.listbox_view.clear())


        self.textbox = QLineEdit(self)
        self.textbox.move(650, 350)
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
                base, ext = os.path.splitext(item.text())
                os.rename(item.text(), base + '.' + self.textbox.text())
                item.setText(base + '.' + self.textbox.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())