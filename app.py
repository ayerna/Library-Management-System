import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------
# Database Setup Function
# -----------------------
def init_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            available INTEGER DEFAULT 1
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_title TEXT NOT NULL,
            comment TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# -----------------------
# Main Application Class
# -----------------------
class LibraryApp:
    def __init__(self, root):
        self.root = root
        root.title("Library Management System")
        root.geometry("700x600")
        root.resizable(False, False)

        # Add a menu bar with an Exit option
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menu_bar)

        # Create Notebook for different sections
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        self.create_add_book_tab()
        self.create_search_book_tab()
        self.create_borrow_book_tab()
        self.create_return_book_tab()
        self.create_list_books_tab()
        self.create_comments_tab()

    # -----------------------
    # Add Book Tab
    # -----------------------
    def create_add_book_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Add Book")

        # Labels and entry fields for title and author
        ttk.Label(frame, text="Book Title:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.add_title_entry = ttk.Entry(frame, width=40)
        self.add_title_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Author:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.add_author_entry = ttk.Entry(frame, width=40)
        self.add_author_entry.grid(row=1, column=1, padx=10, pady=10)

        add_btn = ttk.Button(frame, text="Add Book", command=self.add_book)
        add_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.add_status = ttk.Label(frame, text="", font=("Arial", 10))
        self.add_status.grid(row=3, column=0, columnspan=2, pady=5)

    def add_book(self):
        title = self.add_title_entry.get().strip()
        author = self.add_author_entry.get().strip()
        if not title or not author:
            self.add_status.config(text="Please fill in all fields.", foreground="red")
            return
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        conn.commit()
        conn.close()
        self.add_status.config(text="Book added successfully!", foreground="green")
        self.add_title_entry.delete(0, tk.END)
        self.add_author_entry.delete(0, tk.END)

    # -----------------------
    # Search Book Tab
    # -----------------------
    def create_search_book_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Search Book")

        ttk.Label(frame, text="Book Title:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.search_entry = ttk.Entry(frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        search_btn = ttk.Button(frame, text="Search", command=self.search_book)
        search_btn.grid(row=0, column=2, padx=10, pady=10)

        # Text widget to display search results
        self.search_results = tk.Text(frame, width=80, height=20, wrap="word")
        self.search_results.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.search_results.config(state='disabled')

    def search_book(self):
        title = self.search_entry.get().strip()
        self.search_results.config(state='normal')
        self.search_results.delete(1.0, tk.END)
        if not title:
            self.search_results.insert(tk.END, "Please enter a title to search.")
            self.search_results.config(state='disabled')
            return
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, author, available FROM books WHERE title LIKE ?", ('%' + title + '%',))
        books = cursor.fetchall()
        conn.close()
        if books:
            for book in books:
                avail = "Yes" if book[2] == 1 else "No"
                self.search_results.insert(tk.END, f"{book[0]} by {book[1]} (Available: {avail})\n")
        else:
            self.search_results.insert(tk.END, "No book found.")
        self.search_results.config(state='disabled')

    # -----------------------
    # Borrow Book Tab
    # -----------------------
    def create_borrow_book_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Borrow Book")

        ttk.Label(frame, text="Book Title:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.borrow_entry = ttk.Entry(frame, width=40)
        self.borrow_entry.grid(row=0, column=1, padx=10, pady=10)

        borrow_btn = ttk.Button(frame, text="Borrow Book", command=self.borrow_book)
        borrow_btn.grid(row=1, column=0, columnspan=2, pady=10)

        self.borrow_status = ttk.Label(frame, text="", font=("Arial", 10))
        self.borrow_status.grid(row=2, column=0, columnspan=2, pady=5)

    def borrow_book(self):
        title = self.borrow_entry.get().strip()
        if not title:
            self.borrow_status.config(text="Please enter a book title.", foreground="red")
            return
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM books WHERE title = ? AND available = 1", (title,))
        book = cursor.fetchone()
        if book:
            cursor.execute("UPDATE books SET available = 0 WHERE id = ?", (book[0],))
            conn.commit()
            self.borrow_status.config(text="Book borrowed successfully!", foreground="green")
        else:
            self.borrow_status.config(text="Book not available or not found.", foreground="red")
        conn.close()
        self.borrow_entry.delete(0, tk.END)

    # -----------------------
    # Return Book Tab
    # -----------------------
    def create_return_book_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Return Book")

        ttk.Label(frame, text="Book Title:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.return_entry = ttk.Entry(frame, width=40)
        self.return_entry.grid(row=0, column=1, padx=10, pady=10)

        return_btn = ttk.Button(frame, text="Return Book", command=self.return_book)
        return_btn.grid(row=1, column=0, columnspan=2, pady=10)

        self.return_status = ttk.Label(frame, text="", font=("Arial", 10))
        self.return_status.grid(row=2, column=0, columnspan=2, pady=5)

    def return_book(self):
        title = self.return_entry.get().strip()
        if not title:
            self.return_status.config(text="Please enter a book title.", foreground="red")
            return
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM books WHERE title = ? AND available = 0", (title,))
        book = cursor.fetchone()
        if book:
            cursor.execute("UPDATE books SET available = 1 WHERE id = ?", (book[0],))
            conn.commit()
            self.return_status.config(text="Book returned successfully!", foreground="green")
        else:
            self.return_status.config(text="Book not found or already returned.", foreground="red")
        conn.close()
        self.return_entry.delete(0, tk.END)

    # -----------------------
    # List Books Tab
    # -----------------------
    def create_list_books_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="List Books")

        # Use Treeview widget for a table view of books
        self.tree = ttk.Treeview(frame, columns=("Title", "Author", "Available"), show='headings', height=20)
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Available", text="Available")
        self.tree.column("Title", width=250)
        self.tree.column("Author", width=200)
        self.tree.column("Available", width=80, anchor='center')
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        refresh_btn = ttk.Button(frame, text="Refresh List", command=self.list_books)
        refresh_btn.grid(row=1, column=0, pady=10)

        # Make sure the treeview expands
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def list_books(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, author, available FROM books")
        books = cursor.fetchall()
        conn.close()
        for book in books:
            avail = "Yes" if book[2] == 1 else "No"
            self.tree.insert("", tk.END, values=(book[0], book[1], avail))

    # -----------------------
    # User Comments Tab
    # -----------------------
    def create_comments_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="User Comments")

        # Section to add a comment
        add_comment_frame = ttk.LabelFrame(frame, text="Add Comment")
        add_comment_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        ttk.Label(add_comment_frame, text="Book Title:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.comment_book_entry = ttk.Entry(add_comment_frame, width=40)
        self.comment_book_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_comment_frame, text="Comment:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky='nw')
        self.comment_text = tk.Text(add_comment_frame, width=50, height=5)
        self.comment_text.grid(row=1, column=1, padx=5, pady=5)

        add_comment_btn = ttk.Button(add_comment_frame, text="Add Comment", command=self.add_comment)
        add_comment_btn.grid(row=2, column=0, columnspan=2, pady=5)
        self.comment_status = ttk.Label(add_comment_frame, text="", font=("Arial", 10))
        self.comment_status.grid(row=3, column=0, columnspan=2, pady=5)

        # Section to view comments for a specific book
        view_comment_frame = ttk.LabelFrame(frame, text="View Comments")
        view_comment_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        ttk.Label(view_comment_frame, text="Book Title:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.view_book_entry = ttk.Entry(view_comment_frame, width=40)
        self.view_book_entry.grid(row=0, column=1, padx=5, pady=5)

        view_comment_btn = ttk.Button(view_comment_frame, text="View Comments", command=self.view_comments)
        view_comment_btn.grid(row=1, column=0, columnspan=2, pady=5)

        self.view_comment_text = tk.Text(view_comment_frame, width=60, height=10, wrap="word")
        self.view_comment_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.view_comment_text.config(state='disabled')

    def add_comment(self):
        book_title = self.comment_book_entry.get().strip()
        comment = self.comment_text.get(1.0, tk.END).strip()
        if not book_title or not comment:
            self.comment_status.config(text="Please fill in both fields.", foreground="red")
            return
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO comments (book_title, comment) VALUES (?, ?)", (book_title, comment))
        conn.commit()
        conn.close()
        self.comment_status.config(text="Comment added successfully!", foreground="green")
        self.comment_book_entry.delete(0, tk.END)
        self.comment_text.delete(1.0, tk.END)

    def view_comments(self):
        book_title = self.view_book_entry.get().strip()
        self.view_comment_text.config(state='normal')
        self.view_comment_text.delete(1.0, tk.END)
        if not book_title:
            self.view_comment_text.insert(tk.END, "Please enter a book title.")
            self.view_comment_text.config(state='disabled')
            return
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT comment FROM comments WHERE book_title = ?", (book_title,))
        comments = cursor.fetchall()
        conn.close()
        if comments:
            for comm in comments:
                self.view_comment_text.insert(tk.END, f"- {comm[0]}\n")
        else:
            self.view_comment_text.insert(tk.END, "No comments for this book.")
        self.view_comment_text.config(state='disabled')

# -----------------------
# Main Execution
# -----------------------
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
