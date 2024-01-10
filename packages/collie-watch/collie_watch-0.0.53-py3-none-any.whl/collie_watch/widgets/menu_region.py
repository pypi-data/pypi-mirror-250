
from collie_watch.utils import Utils
from .alignment import CrossAxisAlignment, MainAxisAlignment
from .column import Column
from .button import Button
from .loader import Loader
from .text import Text
from .widget import Widget
from ..main_module import CollieWatch,CollieWatchHtmlEvents,CollieWatchHtmlInternalEvents
from typing import List
import urllib.parse as parser

class MenuClickType:
    LEFT_CLICK = "left_click"
    RIGHT_CLICK = "right_click"

class MenuItem:
    def __init__(self,text,icon="fa-xmark",callback=lambda: None,color="#19d8a8"):
        self.text = text
        self.id = Utils.generate_random_id()
        self.callback = callback
        self.icon = icon
        self.color = color


class MenuRegion(Widget):
    def __init__(self,menu_items: List[MenuItem],child: Widget,click_type=MenuClickType.RIGHT_CLICK):
        """
        Initialize a FileList widget.
        
        Arguments:
            id: An required identifier for the widget.

            
        """
        id = Utils.generate_random_id()

        super().__init__(id)

        for item in menu_items:
            if not type(item) == MenuItem:
                raise Exception("All items in menu_items must be of type MenuItem")

        self.menu_items = menu_items
        self.click_type = click_type
        self.child = child


        if id != "":
            CollieWatch.add_callback_by_id(f"menu_region_{click_type}_{self.id}",[CollieWatchHtmlEvents.MENU_SELECTION],self.__on_click_on_menu_region)
        else:
            raise Exception("FileInput must have an id")

    def __on_click_on_menu_region(self,event):
        for item in self.menu_items:
            if item.id == event["menu_item_id"]:
                item.callback()    
   
    def render(self):
       
        return f"""
   
    <div id="menu_region_{self.click_type}_{self.id}" style="--menuItemsVariable={[{"text": parser.quote(i.text),"id": i.id,"icon":i.icon,"color":i.color} for i in self.menu_items].__repr__()};">
        {self.child.render()}
    </div>
"""
