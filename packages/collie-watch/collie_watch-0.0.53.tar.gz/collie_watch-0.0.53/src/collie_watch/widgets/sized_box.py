from .widget import Widget

class SizedBox(Widget):
    def __init__(self,child="", width="", height="",flex="", id=""):
        super().__init__(id=id,flex=flex)
        self.width = width
        self.height = height
        self.child = child

    def render(self):
        return f'''<div id="{self.id}" style="
        {"flex: {};".format(self.flex) if self.flex != "" else ""}
        overflow-wrap: break-word;
        {"width: {};".format(self.width) if self.width != "" else ""}
        {"height: {};".format(self.height) if self.height != "" else ""}">
        {self.child.render() if isinstance(self.child,Widget) else self.child}
        </div>'''
