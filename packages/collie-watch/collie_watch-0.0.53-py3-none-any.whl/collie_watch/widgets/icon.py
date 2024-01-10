
from .menu_region import MenuRegion
from .scroll_view import ScrollView
from .alignment import CrossAxisAlignment, MainAxisAlignment
from .column import Column
from .button import Button
from .loader import Loader
from .text import Text
from .widget import Widget
from ..main_module import CollieWatch,CollieWatchHtmlEvents,CollieWatchHtmlInternalEvents
from typing import List
from .icons_list import *

class IconSize:
    SMALL = "fa-sm"
    MEDIUM = "fa-md"
    LARGE = "fa-lg"
    EXTRA_LARGE = "fa-xl"
    EXTRA_EXTRA_LARGE = "fa-2x"
    EXTRA_EXTRA_EXTRA_LARGE = "fa-3x"
    EXTRA_EXTRA_EXTRA_EXTRA_LARGE = "fa-4x"
    EXTRA_EXTRA_EXTRA_EXTRA_EXTRA_LARGE = "fa-5x"


class Icon(Widget):
    def __init__(self,icon_data="",size="fa-md",color="white",id=""):
        """
        Initialize a FileList widget.
        
        Arguments:
            id: An required identifier for the widget.

            
        """

        super().__init__(id)
        self.size = size
        self.color = color
        self.icon_data = icon_data
        

        
    
    def render(self):
        
        return f"""
        <i class="fa {self.icon_data} {self.size}" style="color: {self.color}"></i>
"""
