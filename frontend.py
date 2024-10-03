import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

# a main class inheriting from the QMainWindow so that it can access elements
class MainWindow(QMainWindow):
    # self initalizer
    def __init__(self):
        
        # setting up the initial window specifications
        super().__init__() # an initializer of the parent class to ensure that it allows to create a window
        
        self.setWindowTitle("Project1: Sorting Algorithms") # setting the windows title
        screen = QApplication.primaryScreen() # getting the size of the screen
        init_x_posi = (screen.geometry().width()-900)//2 # setting the initial x position of the window
        self.setGeometry(init_x_posi,30,900,690) # setting the initial geometry of the window
        
        self.initUI() # calling the init function to add objects to the UI window
    
    # a function to add objects and necessary UI objects to make a UI
    def initUI(self):
        central_widget = QWidget(self)
        
    
    
         
def main():
    app = QApplication(sys.argv)
    window =  MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()