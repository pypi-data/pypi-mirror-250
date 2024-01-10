
from .widget import Widget
from ..main_module import CollieWatch,CollieWatchHtmlEvents

class Dropdown(Widget):
    def __init__(self, options={},callback=lambda x: x,id=""):
        """
        Initializes a new instance of the Dropdown class.
        
        Args:
            options (dict, optional): A dictionary containing the options to be displayed in the dropdown.
                                     The keys are the option values and the corresponding values are the display texts.
                                     Defaults to an empty dictionary.

        Example:
            dropdown = Dropdown(options={
                "value1": "Option 1",
                "value2": "Option 2"
            })
            This will create a dropdown with two options: "Option 1" and "Option 2" having respective values "value1" and "value2".
        """
        super().__init__(id=id)
        self.options = options

        CollieWatch.add_callback_by_id(self.id,[CollieWatchHtmlEvents.CLICK],callback)

    def render(self):
        options_html = " ".join([f'<option value="{value}">{display}</option>' for value, display in self.options.items()])
        return f'<select id="{self.id}">{options_html}</select>'
