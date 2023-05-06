# DWG File Finder

The DWG File Finder is a simple and user-friendly tool to search and open DWG files on a network server. Users can search for DWG files by entering the file number. The application then searches the server for matching files and displays the results, allowing users to open the desired file directly from the interface.

## Features

- Find and open DWG files on a network server by file number
- Displays a list of matching DWG files with modification dates
- Opens the selected DWG file using Windows PowerShell
- Clear and easy-to-use graphical user interface

## Getting Started

### Prerequisites

- Python 3.7 or later
- Dear PyGui library

### Installation

1. Clone the repository:

    `git clone https://github.com/username/DWG-File-Finder.git`

2. Install the required dependencies:

    `pip install -r requirements.txt`

### Usage

Run the `file_finder.pyw` script to launch the application:

`python file_finder.pyw`

Enter the file number and click the "Search" button or press Enter. The application will display a list of matching DWG files with their modification dates. Select a file from the list and click the "Open" button to open the file.

To clear the search results and start a new search, click the "Clear" button.

## Modules

- `file_finder.pyw`: The entry point for the DWG File Finder application.
- `file.py`: A module containing the `DWGFiles` class, which handles all the file information of a specified DWG file.
- `gui_functions.py`: A module that creates the main GUI for the DWG File Finder and handles all the functions related to the GUI.
- `misc.py`: A module containing miscellaneous functions for the DWG File Finder program.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
