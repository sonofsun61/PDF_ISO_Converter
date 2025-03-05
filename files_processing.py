import tkinter as tk
import os
import shutil
import pandas as pd
import fitz  # PyMuPDF
from tkinter import filedialog, messagebox
from text_processing import TextProcessing
from save_excel import save_to_excel


class FilesProcessing(TextProcessing):
    def select_pdf_folder(self):
        folder = filedialog.askdirectory()
        self.pdf_folder.set(folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        self.output_folder.set(folder)

    def select_output_pdf_folder(self):
        folder = filedialog.askdirectory()
        self.output_pdf_folder.set(folder)

    def process_files(self):
        pdf_path = self.pdf_folder.get()
        output_excel_path = self.output_folder.get()
        output_pdf_path = self.output_pdf_folder.get()

        if not pdf_path or not output_excel_path or not output_pdf_path:
            messagebox.showerror("Ошибка", "Выберите все папки")
            return

        if not os.path.exists(output_pdf_path):
            os.makedirs(output_pdf_path)

        self.status_lbl.config(text="Выполняется обработка файлов...")
        self.process_btn.config(state=tk.DISABLED)
        all_data = []

        for file_name in os.listdir(pdf_path):
            if not file_name.endswith('.pdf'):
                continue
            file_path = os.path.join(pdf_path, file_name)
            try:
                file = fitz.open(file_path)  # Открываем PDF

                for page_num in range(len(file)):
                    try:
                        columns, id = self.extract_columns(file, page_num)  # Используем метод из TextProcessing
                        formatted = self.format_columns(columns, id)  # Используем метод из TextProcessing
                        result = self.insert_spaces(formatted)  # Используем метод из TextProcessing

                        df = pd.DataFrame({
                            'ИДЕНТИФИКАТОР': result.get(0, []),
                            'ОПИСАНИЕ КОМПОНЕНТА': result.get(1, []),
                            'ИДЕНТ.КОД': result.get(2, []),
                            'КОЛ-ВО': result.get(3, [])
                        })

                        all_data.append(df)
                    except Exception as e:
                        messagebox.showerror("Ошибка", f"Ошибка обработки файла {file_name} на странице {page_num + 1}")
                        continue

                file.close()

                try:
                    shutil.move(file_path, os.path.join(output_pdf_path, file_name))
                    self.status_lbl.config(text=f"Файл {file_name} успешно перемещен")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при перемещении файла {file_name}: {str(e)}")
                    continue

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обработать файл {file_name}: {str(e)}")
                continue

        if not all_data:
            self.status_lbl.config(text="Нет данных для сохранения")
            self.process_btn.config(state=tk.NORMAL)
            return

        final_df = pd.concat(all_data, ignore_index=True)
        excel_file_name = "Спецификация к чертежам.xlsx"
        output_file = os.path.join(output_excel_path, excel_file_name)
        save_to_excel(final_df, output_file)  # Импортируем функцию из save_excel.py

        self.status_lbl.config(text=f"Обработка завершена. Файл {excel_file_name} сохранен.")
        self.process_btn.config(state=tk.NORMAL)