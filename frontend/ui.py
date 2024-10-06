import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from frontend import utility as ut

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
        
        self.single_sort_time=0 # variable to store single sort time
        self.multiple_sort_time=0 # varibale to store multi column sort time
        self.progress=0 # variable to save the progress
        self.headers = ["A","B","C","D","E","F","G"]
        
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
        
        self.data_scrap_product = QLineEdit() # adding a text input in UI
        self.data_scrap_product.setPlaceholderText("Enter product name to scrap data: ") # setting up a place holder for user guidance
        self.data_scrap_product.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 14px;") # setting the stylesheet for the product name input
        self.data_scrap_product.setMinimumWidth(400) # setting the minimum width of the product name field
        
        # ------------------------------------- Scraping buttons layout -------------------------------------

        # common stylesheet for the elements in UI
        common_stylesheet = "color:black; font-weight:bold; font-size: 14px; background-color:"
        
        # start button
        self.start_scrap_btn = QPushButton("Start")
        self.start_scrap_btn.setStyleSheet(common_stylesheet+" green;")
        # self.start_scrap_btn.clicked.connect(self.time)
        
        # pause button
        self.pause_scrap_btn = QPushButton("Pause")
        self.pause_scrap_btn.setStyleSheet(common_stylesheet+" yellow;")
        # resume_scrap_btn.clicked.connect(self.pause_scrap_data)

        # resume button
        self.resume_scrap_btn = QPushButton("Resume")
        self.resume_scrap_btn.setStyleSheet(common_stylesheet+" blue;")
        # resume_scrap_btn.clicked.connect(self.resume_scrap_data)
        
        # stop button
        self.stop_scrap_btn = QPushButton("Stop")
        self.stop_scrap_btn.setStyleSheet(common_stylesheet+" red;")
        # stop_scrap_btn.clicked.connect(self.stop_scrap_data)
        
        # ------------------------------------- Progress bar for scraping task -------------------------------------
        
        scrap_progress = QProgressBar() # a new progress bar object
        scrap_progress.setValue(self.progress) # by default value of progress bar
        scrap_progress.setTextVisible(True) # adding a bool variable to make it visible
        scrap_progress.setStyleSheet("color: white;") # adding style sheet
        
        # ------------------------------------- Button and input for loading data -------------------------------------

        self.file_name_input = QLineEdit() # adding a text input in UI
        self.file_name_input.setPlaceholderText("Enter file name to load data: ") # setting up a place holder for user guidance
        self.file_name_input.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 14px;") # setting the stylesheet for the product name input
        self.file_name_input.setMinimumWidth(400) # setting the minimum width of the product name field
        
        # load button
        self.load_from_csv_btn = QPushButton("Load data from CSV")
        self.load_from_csv_btn.setStyleSheet(common_stylesheet+" lightgrey;")
        self.load_from_csv_btn.clicked.connect(self.load_data_from_csv)
        
        
        # ------------------------------------- Setting up the scraping elements and load data in layout -------------------------------------
        
        scrap_data_container = QVBoxLayout() # a main layout holder for the scraping task UI
        
        # a container to hold the product input, progress bar and buttons in the window
        scrapping_functionality_container = QHBoxLayout()
        scrapping_functionality_container.addWidget(self.data_scrap_product)
        scrapping_functionality_container.addWidget(self.start_scrap_btn)
        scrapping_functionality_container.addWidget(self.pause_scrap_btn)
        scrapping_functionality_container.addWidget(self.resume_scrap_btn)
        scrapping_functionality_container.addWidget(self.stop_scrap_btn)
        
        # a container to hold the input and button
        
        load_data_container = QHBoxLayout()
        load_data_container.addWidget(self.file_name_input)
        load_data_container.addWidget(self.load_from_csv_btn)
        
        # adding the elements to the main scraping UI container
        
        scrap_data_container.addLayout(scrapping_functionality_container)
        scrap_data_container.addWidget(scrap_progress)
        scrap_data_container.addLayout(load_data_container)

        # ------------------------------------- Adding the data table to the UI -------------------------------------
        
        self.data_table = QTableWidget() # a new table layout
        self.data_table.setColumnCount(7) # setting the column count for the table
        self.data_table.setHorizontalHeaderLabels(self.headers) # adding the table headers to the table
        self.data_table.setStyleSheet("color: black; background-color: lightgray; font-size: 11px;") # adding the stylesheet
        
        # setting the column width to automatically adjust equally
        table_header = self.data_table.horizontalHeader()
        table_header.setSectionResizeMode(QHeaderView.Stretch)
        
        # ------------------------------------- Single column sort layout -------------------------------------

        single_column_sort_label = QLabel("Single Column Sort: ") # label text for the sort
        single_column_sort_label.setFixedWidth(130)
        single_column_sort_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding a stylesheet for the label
        self.single_column_sort_combobox = QComboBox() # adding a combobox to select a column
        self.single_column_sort_combobox.setStyleSheet(common_stylesheet+"white;") # adding stylesheet
        self.single_column_sort_combobox.addItems(self.headers) # adding the headers to the combo box loaded from the headers of the data
        self.single_column_sort_btn = QPushButton("Sort") # adding a button for single sort triggering
        self.single_column_sort_btn.setStyleSheet(common_stylesheet+" orange;") # adding style to button
        single_sort_time_label = QLabel("Time taken: "+ str(self.single_sort_time*100)+" ms") # displaying the sortgng time
        single_sort_time_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding stylesheet
        
        # adding the elements to main single column sorting layout container
        single_column_sort_container = QHBoxLayout()
        single_column_sort_container.addWidget(single_column_sort_label)
        single_column_sort_container.addWidget(self.single_column_sort_combobox)
        single_column_sort_container.addWidget(self.single_column_sort_btn)
        single_column_sort_container.addWidget(single_sort_time_label)
        
        # ------------------------------------- Multiple column sort layout -------------------------------------

        # label
        multiple_column_sort_label = QLabel("Multiple Columns Sort: ") # label text for the sort
        multiple_column_sort_label.setFixedWidth(150) # setting the fixed width
        multiple_column_sort_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding a stylesheet for the label
        
        # comboboxes for column selection
        self.multiple_column_sort_combobox1 = QComboBox() # adding a combobox to select column 1
        self.multiple_column_sort_combobox1.setStyleSheet(common_stylesheet+"white;") # adding the stylesheet
        self.multiple_column_sort_combobox1.addItems(self.headers) # adding the headers to the combo box loaded from the headers of the data
        self.multiple_column_sort_combobox2 = QComboBox() # adding a combobox to select column 2
        self.multiple_column_sort_combobox2.setStyleSheet(common_stylesheet+"white;") # adding the stylesheet
        self.multiple_column_sort_combobox2.addItems(self.headers) # adding the headers to the combo box loaded from the headers of the data
        
        # button
        self.multiple_column_sort_btn = QPushButton("Multi-Column Sort") # adding a button for single sort triggering
        self.multiple_column_sort_btn.setStyleSheet(common_stylesheet+" orange;") # adding style to button
        
        # time display label
        multiple_sort_time_label = QLabel("Time taken: "+ str(self.multiple_sort_time*100)+" ms") # displaying the time taken to implement the multi level sorting
        multiple_sort_time_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding stylesheet for the time label
        
        # adding the elements to main multi column sorting layout container
        multiple_column_sort_container = QHBoxLayout()
        multiple_column_sort_container.addWidget(multiple_column_sort_label)
        multiple_column_sort_container.addWidget(self.multiple_column_sort_combobox1)
        multiple_column_sort_container.addWidget(self.multiple_column_sort_combobox2)
        multiple_column_sort_container.addWidget(self.multiple_column_sort_btn)
        multiple_column_sort_container.addWidget(multiple_sort_time_label)
        
        # ------------------------------------- Searching functionality -------------------------------------

        # label
        search_column_sort_label = QLabel("Apply searching filter: ") # label text for the sort
        search_column_sort_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding a stylesheet for the label
        search_column_sort_label.setFixedWidth(150) # fixing the width
        
        # input 1 and combobox 1
        self.search_column_input1 = QLineEdit() # adding a text input in UI for search column 1
        self.search_column_input1.setPlaceholderText("Query column 1: ") # setting up a place holder for user guidance
        self.search_column_input1.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 14px;") # setting the stylesheet for the product name input
        self.search_column_input1.setMinimumWidth(100) # setting the minimum width of the product name field
        self.search_column_sort_combobox1 = QComboBox() # adding a combobox to select column 1
        self.search_column_sort_combobox1.setStyleSheet(common_stylesheet+"white;") # adding the stylesheet
        self.search_column_sort_combobox1.addItems(self.headers) # adding the headers to the combo box loaded from the headers of the data
        self.search_column_sort_combobox1.setMinimumWidth(100) # setting the minimum width of the product name field
        
        # input 2 and combobox 2
        self.search_column_input2 = QLineEdit() # adding a text input in UI for search column 2
        self.search_column_input2.setPlaceholderText("Query column 2: ") # setting up a place holder for user guidance
        self.search_column_input2.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 14px;") # setting the stylesheet for the product name input
        self.search_column_input2.setMinimumWidth(100) # setting the minimum width of the product name field
        self.search_column_sort_combobox2 = QComboBox() # adding a combobox to select column 2
        self.search_column_sort_combobox2.setStyleSheet(common_stylesheet+"white;") # adding the stylesheet
        self.search_column_sort_combobox2.addItems(self.headers) # adding the headers to the combo box loaded from the headers of the data
        self.search_column_sort_combobox2.setMinimumWidth(100) # setting the minimum width of the product name field
        
        # adding the objects to search container 1
        search_column_sort_container1=QHBoxLayout()
        search_column_sort_container1.addWidget(search_column_sort_label)
        search_column_sort_container1.addWidget(self.search_column_sort_combobox1)
        search_column_sort_container1.addWidget(self.search_column_input1)
        search_column_sort_container1.addWidget(self.search_column_sort_combobox2)
        search_column_sort_container1.addWidget(self.search_column_input2)
        
        # ------------------------------------- Filter functionality -------------------------------------

        # combo box
        self.filter_combobox = QComboBox() # adding a combobox to apply filters
        self.filter_combobox.addItems(["Contains","Ends with","Starts with"]) # filter content
        
        self.and_checkbox = QCheckBox("AND operation")
        self.and_checkbox.setStyleSheet(common_stylesheet+"lightgrey;")
        self.or_checkbox = QCheckBox("OR operation")
        self.or_checkbox.setStyleSheet(common_stylesheet+"lightgrey;")
        self.not_checkbox = QCheckBox("NOT operations")
        self.not_checkbox.setStyleSheet(common_stylesheet+"lightgrey;")
        
        # push button
        self.search_column_sort_btn = QPushButton("Search") # adding a button for single sort triggering
        self.search_column_sort_btn.setStyleSheet(common_stylesheet+" lightgrey;") # adding style to button
        
        # adding the objects to search container 1
        search_column_sort_container2=QHBoxLayout()
        search_column_sort_container2.addWidget(self.filter_combobox)
        search_column_sort_container2.addWidget(self.and_checkbox)
        search_column_sort_container2.addWidget(self.or_checkbox)
        search_column_sort_container2.addWidget(self.not_checkbox)
        search_column_sort_container2.addWidget(self.search_column_sort_btn)
        
        
        # searching functionality container
        search_column_sort_container = QVBoxLayout()
        search_column_sort_container.addLayout(search_column_sort_container1)
        search_column_sort_container.addLayout(search_column_sort_container2)

        # ------------------------------------- Adding layouts to main layout -------------------------------------
        
        main_layout.addLayout(title_container)
        main_layout.addLayout(scrap_data_container)
        main_layout.addWidget(self.data_table)
        main_layout.addLayout(single_column_sort_container)
        main_layout.addLayout(multiple_column_sort_container)
        main_layout.addLayout(search_column_sort_container)

    def load_data_from_csv(self):
        try:
            if(self.file_name_input.text()!=""):
                file_name = self.file_name_input.text()
                data = ut.load_data(f"{file_name}"+".csv")
                self.headers = data.columns
                self.data_table.setColumnCount(len(self.headers))
                self.data_table.setHorizontalHeaderLabels(self.headers)
                self.data_table.setRowCount(len(data))
                for i in range(len(data)):
                    for j in range(len(data[i])):
                        self.data_table.setItem(i,j,QTableWidgetItem(str(data[i][j])))
            else:
                print("Please enter the file name")
        except Exception as e:
            print("Error occurred: ",e)
            