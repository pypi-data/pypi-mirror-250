
import inspect
from ..utils import Utils
from .alignment import CrossAxisAlignment, MainAxisAlignment
from .column import Column
from .button import Button
from .loader import Loader
from .text import Text
from .widget import Widget
from ..main_module import CollieWatch,CollieWatchHtmlEvents,CollieWatchHtmlInternalEvents

class FileInput(Widget):
    def __init__(self,callback,callback_for_file_chunk_received=lambda ev: None,id="",flex="",file_types=[],label=Button(child=Text("Upload File"))):
        """
        Initialize a FileInput widget.
        
        Arguments:
            id: An required identifier for the widget.

            flex: The flex attribute for the widget, determining how it'll grow in relation to its siblings in a flex container.

            file_types: A list of file types to accept. For example, ["image/png","image/jpeg"]. You can also use file extensions, like [".png",".jpg"].
        
            label: The label for the file input. Can be a string or a Widget.

            callback: The callback to be called when the file is uploaded. The callback will be called with the RECEIVED_FILE event as the first argument.
        """
        
        id = id if id != "" else Utils.generate_random_id()
        super().__init__(id,flex)

    
        self.callback_for_file_chunk_received = callback_for_file_chunk_received
        self.callback = callback
        self.file_types = file_types
        self.__updating = False
        self.label = label
        self.old_label = label

        if id != "":
            CollieWatch.add_callback_by_id(self.id + "_file_input",[CollieWatchHtmlInternalEvents.SENDING_FILE_CHUNK],self.__callback_on_file_chunk_received)
            CollieWatch.add_callback_by_id(self.id + "_file_input",[CollieWatchHtmlEvents.RECEIVED_FILE],self.__callback_on_file_received)
        else:
            raise Exception("FileInput must have an id")
    def __callback_on_file_chunk_received(self,event):
        
        self.callback_for_file_chunk_received(event)
        if not self.__updating:
            self.__updating = True

            print(list(event.keys()))

            html = Column(crossAxisAlignment=CrossAxisAlignment.CENTER,id=self.id + "_label",children=[
                Text("Uploading File"),
                Text( str(event["progress"]) + "% Done",id=self.id + "_progress"),
                Loader()
            ]).render()
            self.old_label = self.label

            CollieWatch.replace_html_element_by_id(self.id + "_label",html)
        else:
            CollieWatch.replace_html_element_by_id(self.id + "_progress",Text(str(event["progress"]) + "% Done",id=self.id + "_progress"))

    def __callback_on_file_received(self,event):
        
        if self.__updating:
            CollieWatch.replace_html_element_by_id(self.id + "_label",self.old_label.render() if isinstance(self.old_label,Widget) else self.old_label)
            self.__updating = False

        if len(inspect.signature(self.callback).parameters) > 0:
            self.callback(event)
        else:
            print("Warning: FileInput callback does not accept any arguments. The received file will be discarded.")


        
    def render(self):
        return f"""
    <div id="{self.id}_file_input">
    <label for="{self.id}_input"><div id="{self.id}_label">{self.label if not isinstance(self.label,Widget) else self.label.render()}</div></label>
    <input style="display: none;" type="file" id="{self.id}_input" accept="{' '.join(self.file_types)}">
    </div>
"""
