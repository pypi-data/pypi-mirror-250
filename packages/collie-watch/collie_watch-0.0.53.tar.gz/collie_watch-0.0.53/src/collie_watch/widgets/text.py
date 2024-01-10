
from .widget import Widget

class Text(Widget):
    def __init__(self,text="",id=""):
        super().__init__(id=id)
        self.text = text

    def render(self):
        return f'<span id="{self.id}">{self.text}</span>'
    
    