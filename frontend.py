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
        
        # a central container to ensure the responsiveness of the windowand holding the elements
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget) # inializing the container as main container to hold QMainWindow items
        
        # main layout to carry all the elements in the window
        main_layout = QVBoxLayout(central_widget)
        
        # adding a title label to the window
        title_label =  QLabel("Project1 - Sorting Algorithms",self) # setting the label text
        title_label.setFont(QFont("Times New Romans",30)) # setting the text font and size
        title_label.setFixedHeight(80) # fixing the height of the label
        title_label.setAlignment(Qt.AlignCenter) # fixing the alignment of the label
        title_label.setStyleSheet("color: black;background-color: grey;font-weight: bold;") # adding a stylesheet for the label

        # making a child container for the label
        label_container = QVBoxLayout()
        label_container.addWidget(title_label) # adding the label to the vertical box layout
        
        # adding the child vertical layout for the label to the main layout
        main_layout.addLayout(label_container)
        
        
    
    
         
def main():
    app = QApplication(sys.argv)
    window =  MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()