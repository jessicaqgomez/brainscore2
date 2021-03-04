from tkinter import Tk
from widgets import BrainscoreSimulator


# ----------------------------------------------------------------------
def main():
    """Entry point for command line invocation."""

    root = Tk()
    app = BrainscoreSimulator(root)

    app.mainloop()


if __name__ == '__main__':
    main()
