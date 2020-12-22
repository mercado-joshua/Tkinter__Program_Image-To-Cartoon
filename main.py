#===========================
# Imports
#===========================
import tkinter as tk
from tkinter import ttk, colorchooser as cc, Menu, Spinbox as sb, scrolledtext as st, messagebox as mb, filedialog as fd, simpledialog as sd

import cv2

#===========================
# Main App
#===========================
class App(tk.Tk):
    """Main Application."""
    #------------------------------------------
    # Initializer
    #------------------------------------------
    def __init__(self):
        super().__init__()
        self.init_config()
        self.init_vars()
        self.init_widgets()
        self.init_events()

    #------------------------------------------
    # Instance Variables
    #------------------------------------------
    def init_vars(self):
        pass

    #-------------------------------------------
    # Window Settings
    #-------------------------------------------
    def init_config(self):
        self.resizable(True, True)
        self.title('Image To Cartoon Effect Version 1.0')
        self.iconbitmap('python.ico')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

    #-------------------------------------------
    # Window Events / Keyboard Shorcuts
    #-------------------------------------------
    def init_events(self):
        pass

    #-------------------------------------------
    # Widgets / Components
    #-------------------------------------------
    def init_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.fieldset = ttk.LabelFrame(self.main_frame, text='Cartoon Filter')
        self.fieldset.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        browse_btn = ttk.Button(self.fieldset, text='Browse Image', command=self.open_file)
        browse_btn.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        self.filepath = tk.StringVar()
        filepath_entry = ttk.Entry(self.fieldset, textvariable=self.filepath, width=50, state=tk.DISABLED)
        filepath_entry.grid(row=0, column=2, sticky=tk.W, padx=(0, 5), ipady=5)

        go_btn = ttk.Button(self.fieldset, text='Go', command=self.apply_filter)
        go_btn.grid(row=1, column=1, columnspan=2, sticky=tk.E, padx=5, pady=(0, 5))

    # ------------------------------------------
    def open_file(self):
        """Open and loads the image file."""
        try:
            file_types = (('JPEG Files', '*.jpg'), ('PNG Files', '*.png'))
            self.filename = fd.askopenfilename(title='Open', initialdir='/', filetypes=file_types)
            self.filepath.set(self.filename)

        except Exception as e:
            return

    def apply_filter(self):
        try:
            img = cv2.imread(self.filename)

            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            grey = cv2.medianBlur(grey, 5)
            edges = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

            # cartoonize
            color = cv2.bilateralFilter(img, 9, 250, 250)
            cartoon = cv2.bitwise_and(color, color, mask=edges)

            cv2.imshow('Original Image', img)
            cv2.imshow('Cartoon Image', cartoon)

            # save
            cv2.imwrite('cartoon.jpg', cartoon)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        except Exception as e:
            mb.showerror('Exception', e)


#===========================
# Start GUI
#===========================
def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()