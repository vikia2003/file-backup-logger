import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.filedialog as fd
from backup_manager import BackupManager
from config_manager import ConfigManager
from logger import Logger

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Backup Manager")

        self.config_manager = ConfigManager()
        self.config = self.config_manager.config
        self.logger = Logger()

        self.src_var = tk.StringVar(value=self.config.get("source", ""))
        self.dest_var = tk.StringVar(value=self.config.get("destination", ""))
        self.zip_var = tk.BooleanVar(value=self.config.get("zip", False))

        tk.Label(root, text="Source Folder:").grid(row=0, column=0, sticky="e")
        self.src_entry = tk.Entry(root, textvariable=self.src_var, width=50)
        self.src_entry.grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.select_source).grid(row=0, column=2)

        tk.Label(root, text="Destination Folder:").grid(row=1, column=0, sticky="e")
        self.dest_entry = tk.Entry(root, textvariable=self.dest_var, width=50)
        self.dest_entry.grid(row=1, column=1)

        tk.Button(root, text="Browse", command=self.select_destination).grid(row=1, column=2)

        tk.Checkbutton(root, text="Zip Backup", variable=self.zip_var).grid(row=2, column=1)

        tk.Button(root, text="Backup", command=self.perform_backup).grid(row=3, column=1)


    def select_source(self):
        path = filedialog.askdirectory()
        if path:
            self.src_entry.delete(0, tk.END)
            self.src_entry.insert(0, path)

    def select_destination(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, path)

    def perform_backup(self):
        src_path = self.src_var.get()
        dest_path = self.dest_var.get()
        use_zip = self.zip_var.get()

        backup_manager = BackupManager(src_path, dest_path, use_zip)
        result = backup_manager.perform_backup()

        success = result.get("success", False)
        backup_path = result.get("backup_path", "Unknown")

        self.logger.log(src_path, backup_path, success)

        if success:
            messagebox.showinfo("Success", f"Backup completed: {backup_path}")
        else:
            messagebox.showerror("Error", f"Backup failed: {result.get('error')}")

