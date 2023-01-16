from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.properties import NumericProperty
import popups
#from popups import comandoVent,medidasVent, comandoComp, ModbusPopup, ScanPopup, medidasComp, inversor, info
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread
from time import sleep
import datetime

class Interface(BoxLayout):
    """
    Widget Principal da Applicação
    """
    _updateThread = None
    _updateWidgets = True
    _tags = {}

    def __init__(self, **kwargs):
        super().__init__()
        self._scan_time = kwargs.get('scan_time')
        self._serverIP = kwargs.get('server_ip')
        self._port = kwargs.get('server_port')
        self._ModbusPopup = popups.ModbusPopup(self._serverIP,self._port)
        self._ScanPopup = popups.ScanPopup(self._scan_time)

        self._ClienteModbus = ModbusClient(host=self._serverIP, port=self._port)
        # self._medidas = {}
        # self._medidas['Timestamp']=None
        # self._medidas['Valores']=None
        # for key,value in kwargs.get('modbus_enderecos').items():
        #     if key == 'fornalha':
        #         cor_plot = (1,0,0,1)
        #     else:
        #         cor_plot =(0,1,0,1)
        #     self._tags[key] = {'endereco': value, 'color': cor_plot}

        self._comandoVent = popups.comandoVent()
        self._medidasVent = popups.medidasVent()
        self._medidasComp = popups.medidasComp()
        self._comandoComp = popups.comandoComp()
        #self._inversor = popups.inversor()
    
    def iniciaColetaDados(self,ip,port):
        """
        Método para configurar ip e porta e inicializar a thread de leitura dos dados
        """
        self._serverIP = ip
        self._port = port
        self._ClienteModbus.host = self._serverIP
        self._ClienteModbus.port = self._port
        try:
            Window.set_system_cursor('wait')
            self._ClienteModbus.open()
            Window.set_system_cursor('arrow')
            if self._ClienteModbus.is_open():
                self._updateThread = Thread(target=self.atualizador)
                self._updateThread.start()
                self.ids.conexa.text = 'CONECTADO'
                self._ModbusPopup.dismiss()
            else:
                self._ModbusPopup.porInfo('FALHA NA CONEXÃO!')
        except Exception as e:
            print("Erro", e.args)
            self._ModbusPopup.porInfo('FALHA NA CONEXÃO!')

    def atualizador(self):
        """
        Metodo que invoca leitura dos dados, atualização de interface e inserção no banco de dados
        """
        try:
            while self._updateWidgets:
                self.lerDados()
                self.atualizaInterface()
                #Inserir no banco de dados
                sleep(self._scan_time/1000)
        except Exception as e:
            self._ClienteModbus.close()
            print('Erro', e.args)



    def lerDados(self):
        """
        Metodo de leitura de dados pelo protocolo modbus
        """
        # self._medidas['Timestamp'] = datetime.now()
        # for key,value in self._tags.items():
        #     self._medidas['valores'][key] = self._ClienteModbus.read_holding_register(value['endereco'],1)[0]

    def atualizaInterface(self):
        """
        Método que atualiza a interface gráfica a partir dos dados lidos
        """
        # for key,value in self._tags.items():
        #         self.ids[key].text = str(self.medidas['values'][key])+'ºC'



    def venezianas(self, *args):
        self.ids.veneziana1.angle = args[1]
        self.ids.veneziana2.angle = args[1]
        self.ids.veneziana3.angle = args[1]
    
    def checkboxes(self,vent):
        if vent == 1:
            self.ids.helice0.source ='imgs/helicebaixadaAzul.png'
            self.ids.helice1.source ='imgs/helicebaixadaBrancasvg.png'
            self.ids.hel0.start()
            self.ids.hel1.stop()
        elif vent == 0:
            self.ids.helice1.source ='imgs/helicebaixadaAzul.png'
            self.ids.helice0.source ='imgs/helicebaixadaBrancasvg.png'
            self.ids.hel1.start()
            self.ids.hel0.stop()
    def teste(self):
        print(self.ids.tamanho.size)

class Helices(FloatLayout):
    """
    Widget derivado da classe FloatLayout para fazer hélices girantes 
    """
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
        super(Helices, self).__init__(**kwargs)
        self.anim = Animation(angle = 360, duration=2) 
        self.anim += Animation(angle = 360, duration=2)
        self.anim.repeat = True
        # anim.start(self)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0
        
    def start(self):
        self.anim.start(self)

    def stop(self):
        self.anim.stop(self)
        self.angle = 0