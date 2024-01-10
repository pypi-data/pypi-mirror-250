from .alignment import CrossAxisAlignment, MainAxisAlignment
from .widget import Widget


class Row(Widget):
    def __init__(self, children=[], id="", flex="", 
                 wrap=False,
                 mainAxisAlignment="", 
                 crossAxisAlignment=""):
        """
        Initialize a Row widget.

        :param children: List of child widgets to be displayed in this row.
        :type children: list of Widget
        :param id: An optional identifier for the widget.
        :type id: str
        :param flex: The flex attribute for the widget, determining how it'll grow in relation to its siblings in a flex container.
        :type flex: str
        :param mainAxisAlignment: Alignment of children along the row's main axis (horizontal).
                                   Accepts values from MainAxisAlignment class constants.
        :type mainAxisAlignment: str
        :param crossAxisAlignment: Alignment of children along the row's cross axis (vertical).
                                   Accepts values from CrossAxisAlignment class constants.
        :type crossAxisAlignment: str
        """
        super().__init__(id=id, flex=flex)
        self.wrap = wrap
        self.children = children
        self.mainAxisAlignment = mainAxisAlignment
        self.crossAxisAlignment = crossAxisAlignment

    def render(self):
        return f'''<div id="{self.id}" style="
        {'flex: {};'.format(self.flex) if self.flex != "" else ""}
        display: flex;
        {"flex-wrap: wrap;" if self.wrap else ""}
        flex-direction: row;
        {"justify-content: {};".format(self.mainAxisAlignment) if self.mainAxisAlignment != "" else ""}
        {"align-items: {};".format(self.crossAxisAlignment) if self.crossAxisAlignment != "" else ""}">
            {" ".join([child.render() for child in self.children])}
        </div>'''.strip()
