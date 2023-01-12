from kivy.app import App
from interface import Interface
from kivy.lang.builder import Builder
from kivy.core.window import Window

class Principal(App):
    """
    Classe com o aplicativo
    """
    def build(self):
        """
        Método para construção do aplicativo com base no widget criado
        """
        self._widget = Interface()
        return self._widget

if __name__ == '__main__':
    #Window.size=(1280, 720)
    #Window.resizable=False
    Window.fullscreen = 'auto'
    Builder.load_string(open("interface.kv",encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("popups.kv",encoding="utf-8").read(),rulesonly=True)
    Principal().run()
