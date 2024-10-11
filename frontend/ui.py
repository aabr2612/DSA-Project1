import time
import pandas as pd
from frontend import utility as ut
from backend.sorting import sorting_algorithms as sa
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from backend.scrap import ScraperThread

# a main class inheriting from the QMainWindow so that it can access element
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
        self.scraper_thread = None
        sorting_algorithms = ["Bubble Sort","Selection Sort","Insertion Sort","Merge Sort","Quick Sort","Genome Sort","Heap Sort","Counting Sort","Radix Sort","Bucket Sort","EvenOdd Sort"]
        
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
        self.start_scrap_btn.clicked.connect(self.start_scraping)
        
        # pause button
        self.pause_scrap_btn = QPushButton("Pause")
        self.pause_scrap_btn.setStyleSheet(common_stylesheet+" yellow;")
        self.pause_scrap_btn.clicked.connect(self.pause_scraping)

        # resume button
        self.resume_scrap_btn = QPushButton("Resume")
        self.resume_scrap_btn.setStyleSheet(common_stylesheet+" blue;")
        self.resume_scrap_btn.clicked.connect(self.resume_scraping)
        
        # stop button
        self.stop_scrap_btn = QPushButton("Stop")
        self.stop_scrap_btn.setStyleSheet(common_stylesheet+" red;")
        self.stop_scrap_btn.clicked.connect(self.stop_scraping)
        
        # ------------------------------------- Progress bar for scraping task -------------------------------------
        
        self.scrap_progress = QProgressBar() # a new progress bar object
        self.scrap_progress.setValue(self.progress) # by default value of progress bar
        self.scrap_progress.setTextVisible(True) # adding a bool variable to make it visible
        self.scrap_progress.setStyleSheet("color: white;") # adding style sheet
        
        # ------------------------------------- Button and input for loading data -------------------------------------

        self.file_name_input = QLineEdit() # adding a text input in UI
        self.file_name_input.setPlaceholderText("Enter file name to load data: ") # setting up a place holder for user guidance
        self.file_name_input.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 14px;") # setting the stylesheet for the product name input
        self.file_name_input.setMinimumWidth(400) # setting the minimum width of the product name field
        
        # start button
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
        scrap_data_container.addWidget(self.scrap_progress)
        scrap_data_container.addLayout(load_data_container)

        # ------------------------------------- Adding the data table to the UI -------------------------------------
        
        self.data_table = QTableWidget() # a new table layout
        self.data_table.setColumnCount(7) # setting the column count for the table
        self.data_table.setHorizontalHeaderLabels(self.headers) # adding the table headers to the table
        self.data_table.setStyleSheet("color: black; background-color: lightgray; font-size: 11px;") # adding the stylesheet
        
        # setting the column width to automatically adjust equally
        table_header = self.data_table.horizontalHeader()
        table_header.setSectionResizeMode(QHeaderView.Stretch)
        
        # ------------------------------------- Algorithms Combobox -------------------------------------

        self.algorithm_combobox = QComboBox() # adding a combobox to select a column
        self.algorithm_combobox.setStyleSheet(common_stylesheet+"white;") # adding stylesheet
        self.algorithm_combobox.addItems(sorting_algorithms) # adding the headers to the combo box loaded from the headers of the data
        
        # ------------------------------------- Single column sort layout -------------------------------------
        
        self.sorting_column = QComboBox() # adding a combobox to select a column
        self.sorting_column.setStyleSheet(common_stylesheet+"white;") # adding stylesheet
        self.sorting_column.addItems(self.headers) # adding the headers to the combo box loaded from the headers of the data
        single_column_sort_label = QLabel("Single Column Sort: ") # label text for the sort
        single_column_sort_label.setFixedWidth(130)
        single_column_sort_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding a stylesheet for the label
        self.single_column_sort_btn = QPushButton("Sort") # adding a button for single sort triggering
        self.single_column_sort_btn.setStyleSheet(common_stylesheet+" orange;") # adding style to button
        self.single_column_sort_btn.clicked.connect(self.sort_data)
        self.single_sort_time_label = QLabel("Time taken: "+ str(self.single_sort_time*100)+" ms") # displaying the sortgng time
        self.single_sort_time_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding stylesheet
        
        # adding the elements to main single column sorting layout container
        single_column_sort_container = QHBoxLayout()
        single_column_sort_container.addWidget(single_column_sort_label)
        single_column_sort_container.addWidget(self.sorting_column)
        single_column_sort_container.addWidget(self.single_column_sort_btn)
        single_column_sort_container.addWidget(self.single_sort_time_label)
        
        # ------------------------------------- Searching functionality -------------------------------------

        # label
        search_column_sort_label = QLabel("Apply searching filter: ") # label text for the sort
        search_column_sort_label.setStyleSheet(common_stylesheet+"lightgrey;") # adding a stylesheet for the label
        search_column_sort_label.setFixedWidth(150) # fixing the width
        
        # input and combobox
        self.search_column_input = QLineEdit() # adding a text input in UI for search column
        self.search_column_input.setPlaceholderText("Query column 1: ") # setting up a place holder for user guidance
        self.search_column_input.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 14px;") # setting the stylesheet for the product name input
        self.search_column_input.setMinimumWidth(100) # setting the minimum width of the product name field
        self.search_column_combobox = QComboBox() # adding a combobox to select column
        self.search_column_combobox.setStyleSheet(common_stylesheet+"white;") # adding the stylesheet
        self.search_column_combobox.addItems(self.headers) # adding the headers to the combo box loaded from the headers of the data
        self.search_column_combobox.setMinimumWidth(100) # setting the minimum width of the product name field
        
        # adding the objects to search container 1
        search_column_container1=QHBoxLayout()
        search_column_container1.addWidget(search_column_sort_label)
        search_column_container1.addWidget(self.search_column_combobox)
        search_column_container1.addWidget(self.search_column_input)
        
        # ------------------------------------- Filter functionality -------------------------------------

        # combo box
        self.filter_combobox = QComboBox() # adding a combobox to apply filters
        self.filter_combobox.addItems(["Contains","Ends with","Starts with"]) # filter content

        self.not_checkbox = QCheckBox("NOT operations")
        self.not_checkbox.setStyleSheet(common_stylesheet+"lightgrey;")
        
        # push button
        self.search_column_sort_btn = QPushButton("Search") # adding a button for single sort triggering
        self.search_column_sort_btn.setStyleSheet(common_stylesheet+" lightgrey;") # adding style to button
        self.search_column_sort_btn.clicked.connect(self.apply_filter)
        
        # adding the objects to search container 1
        search_column_container2=QHBoxLayout()
        search_column_container2.addWidget(self.filter_combobox)
        search_column_container2.addWidget(self.not_checkbox)
        search_column_container2.addWidget(self.search_column_sort_btn)
        
        # searching functionality container
        search_column_container = QVBoxLayout()
        search_column_container.addLayout(search_column_container1)
        search_column_container.addLayout(search_column_container2)

        # ------------------------------------- Message Box -------------------------------------
        message_label = QLabel("Message:")
        message_label.setStyleSheet(common_stylesheet + "lightgrey;")
        message_label.setFixedWidth(100)
        self.message_box = QLabel("")
        self.message_box.setStyleSheet(common_stylesheet + "lightgrey;")
        message_container = QHBoxLayout()
        message_container.addWidget(message_label)
        message_container.addWidget(self.message_box)
        
        # ------------------------------------- Adding layouts to main layout -------------------------------------
        
        main_layout.addLayout(title_container)
        main_layout.addLayout(scrap_data_container)
        main_layout.addWidget(self.data_table)
        main_layout.addWidget(self.algorithm_combobox)
        main_layout.addLayout(single_column_sort_container)
        main_layout.addLayout(search_column_container)
        main_layout.addLayout(message_container)

    def start_scraping(self):
        try:
            if self.data_scrap_product.text()!="":
                product_name=self.data_scrap_product.text()
                self.scraper_thread = ScraperThread(product_name=product_name, total_pages=2)
                self.scraper_thread.progress_signal.connect(self.update_progress)
                self.scraper_thread.start()
                self.start_scrap_btn.setEnabled(False)
                self.pause_scrap_btn.setEnabled(True)
                self.resume_scrap_btn.setEnabled(False)
                self.stop_scrap_btn.setEnabled(True)
                self.message_box.setText(f"Scraping data for the product: {product_name}")
            else:
                self.message_box.setText(f"Enter a product name to start scraping!")
        except Exception as e:
            self.message_box.setText("Error while scraping: "+str(e))

    def pause_scraping(self):
        try:
            if self.scraper_thread:
                self.scraper_thread.pause()
                self.pause_scrap_btn.setEnabled(False)
                self.resume_scrap_btn.setEnabled(True)
                self.message_box.setText(f"Scraping paused")
        except Exception as e:
            self.message_box.setText("Error while scraping: "+str(e))

    def resume_scraping(self):
        try:
            if self.scraper_thread:
                self.scraper_thread.resume()
                self.pause_scrap_btn.setEnabled(True)
                self.resume_scrap_btn.setEnabled(False)
                self.message_box.setText(f"Scraping resumed...")
        except Exception as e:
            self.message_box.setText("Error while scraping: "+str(e))

    def stop_scraping(self):
        try:
            if self.scraper_thread:
                self.scraper_thread.stop()
                self.pause_scrap_btn.setEnabled(False)
                self.resume_scrap_btn.setEnabled(False)
                self.stop_scrap_btn.setEnabled(False)
                self.start_scrap_btn.setEnabled(True)
                self.scraper_thread = None
                self.message_box.setText(f"Scraping stopped!")
        except Exception as e:
            self.message_box.setText("Error while scraping: "+str(e))

    @pyqtSlot(int)
    def update_progress(self, progress):
        try:
            self.scrap_progress.setValue(progress)
            if progress >= 100:
                self.start_scrap_btn.setEnabled(True)
                self.pause_scrap_btn.setEnabled(False)
                self.resume_scrap_btn.setEnabled(False)
                self.stop_scrap_btn.setEnabled(False)
                self.scraper_thread = None
        except Exception as e:
            self.message_box.setText("Error occurred: "+str(e))
        
    def load_data_from_csv(self):
        try:
            if self.file_name_input.text() != "":
                file_name = self.file_name_input.text() + ".csv"
                self.data = ut.load_data(file_name)
            
                if self.data is not None:
                    self.headers = list(self.data.columns)
                    self.data_table.setColumnCount(len(self.headers))
                    self.sorting_column.clear()
                    self.search_column_combobox.clear()
                    self.sorting_column.addItems(self.headers)
                    self.search_column_combobox.addItems(self.headers)

                    self.data_table.setHorizontalHeaderLabels(self.headers)
                    self.data_table.setRowCount(len(self.data))
                    
                    for i in range(len(self.data)):
                        for j in range(len(self.data.columns)):
                            self.data_table.setItem(i, j, QTableWidgetItem(str(self.data.iat[i, j])))
                    self.message_box.setText("Data loaded.")
                else:
                    self.message_box.setText("No data loaded.")
            else:
                self.message_box.setText("Please enter the file name.")
        except Exception as e:
            self.message_box.setText("Error occurred: "+str(e))
    
    def sort_data(self):
        try:
            sorting_algorithm = self.algorithm_combobox.currentText()
            a = self.sorting_column.currentText()
            
            start_time = time.time()
            if sorting_algorithm == "Bubble Sort":
                self.data =sa.bubbleSort(self.data, a)
            elif sorting_algorithm == "Selection Sort":
                self.data =sa.selectionSort(self.data, a)
            elif sorting_algorithm == "Insertion Sort":
                self.data =sa.insertionSort(self.data, a)
            elif sorting_algorithm == "Merge Sort":
                self.data = sa.mergeSort(self.data, a)
            elif sorting_algorithm == "Quick Sort":
                self.data = sa.quickSort(self.data, a)
            elif sorting_algorithm == "Genome Sort":
                self.data =sa.gnomeSort(self.data, a)
            elif sorting_algorithm == "Heap Sort":
                self.data =sa.heapSort(self.data, a)
            elif sorting_algorithm == "Counting Sort":
                self.data =sa.countingSort(self.data, a)
            elif sorting_algorithm == "Radix Sort":
                self.data = sa.radixSort(self.data, a)
            elif sorting_algorithm == "Bucket Sort":
                self.data =sa.bucketSort(self.data, a)
            elif sorting_algorithm == "EvenOdd Sort":
                self.data =sa.oddEvenSort(self.data, a)

            end_time = time.time()
            self.single_sort_time = (end_time - start_time) * 1000
            
            self.single_sort_time_label.setText("Time taken: " + str(int(self.single_sort_time)) + " ms")
            self.message_box.setText("Data sorted successfully using " + a)
            
            self.load_data_to_table()
        except Exception as e:
            self.message_box.setText("Error occurred in sorting: "+str(e))
    
    def load_data_to_table(self):
        try:
            self.data_table.setRowCount(len(self.data))
            for i in range(len(self.data)):
                for j in range(len(self.data.columns)):
                    self.data_table.setItem(i, j, QTableWidgetItem(str(self.data.iat[i, j])))
        except Exception as e:
            self.message_box.setText("Error occurred loading data to table: "+str(e))
                
    def apply_filter(self):
        try:
            if self.data is not None:
                filter_type = self.filter_combobox.currentText()
                column_name = self.search_column_combobox.currentText()
                query = self.search_column_input.text()

                if query.strip() == "":
                    self.data_table.setRowCount(len(self.data))
                    for i in range(len(self.data)):
                        for j in range(len(self.data.columns)):
                            self.data_table.setItem(i, j, QTableWidgetItem(str(self.data.iat[i, j])))
                    return

                filtered_data = self.data.copy()

                if pd.api.types.is_string_dtype(self.data[column_name]):
                    query = query.lower()
                    if filter_type == "Contains":
                        filtered_data = filtered_data[filtered_data[column_name].str.contains(query, na=False, case=False)]
                    elif filter_type == "Ends with":
                        filtered_data = filtered_data[filtered_data[column_name].str.endswith(query, na=False, case=False)]
                    elif filter_type == "Starts with":
                        filtered_data = filtered_data[filtered_data[column_name].str.startswith(query, na=False, case=False)]

                elif pd.api.types.is_numeric_dtype(self.data[column_name]):
                    try:
                        query_value = float(query)
                        if filter_type == "Greater than":
                            filtered_data = filtered_data[filtered_data[column_name] > query_value]
                        elif filter_type == "Less than":
                            filtered_data = filtered_data[filtered_data[column_name] < query_value]
                        elif filter_type == "Equals":
                            filtered_data = filtered_data[filtered_data[column_name] == query_value]
                    except ValueError:
                        self.message_box.setText("Invalid numeric input.")
                        return

                else:
                    self.message_box.setText(f"Filtering not supported for column type: {self.data[column_name].dtype}")
                    return

                if self.not_checkbox.isChecked():
                    filtered_data = self.data[~self.data[column_name].isin(filtered_data[column_name])]

                self.data_table.setRowCount(len(filtered_data))
                for i in range(len(filtered_data)):
                    for j in range(len(filtered_data.columns)):
                        self.data_table.setItem(i, j, QTableWidgetItem(str(filtered_data.iat[i, j])))
            else:
                self.message_box.setText("No data to filter.")
        except Exception as e:
            self.message_box.setText("Error occurred while filtering: " + str(e))