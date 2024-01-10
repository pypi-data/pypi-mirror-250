
from .widget import Widget

class RawHtml(Widget):
    def __init__(self,html="",):
        super().__init__(id="")
        self.html = html

    def render(self):
        return self.html
    
    