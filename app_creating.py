import tkinter as tk
from tkinter import filedialog, messagebox
from files_processing import FilesProcessing


class PDFCreateApp(FilesProcessing):
    def __init__(self, root):
        self.root = root
        self.root.title("PDF ISO Converter")

        menu_bar = tk.Menu(self.root)

        self.pdf_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.output_pdf_folder = tk.StringVar()

        tk.Label(root, text="").grid(row=0, column=0, columnspan=3)

        tk.Label(root, text="Папка с PDF файлами:").grid(row=1, column=0, sticky=tk.W)
        tk.Entry(root, textvariable=self.pdf_folder, width=50).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="Выбрать", command=self.select_pdf_folder).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(root, text="Папка для сохранения Excel:").grid(row=2, column=0, sticky=tk.W)
        tk.Entry(root, textvariable=self.output_folder, width=50).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(root, text="Выбрать", command=self.select_output_folder).grid(row=2, column=2, padx=5, pady=5)

        tk.Label(root, text="Папка для обработанных файлов:").grid(row=3, column=0, sticky=tk.W)
        tk.Entry(root, textvariable=self.output_pdf_folder, width=50).grid(row=3, column=1, padx=5, pady=5)
        tk.Button(root, text="Выбрать", command=self.select_output_pdf_folder).grid(row=3, column=2, padx=5, pady=5)

        self.process_btn = tk.Button(root, text="Обработать", command=self.process_files, fg="black")
        self.process_btn.grid(row=4, columnspan=3, pady=10)

        self.status_lbl = tk.Label(root, text="", fg="black")
        self.status_lbl.grid(row=5, columnspan=3)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_info)
        menu_bar.add_cascade(label="Справка", menu=help_menu)
        self.root.config(menu=menu_bar)

    def show_info(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("Информация")
        about_window.resizable(False, False)
        about_window.geometry("400x120")

        tk.Label(about_window, text="Разработчик: Тарнов Глеб", anchor=tk.W, justify=tk.LEFT).pack(fill=tk.X, padx=10, pady=5)
        tk.Label(about_window, text="Версия: 1.0", anchor=tk.W, justify=tk.LEFT).pack(fill=tk.X, padx=10, pady=5)
        tk.Label(about_window, text="Локализация: Русский (Россия)", anchor=tk.W, justify=tk.LEFT).pack(fill=tk.X, padx=10, pady=5)