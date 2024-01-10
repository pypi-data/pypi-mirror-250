from ..utils import Utils
from .raw_html import RawHtml
from .tooltip import Tooltip
from .widget import Widget
from ..main_module import CollieWatch,CollieWatchHtmlEvents

class ScrollView(Widget):
    def __init__(self, child=None, width="100%", height="100%", flex="", id="",auto_scroll=False,auto_scroll_locked_initial_state=True):
        super().__init__(id=id, flex=flex)
        self.child = child
        self.width = width
        self.height = height
        self.auto_scroll = auto_scroll
        self.locked = None
        
        if auto_scroll:
            self.locked = auto_scroll_locked_initial_state

            CollieWatch.add_callback_by_id(f"auto-scroll-button-{self.id}-locked",[CollieWatchHtmlEvents.CLICK],self.handle_auto_scroll)
            CollieWatch.add_callback_by_id(f"auto-scroll-button-{self.id}-unlocked",[CollieWatchHtmlEvents.CLICK],self.handle_auto_scroll)
            CollieWatch.add_callback_by_id(f"inner-auto-scroll-button-{self.id}",[CollieWatchHtmlEvents.CLICK],self.handle_auto_scroll)
        
    def handle_auto_scroll(self,event_data):
        CollieWatch.replace_html_element_by_id(f"auto-scroll-button-{self.id}-{'locked' if self.locked else 'unlocked'}",f'''
                <button id="auto-scroll-button-{self.id}-{"unlocked" if self.locked else "locked"}"><i id="inner-auto-scroll-button-{self.id}" class="fas {"fa-unlock" if self.locked else "fa-lock"}"></i></button>
        ''')
        self.locked = not self.locked

    def render(self):
        child_html = self.child.render() if self.child else ""
        if self.auto_scroll != None:
            tooltip = Tooltip(
                tooltip_text="Lock/Unlock Auto Scroll",
                tooltip_position="left",
                child=RawHtml(
                    html= f'<button id="auto-scroll-button-{self.id}-{"locked" if self.locked else "unlocked"}"><i id="inner-auto-scroll-button-{self.id}" class="fas {"fa-lock" if self.locked else "fa-unlock"}"></i></button>'
                )
            )
            auto_scroll_child = tooltip.render() if self.auto_scroll else ""

            
            
        return f'''
            <div style="
            {"flex: {};".format(self.flex) if self.flex != "" else ""}
            width: {self.width}; 
            height: {self.height};
            display: flex; 
            flex-direction: row;">
                <div id="{self.id}" style="flex: 1; overflow: auto; flex-direction: column;">
                    {child_html}
                </div>
                <div>
                {auto_scroll_child}
                </div>
            </div>
        '''
