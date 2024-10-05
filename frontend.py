import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# a main class inheriting from the QMainWindow so that it can access elements
class MainWindow(QMainWindow):
    # self initalizer
    def __init__(self):
        
         # setting the geometry of the form
        win_width = 900 # inital width of the form
        win_height = 690 # initial height of the form
        screen = QApplication.primaryScreen() # getting the size of the screen
        init_x_position = (screen.geometry().width() - win_width) // 2 # setting the initial start position for the x-axis to ensure that it is in mid
        init_y_position = 30 # setting the initial start position for the y-axis
        self.setGeometry(init_x_position, init_y_position, win_width, win_height) # setting the initial size and axis of the for
        
        # calling an initalizer function to add objects to the form
        self.initUI()
    
    # a function to add objects and necessary UI objects to make a UI
    def initUI(self):
        
        # a central container to ensure the responsiveness of the windowand holding the elements
        central_widget = QWidget(self)
        # setting the central widget of the window
        self.setCentralWidget(central_widget)
        
        # main layout to hold all the elements to be added to the UI
        main_layout = QVBoxLayout(central_widget)
        
        # adding a title label to the window
        title_label =  QLabel("Project1 - Sorting Algorithms",self) # setting the label text
        title_label.setFont(QFont("Times New Romans",30)) # setting the text font and size
        title_label.setFixedHeight(80) # fixing the height of the label
        title_label.setAlignment(Qt.AlignCenter) # fixing the alignment of the label
        title_label.setStyleSheet("color: black;background-color: grey;font-weight: bold;") # adding a stylesheet for the label

        # title container to hold the label
        title_container = QVBoxLayout()
        title_container.addWidget(title_label) # adding label to the layout
        
        # adding the title container to the main layout
        main_layout.addLayout(title_container)
        
        
    
    
         
def main():
    app = QApplication(sys.argv)
    window =  MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()