import tkinter as tk
from app_creating import PDFCreateApp


def main():
    root = tk.Tk()
    app = PDFCreateApp(root)
    root.mainloop()
    return app


if __name__ == "__main__":
    main()
