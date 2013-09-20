"""
File: buttondemo.py
Author: Kenneth A. Lambert
"""

from breezypythongui import EasyFrame
import math, thread
import time
class ButtonDemo(EasyFrame):
    """Illustrates command buttons and user events."""

    def __init__(self):
        """Sets up the window, label, and buttons."""
        EasyFrame.__init__(self)

        # A single label in the first row.
        self.label = self.addLabel(text = "Hello world!",
                                   row = 0, column = 0,
                                   columnspan = 2, sticky = "NSEW")

        # Two command buttons in the second row.
        self.clearBtn = self.addButton(text = "Clear",
                                       row = 1, column = 0,
                                       command = self.clear)
        self.restoreBtn = self.addButton(text = "Restore",
                                         row = 1, column = 1,
                                         command = self.restore,
                                         state = "disabled")
        #self.newWindow = tk
        self.app = CircleArea(self.newWindow)

    # Methods to handle user events.
    def clear(self):
        """Resets the label to the empty string and
        the button states."""
        self.label["text"] = ""
        self.clearBtn["state"] = "disabled"
        self.restoreBtn["state"] = "normal"

    def restore(self):
        """Resets the label to 'Hello world!'and sets
        the state of the buttons."""
        self.label["text"] = "Hello world!"
        self.clearBtn["state"] = "normal"
        self.restoreBtn["state"] = "disabled"

class CircleArea(EasyFrame):

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Circle Area")

        # Label and field for the area
        self.addLabel(text = "Area",
                      row = 0, column = 0)
        self.areaField = self.addFloatField(value = 0.0,
                                            row = 0,
                                            column = 1,
                                            width = 20)

        # Sliding scale for the radius
        self.radiusScale = self.addScale(label = "Radius",
                                         row = 1, column = 0,
                                         columnspan = 2,
                                         from_ = 0, to = 100,
                                         length = 300,
                                         tickinterval = 10,
                                         command = self.computeArea)


    # The event handler method for the sliding scale
    def computeArea(self, radius):
        """Inputs the radius, computes the area,
        and outputs the area."""
        # radius is the current value of the scale, as a string.
        area = float(radius) ** 2 * math.pi
        self.areaField.setNumber(area)

def start_button():
	ButtonDemo().mainloop()

def start_slider():
	CircleArea().mainloop()

# Instantiates and pops up the window.
if __name__ == "__main__":

	#th = thread.start_new_thread(start_button, ())
	#th2 = thread.start_new_thread(start_button, ())
	#th3 = thread.start_new_thread(start_button, ())
	#time.sleep(.1)
	#start_slider ()
	CircleArea().mainloop()
	#start_button()
