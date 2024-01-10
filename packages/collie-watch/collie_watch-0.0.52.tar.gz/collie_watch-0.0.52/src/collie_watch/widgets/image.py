
from .widget import Widget
from ..main_module import CollieWatch,CollieWatchHtmlEvents

class Image(Widget):
    def __init__(self,src,id="",width="100%",height=""):
        """
        An Image. If height is not specified, it will be set to auto.
        """
        super().__init__(id=id,flex="")
        
        self.src = src
        self.height = height if height != "" else "auto"
        self.width = width

        
    def render(self):
        return '<img id="{}" src="{}" width="{}" height="{}"/>'.format(self.id,self.src,self.width,self.height)
