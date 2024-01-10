from .widget import Widget
from ..main_module import CollieWatch, CollieWatchHtmlEvents

class RadioButtonGroup(Widget):
    def __init__(self, label="", options={}, callback=lambda x: x, id=""):
        """
        Initializes a new instance of the RadioButton class.
        
        Args:
            name (str): The name attribute for the group of radio buttons. This ensures only one option in the group can be selected.
            
            options (dict, optional): A dictionary containing the radio button options.
                                      The keys are the option values and the corresponding values are the display texts.
                                      Defaults to an empty dictionary.

        Example:
            radio_button = RadioButton(name="color", options={
                "red": "Red",
                "blue": "Blue"
            })
            This will create a radio button group with two options: "Red" and "Blue".
        """
        super().__init__(id=id)
        self.label = label
        self.options = options

        for id, label in options.items():
            #print(f"{self.id}_{id}")
            CollieWatch.add_callback_by_id(f"{self.id}_{id}", [CollieWatchHtmlEvents.CLICK], callback)

    def render(self):
        title_html = f'<h3 style="font-weight: bold; margin-bottom: 0.5rem;">{self.label}</h3>' if self.label else ""
        options_html = "\n".join([
            f'<div style="display: flex; margin-bottom: 0.25rem; align-items: center;">'
            f'<input type="radio" id="{self.id}_{value}" name="{self.label}" value="{value}" style="margin: 0.5rem;">'
            f'<label for="{self.id}_{value}">{display}</label>'
            f'</div>'
            for value, display in self.options.items()])
        return f'<div style="display: grid; align-items: center; margin-bottom: 0.5rem;">' + title_html + options_html + "</div>"
