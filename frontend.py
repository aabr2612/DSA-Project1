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
        win_width = 800 # inital width of the form
        win_height = 690 # initial height of the form
        screen = QApplication.primaryScreen() # getting the size of the screen
        init_x_position = (screen.geometry().width() - win_width) // 2 # setting the initial start position for the x-axis to ensure that it is in mid
        init_y_position = 30 # setting the initial start position for the y-axis
        self.setGeometry(init_x_position, init_y_position, win_width, win_height) # setting the initial size and axis of the window form
        
        # setting the minimum size for the screen
        self.setMinimumSize(win_width,win_height)
        
        # setting some stylesheet for the window
        self.setStyleSheet("background-color: grey; font-family: Times New Roman;")
        
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
        title_label.setFixedHeight(80) # fixing the height of the label
        title_label.setAlignment(Qt.AlignCenter) # fixing the alignment of the label
        title_label.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 30px") # adding a stylesheet for the label
        
        title_container = QVBoxLayout() # title container to hold the label
        title_container.addWidget(title_label) # adding label to the layout

        # ------------------------------------- Scraping URL input -------------------------------------
        
        data_scrap_url = QLineEdit() # adding a text input in UI
        data_scrap_url.setPlaceholderText("Enter a valid URL to scrap data") # setting up a place holder for user guidance
        data_scrap_url.setStyleSheet("color: black; background-color: white; font-size: 14px;") # setting the stylesheet for the url input
        data_scrap_url.setMinimumWidth(400) # setting the minimum width of the url input field
        
        # ------------------------------------- Scraping buttons layout -------------------------------------

        # common stylesheet for the buttons in the UI
        buttons_stylesheet = "color:black; font-weight:bold; font-size: 14px;"
        
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
        
        # ------------------------------------- Progress bar for scraping task -------------------------------------
        
        scrap_progress = QProgressBar()
        scrap_progress.setValue(0)
        scrap_progress.setTextVisible(True)
        
        # ------------------------------------- Setting up the scraping elements in layout -------------------------------------
        
        scrap_data_container = QVBoxLayout() # a main layout holder for the scraping task UI
        
        # a container to hold the url input, progress bar and buttons in the window
        scrapping_functionality_container = QHBoxLayout()
        scrapping_functionality_container.addWidget(data_scrap_url)
        scrapping_functionality_container.addWidget(start_scrap_btn)
        scrapping_functionality_container.addWidget(pause_scrap_btn)
        scrapping_functionality_container.addWidget(resume_scrap_btn)
        scrapping_functionality_container.addWidget(stop_scrap_btn)
        
        # adding the elements to the main scraping UI container
        
        scrap_data_container.addLayout(scrapping_functionality_container)
        scrap_data_container.addWidget(scrap_progress)
        
        # ------------------------------------- Adding the data table to the UI -------------------------------------
        
        data_table = QTableWidget() # a new table layout
        data_table.setColumnCount(7) # setting the column count for the table
        data_table.setHorizontalHeaderLabels(["Attribute 1", "Attribute 2", "Attribute 3", "Attribute 4", 
             "Attribute 5", "Attribute 6", "Attribute 7"])
        
        table_header = data_table.horizontalHeader()
        table_header.setSectionResizeMode(QHeaderView.Stretch)
        
         
        # ------------------------------------- Adding layouts to main layout -------------------------------------
        
        main_layout.addLayout(title_container)
        main_layout.addLayout(scrap_data_container)
        main_layout.addWidget(data_table)
        
        
    
    
         
def main():
    app = QApplication(sys.argv)
    window =  MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()