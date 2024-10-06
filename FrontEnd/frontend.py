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
        self.setStyleSheet("background-color: royalblue; font-family: Times New Roman;")
        
        # calling an initalizer function to add objects to the form
        self.initUI()
    
    # ------------------------------------- UI function -------------------------------------
    def initUI(self):
        
        single_sort_time=0 # variable to store single sort time
        multiple_sort_time=0 # varibale to store multi column sort time
        progress=0 # variable to save the progress
        headers = ["A","B","C","D","E","F","G"]
        
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

        # ------------------------------------- Scraping product name input -------------------------------------
        
        data_scrap_url = QLineEdit() # adding a text input in UI
        data_scrap_url.setPlaceholderText("Enter product name to scrap data: ") # setting up a place holder for user guidance
        data_scrap_url.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 14px;") # setting the stylesheet for the product name input
        data_scrap_url.setMinimumWidth(400) # setting the minimum width of the product name field
        
        # ------------------------------------- Scraping buttons layout -------------------------------------

        # common stylesheet for the elements in UI
        common_stylesheet = "color:black; font-weight:bold; font-size: 14px; background-color:"
        
        # start button
        start_scrap_btn = QPushButton("Start")
        start_scrap_btn.setStyleSheet(common_stylesheet+" green;")
        # start_scrap_btn.clicked.connect(self.start_scrap_data)
        
        # pause button
        pause_scrap_btn = QPushButton("Pause")
        pause_scrap_btn.setStyleSheet(common_stylesheet+" yellow;")
        # resume_scrap_btn.clicked.connect(self.pause_scrap_data)

        # resume button
        resume_scrap_btn = QPushButton("Resume")
        resume_scrap_btn.setStyleSheet(common_stylesheet+" blue;")
        # resume_scrap_btn.clicked.connect(self.resume_scrap_data)
        
        # stop button
        stop_scrap_btn = QPushButton("Stop")
        stop_scrap_btn.setStyleSheet(common_stylesheet+" red;")
        # stop_scrap_btn.clicked.connect(self.stop_scrap_data)
        
        # ------------------------------------- Progress bar for scraping task -------------------------------------
        
        scrap_progress = QProgressBar() # a new progress bar object
        scrap_progress.setValue(progress) # by default value of progress bar
        scrap_progress.setTextVisible(True) # adding a bool variable to make it visible
        scrap_progress.setStyleSheet("color: white;") # adding style sheet
        
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
        data_table.setHorizontalHeaderLabels(headers) # adding the table headers to the table
        data_table.setStyleSheet("color: black; background-color: lightgray; font-size: 11px;") # adding the stylesheet
        
        # setting the column width to automatically adjust equally
        table_header = data_table.horizontalHeader()
        table_header.setSectionResizeMode(QHeaderView.Stretch)
        
        # ------------------------------------- Single column sort layout -------------------------------------

        single_column_sort_label = QLabel("Sort data by column: ") # label text for the sort
        single_column_sort_label.setFixedWidth(130)
        single_column_sort_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding a stylesheet for the label
        single_column_sort_combobox = QComboBox() # adding a combobox to select a column
        single_column_sort_combobox.setStyleSheet(common_stylesheet+"white;") # adding stylesheet
        single_column_sort_combobox.addItems(headers) # adding the headers to the combo box loaded from the headers of the data
        single_column_sort_btn = QPushButton("Sort") # adding a button for single sort triggering
        single_column_sort_btn.setStyleSheet(common_stylesheet+" orange;") # adding style to button
        single_sort_time_label = QLabel("Time taken: "+ str(single_sort_time*100)+" ms") # displaying the sortgng time
        single_sort_time_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding stylesheet
        
        # adding the elements to main single column sorting layout container
        single_column_sort_container = QHBoxLayout()
        single_column_sort_container.addWidget(single_column_sort_label)
        single_column_sort_container.addWidget(single_column_sort_combobox)
        single_column_sort_container.addWidget(single_column_sort_btn)
        single_column_sort_container.addWidget(single_sort_time_label)
        
        # ------------------------------------- Multiple column sort layout -------------------------------------

        # label
        multiple_column_sort_label = QLabel("Multiple sort (Select Column1 and Column2): ") # label text for the sort
        multiple_column_sort_label.setFixedWidth(285) # setting the fixed width
        multiple_column_sort_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding a stylesheet for the label
        
        # comboboxes for column selection
        multiple_column_sort_combobox1 = QComboBox() # adding a combobox to select column 1
        multiple_column_sort_combobox1.setStyleSheet(common_stylesheet+"white;") # adding the stylesheet
        multiple_column_sort_combobox1.addItems(headers) # adding the headers to the combo box loaded from the headers of the data
        multiple_column_sort_combobox2 = QComboBox() # adding a combobox to select column 2
        multiple_column_sort_combobox2.setStyleSheet(common_stylesheet+"white;") # adding the stylesheet
        multiple_column_sort_combobox2.addItems(headers) # adding the headers to the combo box loaded from the headers of the data
        
        # button
        multiple_column_sort_btn = QPushButton("Multi-Column Sort") # adding a button for single sort triggering
        multiple_column_sort_btn.setStyleSheet(common_stylesheet+" orange;") # adding style to button
        
        # time display label
        multiple_sort_time_label = QLabel("Time taken: "+ str(multiple_sort_time*100)+" ms") # displaying the time taken to implement the multi level sorting
        multiple_sort_time_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding stylesheet for the time label
        
        # adding the elements to main multi column sorting layout container
        multiple_column_sort_container = QHBoxLayout()
        multiple_column_sort_container.addWidget(multiple_column_sort_label)
        multiple_column_sort_container.addWidget(multiple_column_sort_combobox1)
        multiple_column_sort_container.addWidget(multiple_column_sort_combobox2)
        multiple_column_sort_container.addWidget(multiple_column_sort_btn)
        multiple_column_sort_container.addWidget(multiple_sort_time_label)
        
        # ------------------------------------- Searching functionality -------------------------------------

        # label
        search_column_sort_label = QLabel("Filter by: ") # label text for the sort
        search_column_sort_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding a stylesheet for the label
        search_column_sort_label.setFixedWidth(60) # fixing the width
        
        # input 1 and combobox 1
        self.search_column_input1 = QLineEdit() # adding a text input in UI for search column 1
        self.search_column_input1.setPlaceholderText("Query column 1: ") # setting up a place holder for user guidance
        self.search_column_input1.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 14px;") # setting the stylesheet for the product name input
        self.search_column_input1.setMinimumWidth(100) # setting the minimum width of the product name field
        self.search_column_sort_combobox1 = QComboBox() # adding a combobox to select column 1
        self.search_column_sort_combobox1.setStyleSheet(common_stylesheet+"white;") # adding the stylesheet
        self.search_column_sort_combobox1.addItems(headers) # adding the headers to the combo box loaded from the headers of the data
        self.search_column_sort_combobox1.setMinimumWidth(100) # setting the minimum width of the product name field
        
        # input 2 and combobox 2
        self.search_column_input2 = QLineEdit() # adding a text input in UI for search column 2
        self.search_column_input2.setPlaceholderText("Query column 2: ") # setting up a place holder for user guidance
        self.search_column_input2.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 14px;") # setting the stylesheet for the product name input
        self.search_column_input2.setMinimumWidth(100) # setting the minimum width of the product name field
        self.search_column_sort_combobox2 = QComboBox() # adding a combobox to select column 2
        self.search_column_sort_combobox2.setStyleSheet(common_stylesheet+"white;") # adding the stylesheet
        self.search_column_sort_combobox2.addItems(headers) # adding the headers to the combo box loaded from the headers of the data
        self.search_column_sort_combobox2.setMinimumWidth(100) # setting the minimum width of the product name field
        
        # push button
        self.search_column_sort_btn = QPushButton("Search") # adding a button for single sort triggering
        self.search_column_sort_btn.setStyleSheet(common_stylesheet+" lightgrey;") # adding style to button
        
        # adding the objects to search container 1
        search_column_sort_container1=QHBoxLayout()
        search_column_sort_container1.addWidget(search_column_sort_label)
        search_column_sort_container1.addWidget(self.search_column_sort_combobox1)
        search_column_sort_container1.addWidget(self.search_column_input1)
        search_column_sort_container1.addWidget(self.search_column_sort_combobox2)
        search_column_sort_container1.addWidget(self.search_column_input2)
        search_column_sort_container1.addWidget(self.search_column_sort_btn)
        
        # ------------------------------------- Filter functionality -------------------------------------

        # combo box
        filter_combobox = QComboBox() # adding a combobox to apply filters
        filter_combobox.addItems(["Contains","Ends with","Starts with"]) # filter content
        
        # searching functionality container
        search_column_sort_container = QVBoxLayout()
        
        search_column_sort_container.addLayout(search_column_sort_container1)

        # ------------------------------------- Adding layouts to main layout -------------------------------------
        
        main_layout.addLayout(title_container)
        main_layout.addLayout(scrap_data_container)
        main_layout.addWidget(data_table)
        main_layout.addLayout(single_column_sort_container)
        main_layout.addLayout(multiple_column_sort_container)
        main_layout.addLayout(search_column_sort_container)
        
# a main function to 
def main():
    app = QApplication(sys.argv)
    window =  MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()