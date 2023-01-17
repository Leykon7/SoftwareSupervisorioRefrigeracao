from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.utils import escape_markup
from kivy.uix.slider import Slider
from kivy.app import App

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
        self._infoLabel = Label(text='[b][color=ff3333]'+escape_markup(mensagem)+'[/color][/b]',font_size=42, markup=True)
        self._info.setInfoLabel(self._infoLabel)
        self._info.ids.info.add_widget(self._infoLabel)
        self._info.open()

    # def conexao(self):
    #     if self.ids.conBut.text =='Conectar':
    #         pass

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
    _opcMainBox = None
    def porOpcoes(self, tipo):
        self.limparOpc()
        self._opcGrid = GridLayout(rows=2,cols=2,padding=7,spacing=7)
        self._opcGrid.add_widget(Label(id='acc', text='[color=62718e]ACC (mín. 10s e máx. 60s)[/color]', markup=True))
        self._opcGrid.add_widget(TextInput(halign='center',valign = 'middle',size_hint_x=0.4, center_x=0.5, center_y=0.5))
        self._opcGrid.add_widget(Label(id='dcc', text='[color=62718e]DCC (mín. 10s e máx. 60s)[/color]', markup=True))
        self._opcGrid.add_widget(TextInput(halign='center',valign = 'middle',size_hint_x=0.4, center_x=0.5, center_y=0.5))

        self._opcBox = BoxLayout(size_hint_y=0.5, center_x=0.1,center_y=0.5, spacing=7)
        self._opcBox.add_widget(Label(text='[color=62718e]Velocidade[/color]', markup=True))
        self._opcBox.add_widget(TextInput(id='vel',halign='center',valign = 'middle', size_hint_y=0.75,size_hint_x=0.3, right=0.5))

        self._opcMainBox = BoxLayout(orientation='vertical',spacing=7)
        self._opcMainBox.add_widget(self._opcGrid)
        if tipo:
            self._opcMainBox.add_widget(Slider(orientation='horizontal', min=0, max=100, step=1, size_hint_y=0.25))
        self._opcMainBox.add_widget(self._opcBox)
        self.ids.opcoes.add_widget(self._opcMainBox)

    def limparOpc(self):
        if self._opcMainBox is not None:
            self.ids.opcoes.remove_widget(self._opcMainBox)

    def partida(self, tipo):
        gui = App.get_running_app().root.ids.gui
        gui.parent.Partida(tipo)

    def comandoMotor(self,acao):
        pass

class TempRSTCar(Popup):
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