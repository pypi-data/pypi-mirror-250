
from .widget import Widget


class Center(Widget):
    def __init__(self, child=None, id=""):
        super().__init__(id=id)
        self.child = child

    def render(self):
        child_html = self.child.render() if self.child else ""
        return f'''
            <div id="{self.id}" style="display: flex; align-items: center; justify-content: center; height: 100%;">
                {child_html}
            </div>
        '''
