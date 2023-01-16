from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.utils import escape_markup

class ModbusPopup(Popup):
    """
    popup para conectar no servidor
    """
    _infoLabel = None
    def __init__(self,ip,porta,**kwargs):
        super().__init__(**kwargs)
        self._info = info()
        self.ids.txt_ip.text=str(ip)
        self.ids.txt_porta.text=str(porta)

    def porInfo(self, mensagem):
        self._infoLabel = Label(text='[b][color=ff3333]'+escape_markup(mensagem)+'[/color][/b]', markup=True)
        self._info.setInfoLabel(self._infoLabel)
        self._info.ids.info.add_widget(self._infoLabel)
        self._info.open()

class info(Popup):
    """
    Popup de informação sobre a conexão
    """
    _infoLabel = None
    def setInfoLabel(self, info):
        self._infoLabel = info

    def limparInfo(self):
        if self._infoLabel is not None:
            self.ids.info.remove_widget(self._infoLabel)

class ScanPopup(Popup):
    """
    popup para conectar no servidor
    """
    def __init__(self,scantime,**kwargs):
        super().__init__(**kwargs)
        self.ids.txt_st.text=str(scantime)
    pass

class comandoVent(Popup):
    """
    Comandos dos Ventiladores
    """
    def __init__(self, **kwargs):
        super().__init__()
        self._inversor = inversor()
    pass

class comandoComp(Popup):
    """
    Comandos do Scroll e Hermético
    """
    pass

class medidasVent(Popup):
    """
    Medidas dos Ventiladores
    """
    def teste(self):
        self.ids.tensaoMVent.text = '0 V'

class medidasComp(Popup):
    """
    Medidas dos Ventiladores
    """
    pass

class inversor(Popup):
    """
    Configurações do Inversor
    """
    pass