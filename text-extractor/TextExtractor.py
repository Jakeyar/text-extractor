#!/usr/bin/env python3

# Required dependencies (install via pip):
# pip install customtkinter PyMuPDF python-docx beautifulsoup4 reportlab pillow
# Note: PyMuPDF is used for PDF text extraction, reportlab for PDF creation

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF for PDF text extraction
from docx import Document  # For .docx text extraction
from bs4 import BeautifulSoup  # For HTML text extraction

# Set appearance mode for customtkinter (light, dark, or system)
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TextExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Extractor")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Store list of selected files
        self.files = []
        # Store extracted text
        self.extracted_text = []

        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # File list display
        self.file_listbox = ctk.CTkTextbox(self.main_frame, height=100, wrap="none")
        self.file_listbox.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.file_listbox.insert("end", "Click 'Select Files' to add files\n")
        self.file_listbox.configure(state="disabled")

        # Buttons
        self.select_button = ctk.CTkButton(self.main_frame, text="Select Files", command=self.select_files)
        self.select_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.clear_button = ctk.CTkButton(self.main_frame, text="Clear", command=self.clear_all)
        self.clear_button.grid(row=1, column=1, padx=5, pady=5)

        self.save_menu = ctk.CTkOptionMenu(self.main_frame, values=["Save as...", "Save as TXT", "Save as PDF"], command=self.save_file)
        self.save_menu.grid(row=1, column=2, padx=5, pady=5, sticky="e")

        # Text preview area
        self.text_area = ctk.CTkTextbox(self.main_frame, wrap="word", font=("Arial", 12))
        self.text_area.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.text_area.configure(state="disabled")

    def select_files(self):
        """Open file dialog to select multiple files."""
        filetypes = [
            ("Supported files", "*.txt *.pdf *.docx *.html *.md *.java *.py *.cpp *.cc *.y *.l"),
            ("All files", "*.*")
        ]
        files = filedialog.askopenfilenames(filetypes=filetypes)
        if files:
            self.add_files(files)

    def add_files(self, files):
        """Add files to the list and extract text."""
        for file in files:
            if file not in self.files and self.is_supported_file(file):
                self.files.append(file)
                text = self.extract_text(file)
                if text:
                    self.extracted_text.append((os.path.basename(file), text))
                else:
                    messagebox.showwarning("Warning", f"Could not extract text from {os.path.basename(file)}")

        self.update_file_list()
        self.update_text_area()

    def is_supported_file(self, file):
        """Check if file extension is supported."""
        supported_extensions = {'.txt', '.pdf', '.docx', '.html', '.md', '.java', '.py', '.cpp', '.cc', '.y', '.l'}
        return os.path.splitext(file)[1].lower() in supported_extensions

    def extract_text(self, file):
        """Extract readable text from a file based on its type."""
        try:
            ext = os.path.splitext(file)[1].lower()
            if ext in {'.txt', '.md', '.java', '.py', '.cpp', '.cc', '.y', '.l'}:
                with open(file, 'r', encoding='utf-8') as f:
                    return f.read()
            elif ext == '.pdf':
                doc = fitz.open(file)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
                return text
            elif ext == '.docx':
                doc = Document(file)
                return "\n".join([para.text for para in doc.paragraphs])
            elif ext == '.html':
                with open(file, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    return soup.get_text(separator='\n')
        except Exception as e:
            print(f"Error extracting {file}: {e}")
            return None
        return None

    def update_file_list(self):
        """Update the file list display."""
        self.file_listbox.configure(state="normal")
        self.file_listbox.delete("1.0", "end")
        if self.files:
            self.file_listbox.insert("end", "\n".join([os.path.basename(f) for f in self.files]))
        else:
            self.file_listbox.insert("end", "Click 'Select Files' to add files\n")
        self.file_listbox.configure(state="disabled")

    def update_text_area(self):
        """Update the text preview area with extracted text."""
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", "end")
        for filename, text in self.extracted_text:
            self.text_area.insert("end", f"--- {filename} ---\n{text}\n\n")
        self.text_area.configure(state="disabled")

    def clear_all(self):
        """Clear file list and text area."""
        self.files = []
        self.extracted_text = []
        self.update_file_list()
        self.update_text_area()

    def save_file(self, option):
        """Save the extracted text as TXT or PDF."""
        if not self.extracted_text:
            messagebox.showinfo("Info", "No text to save.")
            return

        content = "\n\n".join([f"--- {filename} ---\n{text}" for filename, text in self.extracted_text])

        if option == "Save as TXT":
            file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file:
                try:
                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    messagebox.showinfo("Success", "File saved successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {e}")

        elif option == "Save as PDF":
            file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if file:
                try:
                    c = canvas.Canvas(file, pagesize=letter)
                    y = 750  # Start near the top of the page
                    for line in content.split("\n"):
                        if y < 50:  # Start a new page if near the bottom
                            c.showPage()
                            y = 750
                        c.drawString(30, y, line[:100])  # Truncate long lines
                        y -= 15
                    c.save()
                    messagebox.showinfo("Success", "File saved successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = TextExtractorApp(root)
    root.mainloop()


