from .widget import Widget

class Tooltip(Widget):
    def __init__(self, child, tooltip_text="", tooltip_position="top", id=""):
        super().__init__(id=id)
        self.child = child
        self.tooltip_text = tooltip_text
        self.tooltip_position = tooltip_position

    def render(self):
        return f'''
        <div style="--cooltipz-border-radius: 5px;--cooltipz-font-size: 1rem;--cooltipz-bg-color: #19D8A8" data-cooltipz-dir="{self.tooltip_position}" aria-label="{self.tooltip_text}"  id="{self.id}">
            {self.child.render() if isinstance(self.child, Widget) else self.child}
        </div>
        '''
