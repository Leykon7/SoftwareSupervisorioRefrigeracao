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
from datetime import datetime
import random
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
#from pymodbus.payload import BinaryPayloadBuilder


class Interface(BoxLayout):
    """
    Widget Principal da Applicação
    """
    _updateThread = None
    _updateWidgets = True
    _tags = {} #teste
    _tagsValvula4X = {}
    _tagsTelaFP = {}
    _tagsPartida4X = {}
    _tagsMotor4X = {}

    def __init__(self,**kwargs):
        super().__init__()
        #Pega info
        self._scan_time = kwargs.get('scan_time')
        self._serverIP = kwargs.get('server_ip')
        self._port = kwargs.get('server_port')

        #Cliente Modbus
        self._ClienteModbus = ModbusClient(host=self._serverIP, port=self._port)

        #Leituras
        self._medidasTela = {}
        self._medidasTela['Timestamp']=None
        self._medidasTela['Valores']={}
        self._valvulas = {}
        self._valvulas['Leitura']={}

        ##Dá cor e salva no dict _tags
        """ cor_plot =(random.random(),random.random(),random.random(),1)
                self._tags[key] = {'endereco': value, 'color': cor_plot} """
        for key, value in kwargs.get('endTelaFP').items():
            cor_plot=(random.random(),random.random(),random.random(),1)
            self._tagsTelaFP[key] = {'endereco': value, 'color': cor_plot}

        for key, value in kwargs.get('endValvulas4X').items():
            self._tagsValvula4X[key] = value

        for key, value in kwargs.get('endPartida4X').items():
            self._tagsPartida4X[key] = value

        for key, value in kwargs.get('endMotor4X').items():
            self._tagsMotor4X[key] = value

        #Popups
        self._ModbusPopup = popups.ModbusPopup(self._serverIP,self._port)
        self._ScanPopup = popups.ScanPopup(self._scan_time)
        self._comandoVent = popups.comandoVent()
        self._medidasTelaVent = popups.medidasVent()
        self._medidasTelaComp = popups.medidasComp()
        self._comandoComp = popups.comandoComp()
        #self._inversor = popups.inversor()
                
    _teste = False
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
            if self._ClienteModbus.is_open:
                self._updateThread = Thread(target=self.atualizador)
                self._updateThread.start()
                self.ids.conexao.text = 'CONECTADO'
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
        Atualiza o atributo medidas
        """
        #Dados da tela
        self._medidasTela['Timestamp'] = datetime.now()
        for key,value in self._tagsTelaFP.items():
            leitura = self._ClienteModbus.read_holding_registers(value['endereco'],2)
            decoder = BinaryPayloadDecoder.fromRegisters(leitura, byteorder=Endian.Big, wordorder=Endian.Little)
            self._medidasTela['Valores'][key] = decoder.decode_32bit_float()
            
        #Leitura das Valvulas
        for key, value in self._tagsValvula4X.items():
            leitura = self._ClienteModbus.read_holding_registers(value,1)[0]
            self._valvulas['Leitura'][key] = leitura
            
    def Partida(self,tipo):
        if tipo == 1: #soft
            self._ClienteModbus.write_single_register(self._tagsPartida4X['ve.sel_driver'],1) 
        elif tipo == 2: #inversor
            self._ClienteModbus.write_single_register(self._tagsPartida4X['ve.sel_driver'],2)
        elif tipo == 3: #direta
            self._ClienteModbus.write_single_register(self._tagsPartida4X['ve.sel_driver'],3) 

    def comandoMotor(self,comando):
        if comando ==0: #desligar
            self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.atv31'],0) 
            self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.ats48'],0) 
            self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.tesys'],0) 

        elif comando == 1: #ligar
            if self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.atv31'],0) and self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.ats48'],0) and self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.tesys'],0):
                self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.atv31'],0) 
                self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.ats48'],0) 
                self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.tesys'],0) 

            if self._ClienteModbus.read_holding_registers(self._tagsPartida4X['ve.indica_driver'],1)[0] == 1:
                self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.ats48'],1)
            elif self._ClienteModbus.read_holding_registers(self._tagsPartida4X['ve.indica_driver'],1)[0] == 2:
                self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.atv31'],1) 
            elif self._ClienteModbus.read_holding_registers(self._tagsPartida4X['ve.indica_driver'],1)[0] == 3:
                self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.tesys'],1) 
        
        elif comando == 2: #resetar
            self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.atv31'],2) 
            self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.ats48'],2) 
            self._ClienteModbus.write_single_register(self._tagsMotor4X['ve.tesys'],2)    
        
        #Exemplo de leitura FP
        """
        if tipo == 1:  #Float
            leitura = self._cliente.read_holding_registers(addr, 2)
            decoder = BinaryPayloadDecoder.fromRegisters(leitura, byteorder=Endian.Big, wordorder=Endian.Little)
            return decoder.decode_32bit_float()
        """
        #Exemplo de leitura 4X
        """"
        #return self._cliente.read_holding_registers(addr,1)[0]

        """

    def atualizaInterface(self):
        """
        Método que atualiza a interface gráfica a partir dos dados lidos
        """
        #Medidas da tela
        self.ids.pit1.text =str((self._medidasTela['Valores']['ve.pit01'])/10)+' Psi'
        self.ids.pit2.text =str((self._medidasTela['Valores']['ve.pit02'])/10)+' Psi'
        self.ids.pit3.text =str((self._medidasTela['Valores']['ve.pit03'])/10)+' Psi'
        self.ids.tit1.text =str((self._medidasTela['Valores']['ve.tit01'])/10)+' ºC'
        self.ids.tit2.text =str((self._medidasTela['Valores']['ve.tit02'])/10)+' ºC'
        self.ids.tit3.text =str(round(self._medidasTela['Valores']['ve.temperatura'],2))+' ºC'
        self.ids.vazao.text =str(self._medidasTela['Valores']['ve.vazao'])+' m³/h'
        self.ids.vel.text =str(self._medidasTela['Valores']['ve.velocidade'])+' m/s'

        #Valvulas
        if self._valvulas['Leituras']['ve.xv_scroll.0'] == 0:
            self.ids.xv1.source = 'imgs/ValvulaAzul.png'
            self.ids.xv3.source = 'imgs/ValvulaAzul.png'
        elif self._valvulas['Leituras']['ve.xv_hermetico.1']==1:
            self.ids.xv2.source = 'imgs/ValvulaAzul.png'
            self.ids.xv4.source = 'imgs/ValvulaAzul.png'
        else:
            self.ids.xv1.source = 'imgs/ValvulaBranca.png'
            self.ids.xv3.source = 'imgs/ValvulaBranca.png'
            self.ids.xv2.source = 'imgs/ValvulaBranca.png'
            self.ids.xv4.source = 'imgs/ValvulaBranca.png'
            
        if self._valvulas['Leituras']['ve.xv5.7'] == 1:
            self.ids.xv5.source = 'imgs/ValvulaAzul.png'
        else:
            self.ids.xv5.source = 'imgs/ValvulaBranca.png'
            
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