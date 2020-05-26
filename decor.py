from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.label import Label


class ResizableLabel(Label):
    def on_pos(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(153, 0, 204, 0.25)
            Rectangle(pos=self.pos, size=self.size)