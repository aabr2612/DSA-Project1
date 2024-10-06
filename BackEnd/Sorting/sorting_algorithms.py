import pandas as pd

# bubble sort
def bubbleSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    for i in range(len(data) - 1):
        isSwapped = False
        
        for j in range(len(data) - i - 1):
            if data[column].iloc[j] > data[column].iloc[j + 1]:
                data.iloc[[j, j + 1]] = data.iloc[[j + 1, j]]
                isSwapped = True
        if not isSwapped:
            break
        
    return data

# selection sort
def selectionSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    for i in range(len(data) - 1): 
        minIdx = i
        
        for j in range(i + 1, len(data)):
            if data[column].iloc[minIdx] > data[column].iloc[j]:
                minIdx = j
                
        if minIdx != i:
            data.iloc[[i, minIdx]] = data.iloc[[minIdx, i]]
        
    return data

# insertion sort
def insertionSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    for i in range(1, len(data)):
        key_row = data.iloc[i].copy()
        j = i - 1
        
        while j >= 0 and key_row[column] < data.iloc[j][column]:  
            data.iloc[j + 1] = data.iloc[j]
            j = j - 1
            
        data.iloc[j + 1] = key_row
        
    return data

# merge sort
def mergeSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left_half_df = mergeSort(data.iloc[:mid], column)
    right_half_df = mergeSort(data.iloc[mid:], column)

    return merge(left_half_df, right_half_df, column)

def merge(left, right, column_name):
    sorted_data = pd.DataFrame(columns=left.columns)
    i = j = 0
    while i < len(left) and j < len(right):
        if left[column_name].iloc[i] <= right[column_name].iloc[j]:
            sorted_data = pd.concat([sorted_data, left.iloc[[i]]], ignore_index=True)
            i += 1
        else:
            sorted_data = pd.concat([sorted_data, right.iloc[[j]]], ignore_index=True)
            j += 1

    while i < len(left):
        sorted_data = pd.concat([sorted_data, left.iloc[[i]]], ignore_index=True)
        i += 1

    while j < len(right):
        sorted_data = pd.concat([sorted_data, right.iloc[[j]]], ignore_index=True)
        j += 1

    return sorted_data

# quick sort
def quickSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    if len(data) <= 1:
        return data
    
    pivot = data[column].iloc[len(data) // 2]
    left = data[data[column] < pivot]
    middle = data[data[column] == pivot]
    right = data[data[column] > pivot]

    return pd.concat([quickSort(left, column), middle, quickSort(right, column)], ignore_index=True)

# counting sort
def countingSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    max_value = int(data[column].max())
    count = [0] * (max_value + 1)
    
    for value in data[column]:
        count[value] += 1
    sorted_index = 0
    
    for value in range(max_value + 1):
        while count[value] > 0:
            rows = data[data[column] == value]
            data.iloc[sorted_index:sorted_index + len(rows)] = rows.values
            sorted_index += len(rows)
            count[value] -= 1
    
    return data

# radix sort
def counting_sort_radix(data: pd.DataFrame, column: str, exp) -> pd.DataFrame:
    n = len(data)
    output = pd.DataFrame(columns=data.columns, index=range(n))
    count = [0] * 10
    
    for i in range(n):
        index = data[column].iloc[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = data[column].iloc[i] // exp
        output.iloc[count[index % 10] - 1] = data.iloc[i]
        count[index % 10] -= 1

    return output

def radixSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    if column not in data.columns or not pd.api.types.is_numeric_dtype(data[column]):
        return

    max_value = int(data[column].max())

    exp = 1
    while max_value // exp > 0:
        data = counting_sort_radix(data, column, exp)
        exp *= 10

    return data

# bucket sort
def bucketSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    if column not in data.columns or not pd.api.types.is_numeric_dtype(data[column]):
        return 

    max_value = int(data[column].max())
    min_value = int(data[column].min())
    bucket_range = max_value - min_value + 1
    bucket_count = bucket_range // 10 + 1
    buckets = [[] for _ in range(bucket_count)]

    for idx, value in data[column].iteritems():
        bucket_index = (value - min_value) // 10
        buckets[bucket_index].append(data.iloc[idx])

    sorted_index = 0
    
    for bucket in buckets:
        if bucket:
            bucket_df = pd.DataFrame(bucket)
            bucket_df = bucket_df.sort_values(by=column)
            data.iloc[sorted_index:sorted_index + len(bucket_df)] = bucket_df.values
            sorted_index += len(bucket_df)
                
    return data

# gnome sort
def gnomeSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    index = 0
    n = len(data)

    while index < n:
        if index > 0 and data[column].iloc[index] < data[column].iloc[index - 1]:
            data.iloc[[index, index - 1]] = data.iloc[[index - 1, index]]
            index -= 1
        else:
            index += 1

    return data.reset_index(drop=True)

# heap sort
def heapify(data: pd.DataFrame, n: int, i: int, column: str):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and data[column].iloc[left] > data[column].iloc[largest]:
        largest = left

    if right < n and data[column].iloc[right] > data[column].iloc[largest]:
        largest = right

    if largest != i:
        data.iloc[[i, largest]] = data.iloc[[largest, i]]
        heapify(data, n, largest, column)

def heapSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    n = len(data)

    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i, column)

    for i in range(n - 1, 0, -1):
        data.iloc[[i, 0]] = data.iloc[[0, i]]
        heapify(data, i, 0, column)

    return data.reset_index(drop=True)

# even-odd sort
def evenOddSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    n = len(data)
    sorted = False

    while not sorted:
        sorted = True

        for i in range(1, n, 2):
            if data[column].iloc[i] < data[column].iloc[i - 1]:
                data.iloc[[i, i - 1]] = data.iloc[[i - 1, i]]
                sorted = False

        for i in range(0, n - 1, 2):
            if data[column].iloc[i] > data[column].iloc[i + 1]:
                data.iloc[[i, i + 1]] = data.iloc[[i + 1, i]]
                sorted = False

    return data