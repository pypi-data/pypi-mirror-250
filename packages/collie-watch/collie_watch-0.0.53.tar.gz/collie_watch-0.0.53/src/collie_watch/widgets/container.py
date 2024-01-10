from .widget import Widget

class BoxDecoration:
    def __init__(self, color=None, border=None,border_radius=None):
        self.color = color
        self.border = border
        self.border_radius = border_radius

    def render(self):
        styles = []

        if self.color:
            styles.append(f"background-color: {self.color};")
        
        if self.border:
            styles.append(f"border: {self.border};")
        if self.border_radius:
            styles.append(f"border-radius: {self.border_radius};")

        return " ".join(styles)


class Container(Widget):
    def __init__(self, child=None, padding="0", margin="0",flex="", decoration=None, id=""):
        super().__init__(id=id,flex=flex)
        self.child = child
        
        self.padding = padding
        self.margin = margin
        self.decoration = decoration

    def render(self):
        child_html = self.child.render() if self.child else ""
        
        decoration_styles = self.decoration.render() if self.decoration else ""

        return f'''
            <div id="{self.id}" style="
            {'flex: {};'.format(self.flex) if self.flex != "" else ""}
            padding: {self.padding};
            margin: {self.margin}; 
            {decoration_styles}">
                {child_html}
            </div>
        '''
