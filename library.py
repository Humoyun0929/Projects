import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")
conn.commit()


# =========================
# APP STYLE
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# =========================
# LOGIN PAGE
# =========================
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("350x300")
        self.root.resizable(False, False)

        self.label = ctk.CTkLabel(root, text="ADMIN LOGIN", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        self.user_entry = ctk.CTkEntry(root, placeholder_text="Username")
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(root, placeholder_text="Password", show="*")
        self.pass_entry.pack(pady=10)

        self.login_btn = ctk.CTkButton(root, text="LOGIN", command=self.login)
        self.login_btn.pack(pady=20)

    def login(self):
        user = self.user_entry.get()
        password = self.pass_entry.get()

        # SIMPLE ADMIN
        if user == "admin" and password == "1234":
            self.root.destroy()
            main_window()
        else:
            messagebox.showerror("Xato", "Login yoki password noto'g'ri!")


# =========================
# MAIN APP (PRO DASHBOARD)
# =========================
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library System PRO")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # LEFT MENU
        self.sidebar = ctk.CTkFrame(root, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.title = ctk.CTkLabel(self.sidebar, text="📚 MENU", font=("Arial", 18, "bold"))
        self.title.pack(pady=20)

        ctk.CTkButton(self.sidebar, text="Add Book", command=self.show_add).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="View Books", command=self.show_books).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Delete Book", command=self.show_delete).pack(pady=10)

        # MAIN AREA
        self.main = ctk.CTkFrame(root)
        self.main.pack(side="right", fill="both", expand=True)

        self.show_books()

    # CLEAR SCREEN
    def clear(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    # ================= ADD BOOK =================
    def show_add(self):
        self.clear()

        label = ctk.CTkLabel(self.main, text="➕ Add Book", font=("Arial", 20))
        label.pack(pady=20)

        self.entry = ctk.CTkEntry(self.main, placeholder_text="Book name")
        self.entry.pack(pady=10)

        btn = ctk.CTkButton(self.main, text="Save", command=self.add_book)
        btn.pack(pady=10)

    def add_book(self):
        name = self.entry.get()

        if not name.strip():
            messagebox.showerror("Error", "Empty name!")
            return

        cursor.execute("INSERT INTO books (name) VALUES (?)", (name,))
        conn.commit()

        messagebox.showinfo("OK", "Book added!")
        self.show_books()

    # ================= VIEW BOOKS =================
    def show_books(self):
        self.clear()

        label = ctk.CTkLabel(self.main, text="📖 All Books", font=("Arial", 20))
        label.pack(pady=10)

        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

        for b in books:
            ctk.CTkLabel(self.main, text=f"ID: {b[0]} | {b[1]}").pack(pady=2)

    # ================= DELETE BOOK =================
    def show_delete(self):
        self.clear()

        label = ctk.CTkLabel(self.main, text="🗑 Delete Book", font=("Arial", 20))
        label.pack(pady=20)

        self.del_entry = ctk.CTkEntry(self.main, placeholder_text="Enter Book ID")
        self.del_entry.pack(pady=10)

        btn = ctk.CTkButton(self.main, text="Delete", command=self.delete_book)
        btn.pack(pady=10)

    def delete_book(self):
        try:
            book_id = int(self.del_entry.get())

            cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showerror("Error", "ID not found")
            else:
                messagebox.showinfo("OK", "Deleted!")

            self.show_books()

        except:
            messagebox.showerror("Error", "Enter valid ID")


# =========================
# MAIN WINDOW
# =========================
def main_window():
    root = ctk.CTk()
    LibraryApp(root)
    root.mainloop()


# =========================
# RUN LOGIN FIRST
# =========================
if __name__ == "__main__":
    root = ctk.CTk()
    LoginApp(root)
    root.mainloop()