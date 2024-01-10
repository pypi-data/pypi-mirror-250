
from .widget import Widget
from ..main_module import CollieWatch,CollieWatchHtmlEvents

class Loader(Widget):
    def __init__(self,width="2rem"):
        """
        A loader that spins forever.
        """
        super().__init__(id="",flex="")
        
        self.width = width

        
    def render(self):
        return '<race-by-loader color="var(--kPrimary)"' + ' size={}/>'.format('"' + self.width + '"')
