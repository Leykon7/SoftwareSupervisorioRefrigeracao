from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.properties import NumericProperty

class Interface(BoxLayout):
    """
    Widget Principal da Applicação
    """
    pass

class Helices(FloatLayout):
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
        super(Helices, self).__init__(**kwargs)
        anim = Animation(angle = 360, duration=2) 
        anim += Animation(angle = 360, duration=2)
        anim.repeat = True
        anim.start(self)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0