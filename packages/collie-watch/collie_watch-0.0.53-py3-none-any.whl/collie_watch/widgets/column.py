from .alignment import MainAxisAlignment,CrossAxisAlignment
from .widget import Widget


class Column(Widget):
    def __init__(self, children=[], id="", flex="", mainAxisAlignment="", crossAxisAlignment=""):
        """
        Initialize a Column widget.

        :param children: List of child widgets to be displayed in this column.
        :type children: list of Widget
        :param id: An optional identifier for the widget.
        :type id: str
        :param flex: The flex attribute for the widget, determining how it'll grow in relation to its siblings in a flex container.
        :type flex: str
        :param mainAxisAlignment: Alignment of children along the column's main axis (vertical).
                                   Can be one of "start", "end", "center", "space-between", "space-around", or "space-evenly".
                                   Use the MainAxisAlignmentClass constants to avoid typos.
        :type mainAxisAlignment: str
        :param crossAxisAlignment: Alignment of children along the column's cross axis (horizontal).
                                   Can be one of "start", "end", "center", or "stretch".
                                   Use the CrossAxisAlignmentClass constants to avoid typos.
        :type crossAxisAlignment: str
        """
        super().__init__(id=id, flex=flex)
        self.children = children
        self.mainAxisAlignment = mainAxisAlignment  # Can be "start", "end", "center", "space-between", "space-around"
        self.crossAxisAlignment = crossAxisAlignment  # Can be "start", "end", "center", "stretch"

    def render(self):


        return f'''<div id="{self.id}" style="
            {"flex: {};".format(self.flex) if self.flex != "" else ""}
            display: flex;
            flex-direction: column; 
            {"justify-content: {};".format(self.mainAxisAlignment) if self.mainAxisAlignment != "" else ""}
            {"margin: 0 auto;" if self.crossAxisAlignment == CrossAxisAlignment.CENTER else ""}
            {"align-items: {};".format(self.crossAxisAlignment) if self.crossAxisAlignment != "" else ""}"
            
            >{" ".join([child.render() for child in self.children])}</div>'''
