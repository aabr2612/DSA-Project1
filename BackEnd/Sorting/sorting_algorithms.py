import pandas as pd

def bubbleSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    try:
        for i in range(len(data) - 1):
            isSwapped = False
            
            for j in range(len(data) - i - 1):
                if data[column].iloc[j] > data[column].iloc[j + 1]:
                    data.iloc[[j, j + 1]] = data.iloc[[j + 1, j]]
                    isSwapped = True
            if not isSwapped:
                break
        return data
    except Exception as e:
        print(f"Error in bubbleSort: {e}")
        return data

def selectionSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    try:
        for i in range(len(data) - 1): 
            minIdx = i
            
            for j in range(i + 1, len(data)):
                if data[column].iloc[minIdx] > data[column].iloc[j]:
                    minIdx = j
                    
            if minIdx != i:
                data.iloc[[i, minIdx]] = data.iloc[[minIdx, i]]
        return data
    except Exception as e:
        print(f"Error in selectionSort: {e}")
        return data

def insertionSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    try:
        for i in range(1, len(data)):
            key_row = data.iloc[i].copy()
            j = i - 1
            
            while j >= 0 and key_row[column] < data.iloc[j][column]:  
                data.iloc[j + 1] = data.iloc[j]
                j = j - 1
                
            data.iloc[j + 1] = key_row
        return data
    except Exception as e:
        print(f"Error in insertionSort: {e}")
        return data

def mergeSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    try:
        if len(data) <= 1:
            return data

        mid = len(data) // 2
        left_half_df = mergeSort(data.iloc[:mid], column)
        right_half_df = mergeSort(data.iloc[mid:], column)

        return merge(left_half_df, right_half_df, column)
    except Exception as e:
        print(f"Error in mergeSort: {e}")
        return data

def merge(left, right, column_name):
    try:
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
    except Exception as e:
        print(f"Error in merge: {e}")
        return left.append(right).reset_index(drop=True)

def quickSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    try:
        if len(data) <= 1:
            return data
        
        pivot = data[column].iloc[len(data) // 2]
        left = data[data[column] < pivot]
        middle = data[data[column] == pivot]
        right = data[data[column] > pivot]

        return pd.concat([quickSort(left, column), middle, quickSort(right, column)], ignore_index=True)
    except Exception as e:
        print(f"Error in quickSort: {e}")
        return data

def heapify(data: pd.DataFrame, n: int, i: int, column: str):
    try:
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
    except Exception as e:
        print(f"Error in heapify: {e}")

def heapSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    try:
        n = len(data)

        for i in range(n // 2 - 1, -1, -1):
            heapify(data, n, i, column)

        for i in range(n - 1, 0, -1):
            data.iloc[[i, 0]] = data.iloc[[0, i]]
            heapify(data, i, 0, column)

        return data.reset_index(drop=True)
    except Exception as e:
        print(f"Error in heapSort: {e}")
        return data
    
def gnomeSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    try:
        index = 0
        n = len(data)

        while index < n:
            if index > 0 and data[column].iloc[index] < data[column].iloc[index - 1]:
                data.iloc[[index, index - 1]] = data.iloc[[index - 1, index]]
                index -= 1
            else:
                index += 1

        return data.reset_index(drop=True)
    except Exception as e:
        print(f"Error in gnomeSort: {e}")
        return data

def countingSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    try:
        if column not in data.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
        
        if not pd.api.types.is_integer_dtype(data[column]):
            raise TypeError(f"Column '{column}' must be of integer type.")
        
        max_value = data[column].max()
        count = [0] * (max_value + 1)

        for value in data[column]:
            count[value] += 1

        for i in range(1, len(count)):
            count[i] += count[i - 1]

        sorted_data = pd.DataFrame(index=data.index, columns=data.columns)

        for i in range(len(data) - 1, -1, -1):
            value = data[column].iloc[i]
            sorted_index = count[value] - 1
            sorted_data.iloc[sorted_index] = data.iloc[i]
            count[value] -= 1

        for col in data.columns:
            sorted_data[col] = sorted_data[col].astype(data[col].dtype)

        return sorted_data

    except Exception as e:
        raise e

def radixSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    try:
        max_value = data[column].max()

        exp = 1
        while max_value // exp > 0:
            data = countingSort(data, column)
            exp *= 10
        return data
    except Exception as e:
        print(f"Error in radixSort: {e}")
        return data


def oddEvenSort(data: pd.DataFrame, column: str) -> pd.DataFrame:
    try:
        n = len(data)
        isSorted = False
        
        while not isSorted:
            isSorted = True

            for i in range(1, n, 2):
                if data[column].iloc[i] > data[column].iloc[i + 1]:
                    data.iloc[[i, i + 1]] = data.iloc[[i + 1, i]]
                    isSorted = False
            
            for i in range(0, n - 1, 2):
                if data[column].iloc[i] > data[column].iloc[i + 1]:
                    data.iloc[[i, i + 1]] = data.iloc[[i + 1, i]]
                    isSorted = False
        
        return data
    except Exception as e:
        print(f"Error in oddEvenSort: {e}")
        return data

def bucketSort(data: pd.DataFrame, column: str, bucket_size=10) -> pd.DataFrame:
    try:
        max_value = data[column].max()
        min_value = data[column].min()
        bucket_count = (max_value - min_value) // bucket_size + 1
        buckets = [[] for _ in range(bucket_count)]

        for index, row in data.iterrows():
            bucket_index = (row[column] - min_value) // bucket_size
            buckets[bucket_index].append(row)

        sorted_data = pd.DataFrame(columns=data.columns)
        for bucket in buckets:
            sorted_data = pd.concat([sorted_data, pd.DataFrame(bucket).sort_values(by=column)], ignore_index=True)

        for col in data.columns:
            sorted_data[col] = sorted_data[col].astype(data[col].dtype)
        return sorted_data
    except Exception as e:
        print(f"Error in bucketSort: {e}")
        return data