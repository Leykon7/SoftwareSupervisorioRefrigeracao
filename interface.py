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
    _tagsTempeRSTCarFP = {}
    _tagsPartida4X = {}
    _tagsMotor4X = {}
    _tagsAqueUmidTermo4X={}
    _tagsVeneziana4X = {}

   

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
        self._medidasTempRSTCar = {}
        self._medidasTempRSTCar['Timestamp']=None
        self._medidasTempRSTCar['Valores']={}

         #escritas
        self._escritas = {}
        self._escritas['4X'] ={}
        self._escritas['FP'] ={}
        self._escritas['HRBits']={}

        #Leitura de status
        self._status = {}

        ### usar apenas duas bibliotecas, uma para ações e outra de leituras

        ##Dá cor e salva no dict _tags
        for key, value in kwargs.get('endTelaFP').items():
            cor_plot=(random.random(),random.random(),random.random(),1)
            self._tagsTelaFP[key] = {'endereco': value, 'color': cor_plot}
        
        for key, value in kwargs.get('endTempFP').items():
            cor_plot=(random.random(),random.random(),random.random(),1)
            self. _tagsTempeRSTCarFP[key] = {'endereco': value, 'color': cor_plot}

        for key, value in kwargs.get('endValvulas4X').items():
            self._tagsValvula4X[key] = value

        for key, value in kwargs.get('endPartida4X').items():
            self._tagsPartida4X[key] = value

        for key, value in kwargs.get('endMotor4X').items():
            self._tagsMotor4X[key] = value

        for key, value in kwargs.get('endAqueUmidTerm4X').items():
            self._tagsAqueUmidTermo4X[key] = value

        for key, value in kwargs.get('endVeneziana').items():
            self._tagsVeneziana4X[key] = value
        
        #Metodo de escrita e leitura
        self._conectaCLP = conectaCLP()

        #Popups
        self._ModbusPopup = popups.ModbusPopup(self._serverIP,self._port)
        self._ScanPopup = popups.ScanPopup(self._scan_time)
        self._comandoVent = popups.comandoVent()
        self._medidasTelaVent = popups.medidasVent()
        self._medidasTelaComp = popups.medidasComp()
        self._comandoComp = popups.comandoComp()
        self._tempRSTCar = popups.TempRSTCar()
                
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
                #self._ModbusPopup.ids.conBut.text='Desconectar'
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
                self.escreveDados()
                #guardar todas escritas num dict por meio de um método
                #Inserir no banco de dados
                sleep(self._scan_time/1000)
        except Exception as e:
            self._ClienteModbus.close()
            self.ids.conexao.text = 'ERRO! DESCONECTADO'
            print('Erro', e.args)

    def pararAtualizador(self):
        self._updateWidgets = False

    def escreveDados(self):
        """
        Método que escreve todos os dados da iteração
        """
        for key,value in self._escritas['4X'].items():
            self._conectaCLP.escreve4x(self._ClienteModbus,int(key),value)
        for key,value in self._escritas['HRBits'].items():
            self._conectaCLP.escreveHRBits(self._ClienteModbus,int(key),value)   
        for key,value in self._escritas['FP'].items():
            self._conectaCLP.escreveFP(self._ClienteModbus,int(key),value)      

    def lerDados(self):
        """
        Metodo de leitura de dados pelo protocolo modbus
        Atualiza o atributo medidas
        """
        """
        _escritas = {'4X':{'1500':5, '329':1 ...}, 'FP':{'20':5.7, ...}}

        _tagsTelaFP= {'ve.pit': {'endereco': addr, 'color': cor_plot}

        _medidasTela = {'Valores':{'ve.pit': 200psi, 've.tit': 25}, 'Timestamp':[Lista]}
        
        _tagsValvulas4X = {'ve.pit':502,'ve.tit':504, ....}

        _valvulas = {'ve.xv':[0,0,1,0...], 've.xv':[0,0,1,0...], ...}
    
        """
        #Dados da tela
        self._medidasTela['Timestamp'] = datetime.now()
        for key,value in self._tagsTelaFP.items():
            self._medidasTela['Valores'][key] = self._conectaCLP.leFP(self._ClienteModbus,value['endereco'])
            
        #Leitura das Valvulas
        for key, value in self._tagsValvula4X.items():
            self._valvulas[key] = self._conectaCLP.leHRBits(self._ClienteModbus,value)

        #Leitura de temperatura dos enrolamentos do motor e carcaça
        self._medidasTempRSTCar['Timestamp'] = datetime.now()
        for key,value in self._tagsTempeRSTCarFP.items():
            self._conectaCLP.leHRBits(self._ClienteModbus,value['endereco'])
            self._medidasTempRSTCar['Valores'][key] = self._conectaCLP.leFP(self._ClienteModbus,value['endereco'])

        #Leitura do status do motor e do driver
        ####FAZER COM QUE AS LEITURAS QUE JÁ ESTÃO NA BANCADA APARECAM NO PROGRAMA
        self._status['driver'] = self._conectaCLP.le4X(self._ClienteModbus,1324)
        self._status['motorInversor'] = self._conectaCLP.le4X(self._ClienteModbus,1312)
        self._status['motorSoft'] = self._conectaCLP.le4X(self._ClienteModbus,1316)
        self._status['motorDireta'] = self._conectaCLP.le4X(self._ClienteModbus,1319)
        self._status['aqueUmi'] = self._conectaCLP.leHRBits(self._ClienteModbus, 1329)
        self._status['comp'] = self._conectaCLP.leHRBits(self._ClienteModbus, 1328)
        self._status['velScroll'] = self._conectaCLP.le4X(self._ClienteModbus, 1236)

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
        if self._valvulas['ve.xv_scroll.0'][1] == 1:
            self.ids.xv1.source = 'imgs/ValvulaAzul.png'
            self.ids.xv3.source = 'imgs/ValvulaAzul.png'
        elif self._valvulas['ve.xv_hermetico.1'][1]==1:
            self.ids.xv2.source = 'imgs/ValvulaAzul.png'
            self.ids.xv4.source = 'imgs/ValvulaAzul.png'
        else:
            self.ids.xv1.source = 'imgs/ValvulaBranca.png'
            self.ids.xv3.source = 'imgs/ValvulaBranca.png'
            self.ids.xv2.source = 'imgs/ValvulaBranca.png'
            self.ids.xv4.source = 'imgs/ValvulaBranca.png'
            
        if self._valvulas['ve.xv5.7'][7]== 1:
            self.ids.xv5.source = 'imgs/ValvulaAzul.png'
        else:
            self.ids.xv5.source = 'imgs/ValvulaBranca.png'

        #Temperaturas R, S, T e Carcaça
        self._tempRSTCar.ids.temp_r.text =str((self._medidasTempRSTCar['Valores']['ve.temp_r'])/10)+' ºC'
        self._tempRSTCar.ids.temp_s.text =str((self._medidasTempRSTCar['Valores']['ve.temp_s'])/10)+' ºC'
        self._tempRSTCar.ids.temp_t.text =str((self._medidasTempRSTCar['Valores']['ve.temp_t'])/10)+' ºC'
        self._tempRSTCar.ids.carcaca.text =str((self._medidasTempRSTCar['Valores']['ve.temp_carc'])/10)+' ºC'

    def Partida(self,tipo):
        if tipo == 1: #soft
            self._escritas['4X']['1324']=tipo
        elif tipo == 2: #inversor
            self._escritas['4X']['1324']=tipo
        elif tipo == 3: #direta
            self._escritas['4X']['1324']=tipo

    def comandoMotor(self,comando):
        if comando ==0: #desligar
            self._escritas['4X']['1312']=comando
            self._escritas['4X']['1316']=comando
            self._escritas['4X']['1319']=comando
        elif comando == 1: #ligar
            ### botar rendimento do motor
            #Trocar animação das helices
            if self._comandoVent.ids.axial.active:
                self.ids.helice0.source ='imgs/helicebaixadaAzul.png'
                self.ids.helice1.source ='imgs/helicebaixadaBrancasvg.png'
                self.ids.hel0.start()
                self.ids.hel1.stop() 
            elif self._comandoVent.ids.radial.active:
                self.ids.helice1.source ='imgs/helicebaixadaAzul.png'
                self.ids.helice0.source ='imgs/helicebaixadaBrancasvg.png'
                self.ids.hel1.start()
                self.ids.hel0.stop()

            #se o motor estiver ligado, desliga
            if self._status['motorInversor'] or self._status['motorSoft'] or self._status['motorDireta'] ==1:
                self._escritas['4X']['1312']=comando
                self._escritas['4X']['1316']=comando
                self._escritas['4X']['1319']=comando

            #Lê o driver escolhido e liga o motor
            ##caso soft
            if self._status['driver'] == 1:
                self._escritas['4X']['1317']=self._comandoVent.ids.acc.text
                self._escritas['4X']['1318']=self._comandoVent.ids.dcc.text
                self._escritas['4X']['1316']=comando
            ##caso inversor
            elif self._status['driver'] == 2:
                self._escritas['4X']['1314']=self._comandoVent.ids.acc.text
                self._escritas['4X']['1315']=self._comandoVent.ids.dcc.text
                self._escritas['4X']['1313']=self._comandoVent.ids.vel.text
                self._escritas['4X']['1312']=comando

            ##caso direta
            elif self._status['driver'] == 3:
                self._escritas['4X']['1319']=comando
        
        elif comando == 2: #resetar
            self._escritas['4X']['1312']=comando
            self._escritas['4X']['1316']=comando
            self._escritas['4X']['1319']=comando

    def comandoAqueUmi(self,comando,maq):
        if comando == 1: #ligar
            self._status['aqueUmi'][maq] = comando
            self._escritas['HRBits']['1329']= self._status['aqueUmi']
        if comando == 0: #ligar
            self._status['aqueUmi'][maq] = comando
            self._escritas['HRBits']['1329']= self._status['aqueUmi']

    def comandoComp(self, comando):
        if comando == 0: # desligar
            self._status['aqueUmi'][0] = comando
            self._escritas['HRBits']['1329']= self._status['aqueUmi']
        elif comando == 1: #ligar
            self._escritas['4X']['1236'] = self._comandoComp.children.ids.comOnze.children[0].value
            self._status['comp'][4] = comando
            self._escritas['HRBits']['1328']= self._status['comp']

    def sel_Comp(self, comando):
        """
        Seleciona o tipo de compressor
        """
        if comando == 0: # scroll
            self._status['comp'][1] = comando
            self._escritas['HRBits']['1328']= self._status['comp']

        elif comando == 1: #hermetico
            self._status['comp'][1] = comando
            self._escritas['HRBits']['1328']= self._status['comp']

            
    # def testeMoverVenezianas(self,*args):
    #     self._conectaCLP.escreve4x(self._ClienteModbus,self._tagsVeneziana4X['ve.sel_pid'],1)
    #     ### FAZER DICT QUE ARMAZENA LEITURAS
    #     self._conectaCLP.escreve4x(self._ClienteModbus, self._tagsVeneziana4X['ve.mv_escreve'],self.ids.slider.value)

    ####SLIDERS DE VELOCIDADE SÓ FUNCIONAM AO CLICAR EM LIGAR, FAZER METODO QUE OS ATUALIZA


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

class conectaCLP(ModbusClient):

    def __init__(self, host='localhost', port=502, unit_id=1, timeout=30, debug=False, auto_open=True, auto_close=False):
        super().__init__(host, port, unit_id, timeout, debug, auto_open, auto_close)
        
    def leFP(self,cliente,endereco):
        leitura = cliente.read_holding_registers(endereco,2)
        decoder = BinaryPayloadDecoder.fromRegisters(leitura, byteorder=Endian.Big, wordorder=Endian.Little)
        return decoder.decode_32bit_float()

    def le4X(self,cliente,endereco):
        leitura = cliente.read_holding_registers(endereco,1)[0]
        return leitura

    def leHRBits(self,cliente,endereco):
        valor16bits = cliente.read_holding_registers(endereco,1)[0]
        listaBits = [int(i) for i in list('{0:016b}'.format(valor16bits))] 
        return listaBits

    def escreve4x(self,cliente,endereco,valor):
        cliente.write_single_register(endereco,valor)

    def escreveHRBits(self,cliente,endereco,valor):
        valor16bits = int("".join(str(i) for i in valor),2)
        cliente.write_single_register(endereco,valor16bits)

    def escreveFP(self,cliente,endereco,valor):
        pass

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