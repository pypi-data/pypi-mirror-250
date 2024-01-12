def bubble_sort(arr):
    """
    Sorts an array using the bubble sort algorithm.

    Parameters:
        arr (list): The input list to be sorted.

    Returns:
        list: The sorted list.
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def selection_sort(arr):
    """
    Sorts an array using the selection sort algorithm.

    Parameters:
        arr (list): The input list to be sorted.

    Returns:
        list: The sorted list.
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr):
    """
    Sorts an array using the insertion sort algorithm.

    Parameters:
        arr (list): The input list to be sorted.

    Returns:
        list: The sorted list.
    """
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# Take input from the user
# input_list = input("Enter a list of numbers separated by spaces: ").split()
input_list = [4, 2, 7, 1, 9, 5]

# Call the sorting functions
sorted_list_bubble = bubble_sort(input_list.copy())
sorted_list_selection = selection_sort(input_list.copy())
sorted_list_insertion = insertion_sort(input_list.copy())

# Print the sorted lists
print("Bubble Sort:", sorted_list_bubble)
print("Selection Sort:", sorted_list_selection)
print("Insertion Sort:", sorted_list_insertion)
