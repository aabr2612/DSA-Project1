
# DSA Project 1

This is my pre-mid Data Structures and Algorithms (DSA) project, implemented in Python. It demonstrates the use of various sorting algorithms, searching techniques, and web scraping functionalities through a PyQt5-based GUI.

## Features

### 1. **Web Scraping**
- Fetch product data by entering a search term (uses Selenium and Beautiful Soup).
- Supports **Start**, **Pause**, **Resume**, and **Stop** actions during the scraping process.
- Automatically saves scraped data to a CSV file with the same name as the product name entered.
- Provides an option to reload the CSV data into the frontend GUI for further operations.
- Includes error handling for scenarios like invalid product names or network issues.

### 2. **Sorting Algorithms**
The project includes 10 sorting algorithms to organize data based on user-selected criteria:
- **Bubble Sort**: Repeatedly compares adjacent elements and swaps them if they are in the wrong order. Simple but inefficient for large datasets.
- **Insertion Sort**: Builds the sorted array one item at a time by placing elements in their correct position.
- **Selection Sort**: Repeatedly selects the smallest element from the unsorted portion and moves it to the sorted portion.
- **Merge Sort**: A divide-and-conquer algorithm that splits data into smaller arrays, sorts them, and merges them back together.
- **Quick Sort**: Another divide-and-conquer method that selects a pivot, partitions the array, and recursively sorts partitions.
- **Counting Sort**: A non-comparison-based algorithm suitable for integers within a specific range.
- **Bucket Sort**: Distributes elements into buckets, sorts them individually, and combines the results.
- **Radix Sort**: Processes elements digit by digit, starting from the least significant digit.
- **Heap Sort**: Builds a max heap to sort the elements by repeatedly extracting the maximum.
- **Genome Sort**: A genetic algorithm-inspired approach to sorting.

Sorting features include:
- Algorithm selection via a dropdown menu.
- Column selection for sorting.
- Real-time performance analysis displaying the time taken for each sort.

### 3. **Simple Searching**
- Apply filters to search for specific data within a column:
  - **Contains**: Searches for rows containing the specified substring.
  - **Starts With**: Filters rows where data begins with the substring.
  - **Ends With**: Filters rows where data ends with the substring.
- Supports **NOT Operation**: Excludes rows matching the query condition.
- Includes error handling for invalid search inputs or empty columns.

### 4. **Additional Functionalities**
- **Message Box**: Provides real-time updates, such as:
  - Successful actions (e.g., data loaded, sort completed).
  - Errors (e.g., invalid file path, unsupported operation).
  - Status of ongoing operations like scraping, sorting, or searching.
- **Error Handling**: Robust error handling across all major features to ensure smooth user experience.

## Folder Structure

```
Project Directory
│
├── backend
│   ├── data                  # Stores scraped or sample CSV files
│   ├── sorting
│   │   ├── sorting_algorithms.py # Sorting algorithms implementations
│   └── scrap.py              # Web scraping logic
│
├── frontend
│   ├── ui.py                 # PyQt5 GUI design
│   └── utility.py            # Utility functions
│
├── main.py                   # Entry point for the application
├── README.md                 # Documentation
├── requirements.txt          # List of required Python libraries
└── ...
```

## Technologies and Libraries Used

- **Programming Language**: Python (3.x)
- **GUI Framework**: PyQt5
- **Web Scraping**:
  - Selenium
  - Beautiful Soup
- **Data Handling**: Pandas
- **Concurrency**: Threading
- **Others**:
  - OS module
  - Time module
  - ChromeDriver (for Selenium)

## Prerequisites

Before running the project, ensure you have the following installed on your system:
1. Python 3.x
2. Required Python packages:
   - `PyQt5`
   - `selenium`
   - `beautifulsoup4`
   - `pandas`
3. ChromeDriver (compatible with your Google Chrome version).

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aabr2612/DSA-Project1
   ```
2. Navigate to the project directory:
   ```bash
   cd DSA-Project1
   ```
3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Download ChromeDriver:
   - [Download ChromeDriver](https://sites.google.com/chromium.org/driver/).
   - Place the `chromedriver` executable in a directory included in your system's `PATH` or provide its path in the code.

## How to Run

1. Open a terminal or command prompt and navigate to the project directory.
2. Run the main Python file:
   ```bash
   python main.py
   ```
3. The GUI will launch, allowing you to use the scraping, sorting, and searching functionalities.

## Conclusion

This project integrates web scraping, data handling, and sorting algorithms through a simple GUI, providing hands-on experience with these concepts and algorithms. It serves as a valuable educational tool for learning data processing and algorithm implementation.