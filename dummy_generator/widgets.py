from datetime import datetime

import json
from tkinter import ttk, Frame, Text
from tkinter import N, S, W, E, FLAT, DISABLED, NORMAL, END

from builder import Builder
from osc_streamer import OSCStreamer


########################################################################
class BrainscoreSimulator(Frame, Builder):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        Frame.__init__(self, parent)
        self.parent = parent
        self.parameters = {}
        self.labels = {}

        self.streamer = OSCStreamer('127.0.0.1', 5005)

        W_, H_ = 940, 480
        X_, Y_ = (self.parent.winfo_screenwidth()
                  - W_) // 2, (self.parent.winfo_screenheight() - H_) // 6
        self.parent.geometry("{}x{}+{}+{}".format(W_, H_, X_, Y_))

        self.parent.title('BrainScore2 - Data Stream Simulation')
        self.parent.config(padx=5, pady=5)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=0)

        style = ttk.Style(self.parent)
        style.configure('TNotebook', tabposition='wn', borderwidth=0)
        style.configure('TNotebook.Tab', borderwidth=0, width=15)

        notebook = ttk.Notebook(self.parent, style='TNotebook')
        notebook.grid(row=0, column=0, sticky=N + S
                      + W + E, padx=(0, 0), pady=(5, 0))

        self.logging = Text(self.parent, bg="#444444", fg="#ffffff", height=10,
                            borderwidth=5, relief=FLAT, highlightthickness=0, font="mono 10", wrap="none")
        self.logging.config(state=DISABLED)
        self.logging.grid(row=1, column=0, sticky=N + S
                          + W + E, padx=(0, 0), pady=(5, 0))

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
    def stream_data(self, type_, name, value):
        """"""
        data = {
            'type': type_,
            'name': name,
            'value': value,
            'timestamp': datetime.now().timestamp(),
        }
        data = json.dumps(data)
        self.log(data)
        self.streamer.write(data)

    # ----------------------------------------------------------------------
    def log(self, message):
        """"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")
        self.logging.config(state=NORMAL)
        self.logging.insert(END, now + message + '\n')
        self.logging.see(END)
        self.logging.config(state=DISABLED)

        if now:
            self.logging.tag_add("start", self.logging.index(
                'end-2l'), self.logging.index('end-2l+{}c'.format(len(now))))
            self.logging.tag_config(
                "start", foreground="#00AFEF", font=("mono", 9))
