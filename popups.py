from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.utils import escape_markup
from kivy.uix.slider import Slider
from kivy.app import App
from kivy.garden.graph import Graph, MeshLinePlot
from modbuspersistencia import Persistencia
import random

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
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._ats = ats48()
        self._atv = atv31()

    def porOpcoes(self, tipo):
        self.limparOpc()
        if tipo == False:
            self.ids.opcoes.add_widget(self._ats)
        elif tipo == True:
            self.ids.opcoes.add_widget(self._atv)

    def limparOpc(self):
        self.ids.opcoes.remove_widget(self._ats)
        self.ids.opcoes.remove_widget(self._atv)

    def partida(self, tipo):
        gui = App.get_running_app().root.ids.gui
        gui.parent.Partida(tipo)

class TempRSTCar(Popup):
    pass
    
class comandoComp(Popup):
    """
    Comandos do Scroll e Hermético
    """
    _slider = None
    def porOpc(self):
        self.limparOpc()
        self._slider = Slider(orientation='horizontal', size_hint_y=0.1, min=0, max=100, cursor_width=16, cursor_height=16)
        self.ids.compOnze.add_widget(self._slider)
    def limparOpc(self):
        if self._slider is not None:
            self.ids.compOnze.remove_widget(self._slider)
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

class ats48(BoxLayout):
    """
    Configurações da partida soft
    """

class atv31(BoxLayout):
    """
    configurações do inversor
    """
    def slider(self):
        self.ids.vel.text = str(float(self.ids.velslider.value))

    def atualizaslider(self):
        if self.ids.vel.text == '':
            self.ids.velslider.value = 0    
            self.ids.text = '0'
        elif int(float(self.ids.vel.text))>100:
             self.ids.velslider.value =100
        else:
            self.ids.velslider.value = int(float(self.ids.vel.text))    

class popupgrafico(Popup):
    """
    Popup do Grafico
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._graficoW = grafico()
        self.grafAdcnd = False
        self.plot1 = MeshLinePlot(color=[1,0,0,1])
        self.plot2 = MeshLinePlot(color=[0,1,0,1])
        self.plot3 = MeshLinePlot(color=[0,0,1,1])
    
    def addGrafico(self):
        if self.grafAdcnd:
            self.removeGrafico()
        self.ids.areagrafico.add_widget(self._graficoW)
        self.grafAdcnd = True

    def removeGrafico(self):
        if self.grafAdcnd:
            self.ids.areagrafico.remove_widget(self._graficoW)
       
        # Clock.schedule_interval(self.atualizaMylist, 1.)
        # Clock.schedule_interval(self.atualizaTamanho, 1.)
        # Clock.schedule_interval(self.update_points, 1.)
        # Clock.schedule_interval(self.update_xaxis, 1.)

class grafico(Graph):
    """
    grafico
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._plot = MeshLinePlot(color=[1, 0, 0, 1])
        self._tamnho = 0
        self._listtuple = []

    def update_xaxis(self):
        if (self.ids.grafico.xmax - self.ids.grafico.xmin)*(3/4) < self._tamnho:
            self.ids.grafico.xmax = self.ids.grafico.xmax + 1
            self.ids.grafico.xmin = self.ids.grafico.xmin + 1        

    def update_points(self,pontos):
        #self.plot.points = [(i,i)]
        #self.plot.points = [i for i in self._mylist]
        self._listtuple.append((self._tamnho,pontos[self._tamnho-1]))
        self._plot.points = self._listtuple
        self.ids.grafico.add_plot(self._plot)

    def atualizaTamanho(self,pontos):
        self._tamnho = len(pontos)

    def atualizadorGrafico(self,pontos):
        self.atualizaTamanho(pontos)
        self.update_points(pontos)
        self.update_xaxis()

class bdPopup(Popup):
    """
    Popup do Banco de dados
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._persistencia = Persistencia

    def printarTable(self):
        self.ids.table.text=self._persistencia.acesso_dados_historicos(self,self.ids.inicial.text, self.ids.final.text)