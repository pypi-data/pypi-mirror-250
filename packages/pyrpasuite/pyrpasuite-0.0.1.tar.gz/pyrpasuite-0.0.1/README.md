# pyrpasuite - A Comprehensive Robotic Process Automation (RPA) System

`pyrpasuite` is a Python-based Robotic Process Automation (RPA) system that allows you to automate repetitive tasks on web and desktop applications. It includes a wrapper for Selenium WebDriver for web automation, and a set of classes for automating tasks on desktop applications.

## Features

- **Web Automation**: Automate tasks on web applications using Selenium WebDriver.
- **Desktop Automation**: Automate tasks on desktop applications.
- **Excel Automation**: Automate tasks in Excel files.
- **PDF Automation**: Automate tasks involving PDF files.
- **Email Automation**: Automate email-related tasks.
- **Network Automation**: Automate network-related tasks.
- **System Automation**: Automate system-related tasks.

### Prerequisites

- Python 3.6 or higher
- Selenium WebDriver
- Other dependencies in the `requirements.txt` file

### Installing

1. Install the package using pip:
```bash
pip install pyrpasuite
```

## Usage

Here's a basic example of how to use the `pyrpasuite` system for web automation:

```python
from core.autoWeb import AutoWeb

# Create an instance of AutoWeb
auto_web = AutoWeb()

# Open a web page
auto_web.openBrowser("Firefox", "https://www.example.com")

# ... more code here ...

# Close the browser
auto_web.closeBrowser()
