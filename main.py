import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

class MyWidget(BoxLayout):
    pass

class InterfaceApp(App):
    def build(self):
        """
        Método para construção do aplicativo com base no widget criado
        """
        return MyWidget()
 
if __name__ == '__main__':
    Config.set('graphics','resizable',True)
    InterfaceApp().run()