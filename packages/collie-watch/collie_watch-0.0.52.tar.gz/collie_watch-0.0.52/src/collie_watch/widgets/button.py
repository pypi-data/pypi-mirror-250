
from ..utils import Utils
from .widget import Widget
from ..main_module import CollieWatch,CollieWatchHtmlEvents

class Button(Widget):
    def __init__(self, child: Widget,callback=None,id="",width="",height="",flex=""):
        id = id if id != "" else Utils.generate_random_id()
        super().__init__(id=id,flex=flex)
        self.child = child
        self.callback = callback

        
        if id != "" and callback != None:
            CollieWatch.add_callback_by_id(self.id,[CollieWatchHtmlEvents.CLICK],self.callback)

        
    def render(self):
        if self.callback == None:
            return f'<div class="button_like">{self.child.render() if isinstance(self.child,Widget) else self.child}</div>'
        return f'<button id="{self.id}">{self.child.render() if isinstance(self.child,Widget) else self.child}</button>'
