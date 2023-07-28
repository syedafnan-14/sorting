import tkinter as tk
import random
import time

# Global variables
array = []
canvas_width = 800
canvas_height = 400
bar_width = 50
delay = 50  # Time delay between each comparison and swap (in milliseconds)
sort_method = None

# Create the main window
window = tk.Tk()
window.title("Sorting Visualizer")

# Create the canvas
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="#ece6ff")
canvas.pack(fill=tk.BOTH, expand=True)


def generate_array():
    global array, canvas_width, canvas_height
    array = [random.randint(10, canvas_height - 10) for _ in range(array_size_slider.get())]

    # Adjust canvas width based on array size
    canvas_width = bar_width * array_size_slider.get()
    canvas.config(width=canvas_width)

    # Adjust canvas height if it exceeds the window height
    if canvas_height > window.winfo_screenheight():
        canvas_height = window.winfo_screenheight() - 100
        canvas.config(height=canvas_height)

    draw_array()
  # Call the generate_array function to initialize the array



def draw_array(current_index=None, compare_index=None, sorted=False):
    canvas.delete("all")
    for i, height in enumerate(array):
        x0 = i * bar_width
        y0 = canvas_height - height
        x1 = x0 + bar_width
        y1 = canvas_height
        fill_color = "#77ab59" if sorted else "#2389da"
        if compare_index is not None and i == compare_index:
            fill_color = "#ffcc5c"
        if current_index is not None and i == current_index:
            fill_color = "#ff6f69"
        canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color)

    window.update()
    time.sleep(delay*10 / 1000)


def bubble_sort():
    global array, sort_method
    sort_method = "Bubble Sort"
    n = len(array)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                swapped = True
                draw_array(j + 1, j)
            
        if not swapped:
            break
    draw_array(sorted=True)


def selection_sort():
    global array, sort_method
    sort_method = "Selection Sort"
    n = len(array)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if array[j] < array[min_idx]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
        draw_array(i, min_idx)
        
    draw_array(sorted=True)


def insertion_sort():
    global array, sort_method
    sort_method = "Insertion Sort"
    n = len(array)
    for i in range(1, n):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            draw_array(j + 1, j)
            j -= 1
            
        array[j + 1] = key
    draw_array(sorted=True)


def merge_sort():
    global array, sort_method
    sort_method = "Merge Sort"

    def merge(arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m
        L = [0] * n1
        R = [0] * n2

        for i in range(n1):
            L[i] = arr[l + i]
        for j in range(n2):
            R[j] = arr[m + 1 + j]

        i = j = 0
        k = l
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            draw_array(k)
            k += 1
           

        while i < n1:
            arr[k] = L[i]
            draw_array(k)
            i += 1
            k += 1
           

        while j < n2:
            arr[k] = R[j]
            draw_array(k)
            j += 1
            k += 1
           
             

    def merge_sort_recursive(arr, l, r):
        if l < r:
            m = (l + r) // 2
            merge_sort_recursive(arr, l, m)
            merge_sort_recursive(arr, m + 1, r)
            merge(arr, l, m, r)

    merge_sort_recursive(array, 0, len(array) - 1)
    draw_array(sorted=True)


def quick_sort():
    global array, sort_method
    sort_method = "Quick Sort"

    def partition(arr, low, high):
        i = low - 1
        pivot = arr[high]

        for j in range(low, high):
            if arr[j] <= pivot:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]
                draw_array(i, j)
             

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        draw_array(i + 1, high)
        return i + 1

    def quick_sort_recursive(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_recursive(arr, low, pi - 1)
            quick_sort_recursive(arr, pi + 1, high)

    quick_sort_recursive(array, 0, len(array) - 1)
    draw_array(sorted=True)


def set_speed(value):
    global delay
    delay = int(value)






# Create buttons and sliders
slider_style={
    "fg": "black",  # Text color
    "font": ("Helvetica", 10,"bold"),  # Font family and size
    "relief": "flat",
}
generate_button = tk.Button(window, text="Generate Array", command=generate_array, bg="#ff4e50",**slider_style)
generate_button.pack(side="left")

bubble_sort_button = tk.Button(window, text="Bubble Sort", command=bubble_sort, bg="#feda75",**slider_style)
bubble_sort_button.pack(side="left")

selection_sort_button = tk.Button(window, text="Selection Sort", command=selection_sort, bg="#fa7e1e",**slider_style)
selection_sort_button.pack(side="left")

insertion_sort_button = tk.Button(window, text="Insertion Sort", command=insertion_sort, bg="#01cdfe",**slider_style)
insertion_sort_button.pack(side="left")

merge_sort_button = tk.Button(window, text="Merge Sort", command=merge_sort, bg="#05ffa1",**slider_style)
merge_sort_button.pack(side="left")

quick_sort_button = tk.Button(window, text="Quick Sort", command=quick_sort, bg="#b967ff",**slider_style)
quick_sort_button.pack(side="left")

speed_label = tk.Label(window, text="Speed:", bg="#97ebdb",**slider_style)
speed_label.pack(side="left")
speed_slider = tk.Scale(window, from_=1, to=20, orient="horizontal", length=150, command=set_speed, bg="#97ebdb",**slider_style)
speed_slider.pack(side="left")
speed_slider.set(delay)

array_size_label = tk.Label(window, text="Array Size:", bg="#ff9a00",**slider_style)
array_size_label.pack(side="left")
array_size_slider = tk.Scale(window, from_=10, to=(window.winfo_screenwidth() // bar_width), orient="horizontal",
                            length=150, bg="#ff9a00",**slider_style)
array_size_slider.pack(side="left")
array_size_slider.set(canvas_width // bar_width)

# Start the main loop
window.mainloop()