from ..utils import *


class Widget:

    def __init__(self,id="",flex="") -> None:
        self.id = id if id != "" else Utils.generate_random_id()
        self.flex = flex

    def render(self) -> str:
        """
        Generates and returns the HTML representation of the widget.
        """
        return ""
