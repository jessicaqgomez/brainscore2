import json
from tkinter import ttk, Frame, Button
from tkinter import N, S, W, E, FLAT, CENTER


########################################################################
class BrainscoreSimulator(Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        Frame.__init__(self, parent)
        self.parent = parent

        W_, H_ = 640, 480
        X_, Y_ = (self.parent.winfo_screenwidth() -
                  W_) // 2, (self.parent.winfo_screenheight() - H_) // 6
        self.parent.geometry("{}x{}+{}+{}".format(W_, H_, X_, Y_))

        self.parent.title('BrainScore2 - Data Stream Simulation')
        self.parent.config(padx=5, pady=5)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)

        style = ttk.Style(self.parent)
        style.configure('TNotebook', tabposition='wn', borderwidth=0)
        style.configure('TNotebook.Tab', borderwidth=0, width=15)

        notebook = ttk.Notebook(self.parent, style='TNotebook')
        notebook.grid(row=0, column=0, sticky=N + S + W + E)

        with open('interface.json') as file:
            interface = json.load(file)

            for parameter in interface:
                frame = Frame(notebook, relief=FLAT)
                if builder := getattr(self, f'build_{parameter["type"]}', None):
                    builder(frame, parameter)
                    notebook.add(frame, text=parameter['label'])

        self.parent.bind("<Destroy>", self.close_frame)

    # ----------------------------------------------------------------------
    def close_frame(self, *args, **kwargs):
        """"""
        self.destroy()

    # ----------------------------------------------------------------------
    def build_categorical(self, frame, parameter):
        """"""
        frame.grid_rowconfigure(0, weight=5)
        frame.grid_rowconfigure(len(parameter['options']) + 1, weight=5)

        for i in range(1, len(parameter['options']) + 1):
            frame.grid_rowconfigure(i, weight=2)

        for i in range(3):
            frame.grid_columnconfigure(i, weight=1)

        for i, option in enumerate(parameter['options']):
            button = Button(frame, text=option, width=20)
            button.grid(row=i + 1, column=1)

    # ----------------------------------------------------------------------
    def build_slider(self, frame, parameter):
        """"""

    # ----------------------------------------------------------------------
    def build_boolean(self, frame, parameter):
        """"""
