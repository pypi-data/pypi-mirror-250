from .widget import Widget
from ..main_module import CollieWatch,CollieWatchHtmlEvents

class TextField(Widget):
    def __init__(self, placeholder="", callback=lambda x: x, id=""):
        """
        Initializes a new instance of the TextField class.
        
        Args:
            placeholder (str, optional): A placeholder text that provides a brief hint to the user about what the input field expects.
                                         It gets displayed in the input field before the user enters a value.
                                         Defaults to an empty string.

        Example:
            textfield = TextField(placeholder="Enter your name")
            This will create a text field with the placeholder "Enter your name".
        """
        super().__init__(id=id)
        self.placeholder = placeholder

        CollieWatch.add_callback_by_id(self.id,[CollieWatchHtmlEvents.INPUT], callback)

    def render(self):
        return f'<input type="text" id="{self.id}" placeholder="{self.placeholder}">'
