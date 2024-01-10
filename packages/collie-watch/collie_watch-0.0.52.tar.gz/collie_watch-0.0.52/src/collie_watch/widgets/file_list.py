
from .container import Container,BoxDecoration
from .sized_box import SizedBox
from ..utils import Utils
from .row import Row
from .icon import Icon, IconSize
from .icons_list import Icons
from .menu_region import MenuItem, MenuRegion
from .scroll_view import ScrollView
from .alignment import CrossAxisAlignment, MainAxisAlignment
from .column import Column
from .button import Button
from .loader import Loader
from .text import Text
from .widget import Widget
from ..main_module import CollieWatch,CollieWatchHtmlEvents,CollieWatchHtmlInternalEvents
from typing import List
import os

class FileListItem:
    def __init__(self,file_name="",context_menu_items: List[MenuItem]=[]):

        for i in context_menu_items:
            if not type(i) == MenuItem:
                raise Exception("All items in context_menu_items must be of type MenuItem")

        self.file_name = file_name
        self.context_menu_items = context_menu_items
        self.file_id = Utils.generate_random_id()

    


class FileList(Widget):
    def __init__(self,file_list: List[FileListItem],file_icon: Widget=Icon(Icons.FILE,size=IconSize.EXTRA_LARGE,color="white"),id=""):
        """
        Initialize a FileList widget.
        
        Arguments:
            id: An required identifier for the widget.

            
        """

        super().__init__(id)
        self.file_icon = file_icon
        self.file_list = file_list
        
        
 
        
    
    def render(self):
        return Container(
        id=self.id,
        padding="10px",
        decoration=BoxDecoration(
            border="solid white 1px",
            border_radius="5px",
        ),child=ScrollView(
            child=Row(
                wrap=True,
                children=[
                    i for file in self.file_list for i in [
                        SizedBox(
                            width="10rem",
                            child= MenuRegion(
                            menu_items=file.context_menu_items,
                            child=Column(
                                crossAxisAlignment=CrossAxisAlignment.CENTER,
                                children=[
                                    self.file_icon,
                                    Text(
                                        text=file.file_name,
                                        id=f"file_list_item_{file.file_id}",
                                    ),
                                ]
                            )
                        )
                    ),SizedBox(
                        width="10px"
                    )
                    ]
                ]
            ),
        )).render()

