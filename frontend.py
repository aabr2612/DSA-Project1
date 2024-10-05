import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# a main class inheriting from the QMainWindow so that it can access elements
class MainWindow(QMainWindow):
    
    # ------------------------------------- Self initalizer -------------------------------------
    def __init__(self):
        
        super().__init__() # an initializer allowing to make a window form
        self.setWindowTitle("Project-1 Scraping and Data sorting") # setting the window title
        
        # setting the geometry of the form
        win_width = 900 # inital width of the form
        win_height = 690 # initial height of the form
        screen = QApplication.primaryScreen() # getting the size of the screen
        init_x_position = (screen.geometry().width() - win_width) // 2 # setting the initial start position for the x-axis to ensure that it is in mid
        init_y_position = 30 # setting the initial start position for the y-axis
        self.setGeometry(init_x_position, init_y_position, win_width, win_height) # setting the initial size and axis of the for
        
        # setting some stylesheet for the window
        self.setStyleSheet("background-color: grey;")
        
        # calling an initalizer function to add objects to the form
        self.initUI()
    
    # ------------------------------------- UI function -------------------------------------
    def initUI(self):
        
        # ------------------------------------- Basic setup -------------------------------------
        
        central_widget = QWidget(self) # a central container to ensure the responsiveness of the window and holding the elements
        self.setCentralWidget(central_widget) # setting the central widget of the window
        main_layout = QVBoxLayout(central_widget) # main layout to hold all the elements to be added to the UI
        
        # ------------------------------------- Title layout -------------------------------------

        title_label =  QLabel("Project1 - Sorting Algorithms",self) # setting the label text
        title_label.setFont(QFont("Times New Romans",30)) # setting the text font and size
        title_label.setFixedHeight(80) # fixing the height of the label
        title_label.setAlignment(Qt.AlignCenter) # fixing the alignment of the label
        title_label.setStyleSheet("color: black;background-color:white;font-weight: bold;") # adding a stylesheet for the label
        
        title_container = QVBoxLayout() # title container to hold the label
        title_container.addWidget(title_label) # adding label to the layout
        
        # ------------------------------------- Scraping buttons layout -------------------------------------

        # common stylesheet for the buttons in the UI
        buttons_stylesheet = "color:black; font-weight:bold; font-size: 11;"
        
        # start button
        start_scrap_btn = QPushButton("Start")
        start_scrap_btn.setStyleSheet(buttons_stylesheet+"background-color: green;")
        # start_scrap_btn.clicked.connect(self.start_scrap_data)
        
        # pause button
        pause_scrap_btn = QPushButton("Pause")
        pause_scrap_btn.setStyleSheet(buttons_stylesheet+"background-color: yellow;")
        # resume_scrap_btn.clicked.connect(self.pause_scrap_data)

        # resume button
        resume_scrap_btn = QPushButton("Resume")
        resume_scrap_btn.setStyleSheet(buttons_stylesheet+"background-color: blue;")
        # resume_scrap_btn.clicked.connect(self.resume_scrap_data)
        
        # stop button
        stop_scrap_btn = QPushButton("Stop")
        stop_scrap_btn.setStyleSheet(buttons_stylesheet+"background-color: red;")
        # stop_scrap_btn.clicked.connect(self.stop_scrap_data)
        
        # a buttons container to hold the buttons in the window
        buttons_container = QHBoxLayout()
        buttons_container.addWidget(start_scrap_btn)
        buttons_container.addWidget(pause_scrap_btn)
        buttons_container.addWidget(resume_scrap_btn)
        buttons_container.addWidget(stop_scrap_btn)
        
        # ------------------------------------- Adding layouts to main layout -------------------------------------
        
        main_layout.addLayout(title_container)
        main_layout.addLayout(buttons_container)
        
        
    
    
         
def main():
    app = QApplication(sys.argv)
    window =  MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()