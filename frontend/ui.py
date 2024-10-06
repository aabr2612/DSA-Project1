import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from frontend import utility as ut
from backend.sorting import sorting_algorithms as sa

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project-1 Scraping and Data sorting")
        
        win_width = 800
        win_height = 690
        screen = QApplication.primaryScreen()
        init_x_position = (screen.geometry().width() - win_width) // 2
        init_y_position = 30
        self.setGeometry(init_x_position, init_y_position, win_width, win_height)
        
        self.setMinimumSize(win_width, win_height)
        self.setStyleSheet("background-color: royalblue; font-family: Times New Roman;")
        self.initUI()
    
    def initUI(self):
        sorting_algorithms_arr = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Counting Sort", "Radix Sort", "Bucket Sort", "Genome Sort", "Even Odd Sort", "Heap Sort"]
        self.data = None
        self.single_sort_time = 0
        self.headers = ["A", "B", "C", "D", "E", "F", "G"]
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        title_label = QLabel("Project1 - Sorting Algorithms", self)
        title_label.setFixedHeight(80)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 30px")
        
        title_container = QVBoxLayout()
        title_container.addWidget(title_label)

        common_stylesheet = "color:black; font-weight:bold; font-size: 14px; background-color: white;"

        self.file_name_input = QLineEdit()
        self.file_name_input.setPlaceholderText("Enter file name to load data: ")
        self.file_name_input.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 14px;")
        self.file_name_input.setMinimumWidth(400)

        self.load_from_csv_btn = QPushButton("Load data from CSV")
        self.load_from_csv_btn.setStyleSheet(common_stylesheet + " lightgrey;")
        self.load_from_csv_btn.clicked.connect(self.load_data_from_csv)
        
        scrap_data_container = QVBoxLayout()
        
        load_data_container = QHBoxLayout()
        load_data_container.addWidget(self.file_name_input)
        load_data_container.addWidget(self.load_from_csv_btn)
        
        scrap_data_container.addLayout(load_data_container)

        self.data_table = QTableWidget()
        self.data_table.setColumnCount(7)
        self.data_table.setHorizontalHeaderLabels(self.headers)
        self.data_table.setStyleSheet("color: black; background-color: lightgray; font-size: 11px;")
        
        table_header = self.data_table.horizontalHeader()
        table_header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.algorithm_combobox = QComboBox()
        self.algorithm_combobox.setStyleSheet(common_stylesheet + "white;")
        self.algorithm_combobox.addItems(sorting_algorithms_arr)

        single_column_sort_label = QLabel("Single Column Sort: ")
        single_column_sort_label.setFixedWidth(130)
        single_column_sort_label.setStyleSheet(common_stylesheet + "lightgrey;")
        self.single_column_sort_combobox = QComboBox()
        self.single_column_sort_combobox.setStyleSheet(common_stylesheet + "white;")
        self.single_column_sort_combobox.addItems(self.headers)
        self.single_column_sort_btn = QPushButton("Sort")
        self.single_column_sort_btn.setStyleSheet(common_stylesheet + " orange;")
        self.single_column_sort_btn.clicked.connect(self.sort_data)

        self.single_sort_time_label = QLabel("Time taken: " + str(self.single_sort_time * 100) + " ms")
        self.single_sort_time_label.setStyleSheet(common_stylesheet + "lightgrey;")
        
        single_column_sort_container = QHBoxLayout()
        single_column_sort_container.addWidget(single_column_sort_label)
        single_column_sort_container.addWidget(self.single_column_sort_combobox)
        single_column_sort_container.addWidget(self.single_column_sort_btn)
        single_column_sort_container.addWidget(self.single_sort_time_label)
        
        search_column_sort_label = QLabel("Apply searching filter: ")
        search_column_sort_label.setStyleSheet(common_stylesheet + "lightgrey;")
        search_column_sort_label.setFixedWidth(150)
        
        self.filter_combobox = QComboBox()
        self.filter_combobox.addItems(["Contains", "Ends with", "Starts with"])
        self.filter_combobox.setStyleSheet("background-color:white;")

        self.search_column_combobox = QComboBox()
        self.search_column_combobox.setStyleSheet(common_stylesheet + "white;")
        self.search_column_combobox.addItems(self.headers)
        self.search_column_combobox.setFixedWidth(200)
        self.not_checkbox = QCheckBox("NOT")
        self.not_checkbox.setFixedWidth(50)
        self.not_checkbox.setStyleSheet(common_stylesheet + "lightgrey;")
        self.search_column_input1 = QLineEdit()
        self.search_column_input1.setPlaceholderText("Query column 1: ")
        self.search_column_input1.setStyleSheet("color: black; background-color: white; font-weight: bold; font-size: 14px;")
        self.and_checkbox = QCheckBox("AND")
        self.and_checkbox.setStyleSheet(common_stylesheet + "lightgrey;")
        self.and_checkbox.setFixedWidth(50)
        search_column_container1 = QHBoxLayout()
        search_column_container1.addWidget(search_column_sort_label)
        search_column_container1.addWidget(self.filter_combobox)
        search_column_container1.addWidget(self.not_checkbox)
        search_column_container1.addWidget(self.search_column_input1)
        
        self.search_column_btn = QPushButton("Search")
        self.search_column_btn.setStyleSheet(common_stylesheet + " lightgrey;")
        self.search_column_btn.clicked.connect(self.apply_filter)

        
        search_column_container2 = QHBoxLayout()
        search_column_container2.addWidget(self.search_column_combobox)
        search_column_container2.addWidget(self.search_column_btn)
        
        search_column_sort_container = QVBoxLayout()
        search_column_sort_container.addLayout(search_column_container1)
        search_column_sort_container.addLayout(search_column_container2)

        main_layout.addLayout(title_container)
        main_layout.addLayout(scrap_data_container)
        main_layout.addWidget(self.data_table)
        main_layout.addWidget(self.algorithm_combobox)
        main_layout.addLayout(single_column_sort_container)
        main_layout.addLayout(search_column_sort_container)

    def load_data_from_csv(self):
        try:
            if self.file_name_input.text() != "":
                file_name = self.file_name_input.text() + ".csv"
                self.data = ut.load_data(file_name)
            
                if self.data is not None:
                    self.headers = list(self.data.columns)
                    self.data_table.setColumnCount(len(self.headers))
                    self.single_column_sort_combobox.clear()
                    self.search_column_combobox.clear()
                    self.single_column_sort_combobox.addItems(self.headers)
                    self.search_column_combobox.addItems(self.headers)

                    self.data_table.setHorizontalHeaderLabels(self.headers)
                    self.data_table.setRowCount(len(self.data))
                    
                    for i in range(len(self.data)):
                        for j in range(len(self.data.columns)):
                            self.data_table.setItem(i, j, QTableWidgetItem(str(self.data.iat[i, j])))
                else:
                    print("No data loaded.")
            else:
                print("Please enter the file name.")
        except Exception as e:
            print("Error occurred: ", e)
    
    def sort_data(self):
        sorting_algorithm = self.algorithm_combobox.currentText()
        a = self.single_column_sort_combobox.currentText()
        print(a)
        
        start_time = time.time()
        if sorting_algorithm == "Bubble Sort":
            sa.bubbleSort(self.data, a)
        elif sorting_algorithm == "Selection Sort":
            sa.selectionSort(self.data, a)
        elif sorting_algorithm == "Insertion Sort":
            sa.insertionSort(self.data, a)
        elif sorting_algorithm == "Merge Sort":
            self.data = sa.mergeSort(self.data, a)
        elif sorting_algorithm == "Quick Sort":
            self.data = sa.quickSort(self.data, a)
        elif sorting_algorithm == "Counting Sort":
            sa.countingSort(self.data, a)
        elif sorting_algorithm == "Radix Sort":
            sa.radixSort(self.data, a)
        elif sorting_algorithm == "Bucket Sort":
            sa.bucketSort(self.data, a)
        elif sorting_algorithm == "Genome Sort":
            sa.gnomeSort(self.data, a)
        elif sorting_algorithm == "Heap Sort":
            sa.heapSort(self.data, a)
        elif sorting_algorithm == "EvenOdd Sort":
            sa.evenOddSort(self.data, a)
        end_time = time.time()
        self.single_sort_time = (end_time - start_time) * 1000
        
        self.single_sort_time_label.setText("Time taken: " + str(int(self.single_sort_time)) + " ms")
        
        self.load_data_to_table()
    
    def load_data_to_table(self):
        self.data_table.setRowCount(len(self.data))
        for i in range(len(self.data)):
            for j in range(len(self.data.columns)):
                self.data_table.setItem(i, j, QTableWidgetItem(str(self.data.iat[i, j])))
    def apply_filter(self):
        try:
            if self.data is not None:
                filter_type = self.filter_combobox.currentText()
                column_name = self.search_column_combobox.currentText()
                query = self.search_column_input1.text()
                
                if query.strip() == "":
                    return
                
                filtered_data = self.data.copy()
                
                if filter_type == "Contains":
                    filtered_data = filtered_data[filtered_data[column_name].str.contains(query, na=False)]
                elif filter_type == "Ends with":
                    filtered_data = filtered_data[filtered_data[column_name].str.endswith(query, na=False)]
                elif filter_type == "Starts with":
                    filtered_data = filtered_data[filtered_data[column_name].str.startswith(query, na=False)]
                
                if self.not_checkbox.isChecked():
                    filtered_data = self.data[~self.data[column_name].isin(filtered_data[column_name])]

                self.data_table.setRowCount(len(filtered_data))
                for i in range(len(filtered_data)):
                    for j in range(len(filtered_data.columns)):
                        self.data_table.setItem(i, j, QTableWidgetItem(str(filtered_data.iat[i, j])))
            else:
                print("No data to filter.")
        except Exception as e:
            print("Error occurred during filtering: ", e)
