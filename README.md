
# Library Management System with Tkinter GUI

A simple **Library Management System** built with Python, featuring a user-friendly graphical interface using Tkinter and a persistent backend using SQLite. This application allows users to manage books in a library, including adding, searching, borrowing, returning, listing books, and managing user comments.

## Features

- **Add Book:** Enter the book title and author directly in the provided form to add a new book to the library.
- **Search Books:** Quickly search for books by title. Search results display the author and availability status.
- **Borrow Book:** Borrow a book if it is available. The system automatically marks it as unavailable.
- **Return Book:** Return a borrowed book and update its status to available.
- **List Books:** View all books in a table-like format using a Treeview widget.
- **User Comments:** Add and view comments for each book.
- **Exit:** Easily exit the application through the menu bar.

## Getting Started

### Prerequisites

- **Python 3.x**  
  Most modern Python installations include SQLite3 and Tkinter by default. If Tkinter is not installed on your system, refer to the [Tkinter installation guide](https://tkdocs.com/tutorial/install.html).

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ayerna/library-management-system.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd library-management-system
   ```

### Running the Application

Run the Python script to start the application:

```bash
python library_management_gui.py
```

The GUI window will open, displaying a tabbed interface for managing your library.

## Code Structure

- **`library_management_gui.py`**  
  The main Python file that includes the complete code for the Library Management System with a Tkinter GUI.

- **SQLite Database (`library.db`):**  
  The application automatically creates and uses a SQLite database to store book information and user comments.

## Usage

- **Tabbed Interface:**  
  The application uses a tabbed interface (`ttk.Notebook`) to separate functionalities, making it intuitive to navigate through different operations.

- **Forms and Status Messages:**  
  Each tab contains dedicated input fields and status messages to guide users through various operations (adding, searching, borrowing, returning books, and managing comments).

- **Treeview for Listing Books:**  
  The "List Books" tab displays all books in a table format with scroll functionality.

