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
        self._widget = Interface(scan_time=1000,server_ip='10.15.20.17', server_port=10012)

        return self._widget
    
    def on_stop(self):
        self._widget.pararAtualizador()

if __name__ == '__main__':
    Window.size=(1080, 720)
    #Window.fullscreen = 'auto'
    Builder.load_string(open("interface.kv",encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("popups.kv",encoding="utf-8").read(),rulesonly=True)
    Principal().run()
