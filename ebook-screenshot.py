import pyautogui
import time
import os
from PIL import Image
from reportlab.pdfgen import canvas
from tkinter import Tk, Label, Entry, Button, Toplevel, Canvas, messagebox
from tkinter import filedialog
import pygetwindow as gw

# Directory to save screenshots
screenshot_dir = "screenshots"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

# Global variables to store the region for the screenshot
region_x, region_y, region_width, region_height = 0, 0, 0, 0

# Function to take a screenshot of a specific region
def take_screenshot(filename, region=None):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(filename)

# Function to simulate right arrow key presses a set number of times and take a screenshot after each press
def press_right_arrow_and_capture(presses, region=None):
    for i in range(presses):
        time.sleep(3)  # wait 1 second between key presses (adjust if needed)
        pyautogui.press('right')  # Simulate pressing the right arrow key
        screenshot_path = f"{screenshot_dir}/screenshot_{i+1}.png"
        take_screenshot(screenshot_path, region)
        print(f"Screenshot {i+1} saved to {screenshot_path}")

# Function to convert images to a single PDF without downgrading quality
def convert_images_to_pdf(image_folder, output_pdf, presses):
    image_list = []
    
    for i in range(1, presses + 1):
        image_path = f"{image_folder}/screenshot_{i}.png"
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image_list.append(image)  # Keep the original quality without conversion to RGB

    if image_list:
        # Save the images as a PDF without compressing or converting
        first_image = image_list[0]
        first_image.save(output_pdf, "PDF", resolution=100.0, save_all=True, append_images=image_list[1:])
        print(f"PDF saved to {output_pdf}")
        messagebox.showinfo("Success", f"PDF saved to {output_pdf}")
    else:
        messagebox.showerror("Error", "No screenshots found to convert to PDF")

# Function to select output PDF file
def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    return file_path

# Function to select the region interactively using a draggable box
def select_region():
    # Create a new window with a Canvas
    region_window = Toplevel()
    region_window.attributes("-fullscreen", True)
    region_window.attributes("-alpha", 0.3)  # Set transparency to 30%
    region_window.attributes("-topmost", True)

    canvas = Canvas(region_window, cursor="cross")
    canvas.pack(fill="both", expand=True)

    # Global variables for box coordinates
    global region_x, region_y, region_width, region_height

    # Temporary variables to track the box as the user draws it
    box_start_x, box_start_y = None, None
    rect_id = None

    # Function to start drawing the rectangle
    def start_draw(event):
        nonlocal box_start_x, box_start_y, rect_id
        box_start_x, box_start_y = event.x, event.y
        if rect_id:
            canvas.delete(rect_id)  # Delete the old rectangle if already drawn
        rect_id = canvas.create_rectangle(box_start_x, box_start_y, event.x, event.y, outline="red", width=2)

    # Function to draw the rectangle as the user drags the mouse
    def draw(event):
        nonlocal rect_id
        if rect_id:
            canvas.coords(rect_id, box_start_x, box_start_y, event.x, event.y)

    # Function to finalize the drawing of the rectangle and save the coordinates
    def end_draw(event):
        global region_x, region_y, region_width, region_height
        region_x, region_y = box_start_x, box_start_y
        region_width, region_height = event.x - box_start_x, event.y - box_start_y
        print(f"Region selected: X={region_x}, Y={region_y}, Width={region_width}, Height={region_height}")
        region_window.destroy()

    # Bind mouse events to start drawing, dragging, and ending
    canvas.bind("<ButtonPress-1>", start_draw)
    canvas.bind("<B1-Motion>", draw)
    canvas.bind("<ButtonRelease-1>", end_draw)

    # Wait for the region window to be closed
    region_window.wait_window()

# Function to handle the GUI button click and minimize window
def on_start_button_click():
    try:
        presses = int(presses_entry.get())

        if presses <= 0 or region_width <= 0 or region_height <= 0:
            messagebox.showerror("Error", "Please enter valid positive values for number of right arrow presses and region dimensions")
            return

        output_pdf = select_output_file()
        if not output_pdf:
            return  # If no file is selected, don't proceed

        region = (region_x, region_y, region_width, region_height)  # Define the screenshot area
        
        # Minimize or hide the main window to focus on the app behind
        root.withdraw()

        # Find the Kindle window by title
        kindle_window = None
        for window in gw.getWindowsWithTitle('Kindle'):
            kindle_window = window
            break

        if kindle_window:
            print(f"Focusing on Kindle window: {kindle_window.title}")
            kindle_window.activate()  # Bring the Kindle window to focus
        else:
            messagebox.showerror("Error", "Kindle window not found!")

        press_right_arrow_and_capture(presses, region)
        convert_images_to_pdf(screenshot_dir, output_pdf, presses)

        # Bring back the Tkinter window after screenshots are taken
        root.deiconify()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for right arrow presses")

# Setup GUI
root = Tk()
root.title("Screenshot and Right Arrow Key Automation")

# GUI labels and entry fields
presses_label = Label(root, text="Number of Page Turns (pages -1):")
presses_label.grid(row=0, column=0, padx=10, pady=10)
presses_entry = Entry(root)
presses_entry.grid(row=0, column=1, padx=10, pady=10)

# Button to open the region selection tool
select_region_button = Button(root, text="Select Screenshot Region", command=select_region)
select_region_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Start button
start_button = Button(root, text="Start", command=on_start_button_click)
start_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

# Run the GUI
root.mainloop()
