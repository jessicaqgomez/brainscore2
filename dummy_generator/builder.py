
from tkinter import Button, Label
import datetime
import numpy as np


########################################################################
class Builder:
    """"""

    # ----------------------------------------------------------------------
    def build_time_series(self, _, parameter):
        """"""
        self.time_series[parameter['name']] = parameter.copy()
        self.time_series[parameter['name']]['start'] = 0
        self.update_time_series(parameter['name'])

    # ----------------------------------------------------------------------
    def update_time_series(self, name):
        """"""
        parameter = self.time_series[name]
        start = parameter['start']
        t = np.linspace(start, start + parameter['package_size']
                        / parameter['sample_frequency'], parameter['package_size'])

        parameter['start'] = t[-1]
        signal = eval(parameter['value'])
        
        self.stream_data(parameter['type'], name, (signal.tolist())[:12])
       
        timeout_ms = (parameter['package_size']
                      / parameter['sample_frequency']) * 1000
        self.after(int(timeout_ms), lambda: self.update_time_series(name))

    # ----------------------------------------------------------------------
    def build_categorical(self, frame, parameter):
        """"""
        frame.grid_rowconfigure(0, weight=5)
        frame.grid_rowconfigure(len(parameter['values']) + 1, weight=5)

        for i in range(1, len(parameter['values']) + 1):
            frame.grid_rowconfigure(i, weight=2)

        for i in range(3):
            frame.grid_columnconfigure(i, weight=1)

        self.parameters[parameter['name']] = ''
        for i, values in enumerate(parameter['values']):
            name, label = values

            button = Button(frame, text=label, width=20,
                            command=self.set_parameter(parameter['type'], parameter['name'], name))
            button.grid(row=i + 1, column=1)

    # ----------------------------------------------------------------------
    def build_slider(self, frame, parameter):
        """"""
        frame.grid_rowconfigure(0, weight=5)
        for i in range(1, 4):
            frame.grid_rowconfigure(i, weight=2)
        frame.grid_rowconfigure(4, weight=5)

        for i in range(3):
            frame.grid_columnconfigure(i, weight=1)

        for i, option in enumerate(parameter['increase_modifiers']):
            button = Button(frame, text=option, width=5,
                            command=self.set_parameter(parameter['type'], parameter['name'], option))
            button.grid(row=1, column=i)

        label = Label(frame, text=str(parameter['value']))
        r = int(len(parameter['increase_modifiers']) // 2)
        label.grid(row=2, column=r)

        self.parameters[parameter['name']] = parameter['value']
        self.labels[parameter['name']] = label

        for i, option in enumerate(parameter['decrease_modifiers']):
            button = Button(frame, text=option, width=5,
                            command=self.set_parameter(parameter['type'], parameter['name'], option))
            button.grid(row=3, column=i)

    # ----------------------------------------------------------------------
    def build_boolean(self, frame, parameter):
        """"""
        frame.grid_columnconfigure(0, weight=5)
        for i in range(1, 4):
            frame.grid_columnconfigure(i, weight=2)
        frame.grid_columnconfigure(4, weight=5)

        frame.grid_rowconfigure(0, weight=5)
        for i in range(1, len(parameter['values']) + 1):
            frame.grid_rowconfigure(i, weight=2)
        frame.grid_rowconfigure(len(parameter['values']) + 1, weight=5)

        for i, values in enumerate(parameter['values']):

            name, label, value = values
            self.parameters[name] = value

            button_true = Button(frame, text='True', width=5,
                                 command=self.set_parameter(parameter['type'], name, True))
            button_true.grid(row=i + 1, column=1)

            label_ = Label(frame, text=f'{label}:{value}', width=15)
            label_.grid(row=i + 1, column=2)
            label_.prefix = label
            self.labels[name] = label_

            button_false = Button(frame, text='False', width=5, command=self.set_parameter(
                parameter['type'], name, False))
            button_false.grid(row=i + 1, column=3)

    # ----------------------------------------------------------------------
    def set_parameter(self, type_, name, value):
        """"""
        # ----------------------------------------------------------------------
        def wrap(*args, **kwars):
            if type_ == 'categorical':
                self.parameters[name] = value

            elif type_ == 'slider':
                self.parameters[name] += float(value)
                self.labels[name].config(text=self.parameters[name])

            elif type_ == 'boolean':
                self.parameters[name] = value
                self.labels[name].config(
                    text=f'{self.labels[name].prefix}:{value}')

            self.stream_data(type_, name, self.parameters[name])

        return wrap
