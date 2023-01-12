from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.properties import NumericProperty
from popups import comandoVent, comandoComp

class Interface(BoxLayout):
    """
    Widget Principal da Applicação
    """
    def __init__(self, **kwargs):
        super().__init__()
        self._comandoVent = comandoVent()
        self._comandoVent = comandoComp()

    def venezianas(self, *args):
        self.ids.veneziana1.angle = args[1]
        self.ids.veneziana2.angle = args[1]
        self.ids.veneziana3.angle = args[1]
    
    def checkboxes(self,vent):
        if vent == 0:
            pass
        elif vent == 1:
            pass

class Helices(FloatLayout):
    """
    Widget derivado da classe FloatLayout para fazer hélices girantes 
    """
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
        
        