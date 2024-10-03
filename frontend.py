import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

# a main class inheriting from the QMainWindow so that it can access elements
class MainWindow(QMainWindow):
    # self initalizer
    def __init__(self):
        # an initializer of the parent class to ensure that it allows to create a window
        super().__init__()
        # setting the windows title
        self.setWindowTitle("Project1: Sorting Algorithms")
        
def main():
    app = QApplication(sys.argv)
    window =  MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()