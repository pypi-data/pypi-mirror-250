
from .widget import Widget

class HorizontalFilledPill(Widget):
    def __init__(self,max_fill=100,current_fill=0,min_fill = 0,id="",width="100%",height="1rem",flex="",current_label_transform=  lambda x: x, max_label_transform = lambda x: x,min_label_transform = lambda x: x):
        """
        A loader that spins forever.
        """
        super().__init__(id=id,flex=flex)
        
        self.max_fill = max_fill
        self.min_fill = min_fill
        self.current_fill = current_fill
        self.height = height
        self.width = width
        self.current_label_transform = current_label_transform
        self.max_label_transform = max_label_transform
        self.min_label_transform = min_label_transform

        
    def render(self):
        return """
        <div style="width: {}; margin-top: 1rem; margin-bottom: 1rem;">
            <div style="width: 100%; height: 2rem">
            <p style="text-align: left; margin-left: calc({}% - 0.5rem)">{}</p>
            </div>
            <div style="">
            <horizontal-filled-pill percentage="{}" height="{}" width="100%"></horizontal-filled-pill>
            </div>
            <div style="justify-content: space-between; display: flex;">
            <span style="text-align: left">{}</span>
            <span style="text-align: right">{}</span>
            </div>
        </div>
""".format(self.width,self.current_fill/self.max_fill*100,self.current_label_transform(self.current_fill),self.current_fill/self.max_fill*100,self.height,self.min_label_transform(self.min_fill),self.max_label_transform(self.max_fill))
