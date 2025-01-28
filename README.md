# Ebook Screenshot Automation

This Python project allows you to automate the task of taking screenshots of a selected region after simulating right arrow key presses. It's designed to return focus to the Kindle app after you start the automation. The screenshots are converted to a high-quality PDF without downgrading the image resolution.

## Features

- Interactive screenshot region selection with a draggable box.
- Simulates right arrow key presses to flip through pages.
- Focuses on the Kindle app after starting the automation.
- Converts captured screenshots to a PDF without loss of image quality.

## Installation

### Prerequisites

Before running this script, make sure you have Python installed on your machine. You can download Python from [here](https://www.python.org/downloads/).  This currently only works on Windows.

### Required Python Packages

This project depends on several Python libraries. To install them, run the following command in your terminal:

```bash
pip install pyautogui pillow reportlab pygetwindow img2pdf
```

- `pyautogui`: Used for automating keyboard presses and taking screenshots.
- `Pillow`: A Python Imaging Library used for image manipulation.
- `reportlab`: A PDF generation library used for creating the PDF from screenshots.
- `pygetwindow`: A library to interact with application windows, used to focus on Kindle.
- `img2pdf`: A library that enables seamless conversion of various image formats (JPEG, PNG, etc.) into high-quality PDF files

## Usage

1. Clone the repository or download the script.

2. Open a terminal or command prompt and navigate to the directory where the script is located.

3. Run the script:

    ```bash
    python ebook-screenshot.py
    ```

4. Once the GUI appears:
    - Select the screenshot region by clicking the **"Select Screenshot Region"** button.
    - Define the number of pages (this determines how many screenshots will be taken after each page flip).
    - Click the **"Start"** button to begin the process.

5. The script will:
    - Automatically focus on the **Kindle** application.
    - Simulate right arrow key presses (to flip through pages).
    - Take screenshots of the specified region after each key press.
    - Convert the screenshots to a high-quality PDF without any image compression.

### Example

- Suppose you want to take 10 screenshots from the Kindle app, capturing a specific portion of the screen. 
    1. Select the screenshot region (e.g., the content of the book you're reading).
    2. Set the number of page turns (e.g., `10`).
    3. Click **Start**. The script will return focus to the Kindle app, press the right arrow 10 times, and capture screenshots after each press.
    4. A PDF will be generated with all the screenshots in high resolution.

### Important Notes

- Ensure the **Kindle** application is open before running the script.
- Make sure the Kindle window is titled "Kindle" for the script to detect and return focus to it.

## Contributing

If you find any issues or would like to contribute to the project, feel free to submit a pull request or open an issue on GitHub.
