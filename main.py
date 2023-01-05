from kivy.app import App
from interface import Interface
from kivy.lang.builder import Builder

class PrincipalApp(App):
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
    Builder.load_string(open("interface.kv",encoding="utf-8").read(),rulesonly=True)
    PrincipalApp().run()