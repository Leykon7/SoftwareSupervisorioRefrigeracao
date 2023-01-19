from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.properties import NumericProperty
import popups
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread
from time import sleep
from datetime import datetime
import random
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
#from pymodbus.payload import BinaryPayloadBuilder
from modbuspersistencia import Persistencia

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
    _tagsaque_umi_comdTermo4X={}
    _tagsVeneziana4X = {}

    def __init__(self,**kwargs):
        super().__init__()
        #Pega info
        self._scan_time = kwargs.get('scan_time')
        self._serverIP = kwargs.get('server_ip')
        self._port = kwargs.get('server_port')

        #Cliente Modbus
        self._ClienteModbus = ModbusClient(host=self._serverIP, port=self._port)

        #Persistencia
        self._persistencia = Persistencia()

        #Leituras
        self._valvulas = {}
        self._dadosUteis={}
        self._dados2BD = {}
        self._dadosUteis['4X']={}
        self._dadosUteis['FP']={}

         #escritas
        self._escritas = {}
        self._escritas['4X'] ={}
        self._escritas['FP'] ={}
        self._escritas['HRBits']={}

        #Leitura de status
        self._status = {}

        ### usar apenas duas bibliotecas, uma para ações e outra de leituras

        ##Dá cor e salva no dict _tags

        for key, value in kwargs.get('endValvulas4X').items():
            self._tagsValvula4X[key] = value

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
        self._ats48 = popups.ats48()
        self._atv31 = popups.atv31()
        self._popupgrafico = popups.popupgrafico()
        self._bdPopup = popups.bdPopup()
                
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
                self.insereNoBD()
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
        # Dados da tela
        # self._medidasTela['Timestamp'] = datetime.now()
        # for key,value in self._tagsTelaFP.items():
        #     self._medidasTela['Valores'][key] = self._conectaCLP.leFP(self._ClienteModbus,value['endereco'])
            
        #Leitura das Valvulas
        for key, value in self._tagsValvula4X.items():
            self._valvulas[key] = self._conectaCLP.leHRBits(self._ClienteModbus,value)

        #Leitura de temperatura dos enrolamentos do motor e carcaça
        # self._medidasTempRSTCar['Timestamp'] = datetime.now()
        # for key,value in self._tagsTempeRSTCarFP.items():
        #     self._conectaCLP.leHRBits(self._ClienteModbus,value['endereco'])
        #     self._medidasTempRSTCar['Valores'][key] = self._conectaCLP.leFP(self._ClienteModbus,value['endereco'])

        #Leitura de dados que vão para o bd
        if self._comandoVent.ids.axial.active:
            self._dadosUteis['4X']['tipo_motor']= 1
        elif self._comandoVent.ids.radial.active:
            self._dadosUteis['4X']['tipo_motor']= 2
        if self._comandoComp.ids.hermetico.active:
            self._dadosUteis['4X']['tipo_motor']= 1
        elif self._comandoComp.ids.scroll.active:
            self._dadosUteis['4X']['tipo_motor']= 2
        self._dadosUteis['FP']['temperatura_tit1']=	self._conectaCLP.leFP(self._ClienteModbus,	1220)/10
        self._dadosUteis['FP']['temperatura_tit2']=	self._conectaCLP.leFP(self._ClienteModbus,	1218)/10
        self._dadosUteis['FP']['pressao_pit1']=	self._conectaCLP.leFP(self._ClienteModbus,	1224)/10
        self._dadosUteis['FP']['pressao_pit2']=	self._conectaCLP.leFP(self._ClienteModbus,	1222)/10
        self._dadosUteis['FP']['pressao_pit3']=	self._conectaCLP.leFP(self._ClienteModbus,	1226)/10
        self._dadosUteis['FP']['vazao_saida']=	self._conectaCLP.leFP(self._ClienteModbus,	714)
        self._dadosUteis['FP']['velocidade_saida']=	self._conectaCLP.leFP(self._ClienteModbus,	712)
        self._dadosUteis['FP']['temp_ar_saida']=	self._conectaCLP.leFP(self._ClienteModbus,	710)
        self._dadosUteis['FP']['freq_motor']=	self._conectaCLP.leFP(self._ClienteModbus,	884)
        self._dadosUteis['FP']['torque_motor_axial']=	self._conectaCLP.leFP(self._ClienteModbus,	1424)
        self._dadosUteis['FP']['torque_motor_radial']=	self._conectaCLP.leFP(self._ClienteModbus,	1422)
        self._dadosUteis['FP']['temperatura_R']=	self._conectaCLP.leFP(self._ClienteModbus,	700)/10
        self._dadosUteis['FP']['temperatura_S']=	self._conectaCLP.leFP(self._ClienteModbus,	702)/10
        self._dadosUteis['FP']['temperatura_T']=	self._conectaCLP.leFP(self._ClienteModbus,	704)/10
        self._dadosUteis['FP']['temperatura_Carc']=	self._conectaCLP.leFP(self._ClienteModbus,	70)/10
        self._dadosUteis['4X']['corrente_R']=	self._conectaCLP.le4X(self._ClienteModbus,	840)/10
        self._dadosUteis['4X']['corrente_S']=	self._conectaCLP.le4X(self._ClienteModbus,	841)/10
        self._dadosUteis['4X']['corrente_T']=	self._conectaCLP.le4X(self._ClienteModbus,	842)/10
        self._dadosUteis['4X']['corrente_N']=	self._conectaCLP.le4X(self._ClienteModbus,	843)/10
        self._dadosUteis['4X']['corrente_Media']=	self._conectaCLP.le4X(self._ClienteModbus,	845)/10
        self._dadosUteis['4X']['tensao_RS']=	self._conectaCLP.le4X(self._ClienteModbus,	847)/10
        self._dadosUteis['4X']['tensao_ST']=	self._conectaCLP.le4X(self._ClienteModbus,	848)/10
        self._dadosUteis['4X']['tensao_TR']=	self._conectaCLP.le4X(self._ClienteModbus,	849)/10
        self._dadosUteis['4X']['potencia_ativa_R']=	self._conectaCLP.le4X(self._ClienteModbus,	852)
        self._dadosUteis['4X']['potencia_ativa_S']=	self._conectaCLP.le4X(self._ClienteModbus,	853)
        self._dadosUteis['4X']['potencia_ativa_T']=	self._conectaCLP.le4X(self._ClienteModbus,	854)
        self._dadosUteis['4X']['potencia_ativa_Total']=	self._conectaCLP.le4X(self._ClienteModbus,	855)
        self._dadosUteis['4X']['fp_R']=	self._conectaCLP.le4X(self._ClienteModbus,	868)/1000
        self._dadosUteis['4X']['fp_S']=	self._conectaCLP.le4X(self._ClienteModbus,	869)/1000
        self._dadosUteis['4X']['fp_T']=	self._conectaCLP.le4X(self._ClienteModbus,	870)/1000
        self._dadosUteis['4X']['fp_Total']=	self._conectaCLP.le4X(self._ClienteModbus,	871)/1000
        self._dadosUteis['4X']['corrente_R_co']=	self._conectaCLP.le4X(self._ClienteModbus,	726)/10
        self._dadosUteis['4X']['corrente_S_co']=	self._conectaCLP.le4X(self._ClienteModbus,	727)/10
        self._dadosUteis['4X']['corrente_T_co']=	self._conectaCLP.le4X(self._ClienteModbus,	728)/10
        self._dadosUteis['4X']['corrente_N_co']=	self._conectaCLP.le4X(self._ClienteModbus,	729)/10
        self._dadosUteis['4X']['corrente_Media_co']=	self._conectaCLP.le4X(self._ClienteModbus,	731)/10
        self._dadosUteis['4X']['tensao_RS_co']=	self._conectaCLP.le4X(self._ClienteModbus,	732)/10
        self._dadosUteis['4X']['tensao_ST_co']=	self._conectaCLP.le4X(self._ClienteModbus,	733)/10
        self._dadosUteis['4X']['tensao_TR_co']=	self._conectaCLP.le4X(self._ClienteModbus,	734)/10
        self._dadosUteis['4X']['potencia_ativa_R_co']=	self._conectaCLP.le4X(self._ClienteModbus,	735)
        self._dadosUteis['4X']['potencia_ativa_S_co']=	self._conectaCLP.le4X(self._ClienteModbus,	736)
        self._dadosUteis['4X']['potencia_ativa_T_co']=	self._conectaCLP.le4X(self._ClienteModbus,	737)
        self._dadosUteis['4X']['potencia_ativa_Total_co']=	self._conectaCLP.le4X(self._ClienteModbus,	738)
        self._dadosUteis['4X']['fp_R_co']=	self._conectaCLP.le4X(self._ClienteModbus,	747)/1000
        self._dadosUteis['4X']['fp_S_co']=	self._conectaCLP.le4X(self._ClienteModbus,	748)/1000
        self._dadosUteis['4X']['fp_T_co']=	self._conectaCLP.le4X(self._ClienteModbus,	749)/1000
        self._dadosUteis['4X']['fp_Total_co']=	self._conectaCLP.le4X(self._ClienteModbus,	750)/1000

        #Leitura do status do motor e do driver
        ####FAZER COM QUE AS LEITURAS QUE JÁ ESTÃO NA BANCADA APARECAM NO PROGRAMA
        self._status['driver'] = self._conectaCLP.le4X(self._ClienteModbus,1324)
        self._status['motorInversor'] = self._conectaCLP.le4X(self._ClienteModbus,1312)
        self._status['motorSoft'] = self._conectaCLP.le4X(self._ClienteModbus,1316)
        self._status['motorDireta'] = self._conectaCLP.le4X(self._ClienteModbus,1319)
        self._status['aque_umi_com'] = self._conectaCLP.leHRBits(self._ClienteModbus, 1329)
        self._status['comp'] = self._conectaCLP.leHRBits(self._ClienteModbus, 1328)
        self._status['velScroll'] = self._conectaCLP.le4X(self._ClienteModbus, 1236)
        self._status['pressao_comp'] = self._conectaCLP.leHRBits(self._ClienteModbus, 1230)
        self._status['veneziana'] = self._conectaCLP.leFP(self._ClienteModbus,1310)
        #print('veneziana: '+ str(self._status['veneziana']))
        self._status['pid'] = self._conectaCLP.le4X(self._ClienteModbus,722)
        #print('pid: '+ str(self._status['pid']))

    def atualizaInterface(self):
        """
        Método que atualiza a interface gráfica a partir dos dados lidos
        """
        #Medidas da tela

        self.ids.pit1.text =str((self._dadosUteis['FP']['pressao_pit1']))+' Psi'
        self.ids.pit2.text =str((self._dadosUteis['FP']['pressao_pit2']))+' Psi'
        self.ids.pit3.text =str((self._dadosUteis['FP']['pressao_pit3']))+' Psi'
        self.ids.tit1.text =str((self._dadosUteis['FP']['temperatura_tit1']))+' ºC'
        self.ids.tit2.text =str((self._dadosUteis['FP']['temperatura_tit2']))+' ºC'
        self.ids.tit3.text =str(round(self._dadosUteis['FP']['temp_ar_saida'],2))+' ºC'
        self.ids.vazao.text =str(round(self._dadosUteis['FP']['vazao_saida'],2))+' m³/h'
        self.ids.vel.text =str(round(self._dadosUteis['FP']['velocidade_saida'],2))+' m/s'
        
        if self._status['pressao_comp'][4] == 1:
            self.ids.st_hermetico.text = 'Alta pressao'
            
        if self._status['pressao_comp'][5] == 1:
            self.ids.st_hermetico.text = 'Alta pressao'
        
       
        #Valvulas
        if self._valvulas['ve.xv_scroll.0'][15] == 1:
            self.ids.xv1.source = 'imgs/ValvulaAzul.png'
            self.ids.xv3.source = 'imgs/ValvulaAzul.png'
        elif self._valvulas['ve.xv_hermetico.1'][14]==1:
            self.ids.xv2.source = 'imgs/ValvulaAzul.png'
            self.ids.xv4.source = 'imgs/ValvulaAzul.png'
        else:
            self.ids.xv1.source = 'imgs/ValvulaBranca.png'
            self.ids.xv3.source = 'imgs/ValvulaBranca.png'
            self.ids.xv2.source = 'imgs/ValvulaBranca.png'
            self.ids.xv4.source = 'imgs/ValvulaBranca.png'
            
        if self._valvulas['ve.xv5.7'][8]== 1:
            self.ids.xv5.source = 'imgs/ValvulaAzul.png'
        else:
            self.ids.xv5.source = 'imgs/ValvulaBranca.png'

        #Temperaturas R, S, T e Carcaça
        self._tempRSTCar.ids.temp_r.text =str(self._dadosUteis['FP']['temperatura_R'])+' ºC'
        self._tempRSTCar.ids.temp_s.text =str(self._dadosUteis['FP']['temperatura_S'])+' ºC'
        self._tempRSTCar.ids.temp_t.text =str(self._dadosUteis['FP']['temperatura_T'])+' ºC'
        self._tempRSTCar.ids.carcaca.text =str(self._dadosUteis['FP']['temperatura_Carc'])+' ºC'

        #medidas do compressor
        self._medidasTelaComp.ids.corrente_R_co.text = str(self._dadosUteis['4X']['corrente_R_co'])
        self._medidasTelaComp.ids.corrente_T_co.text = str(self._dadosUteis['4X']['corrente_T_co'])
        self._medidasTelaComp.ids.corrente_S_co.text = str(self._dadosUteis['4X']['corrente_S_co'])
        self._medidasTelaComp.ids.corrente_N_co.text = str(self._dadosUteis['4X']['corrente_N_co'])
        self._medidasTelaComp.ids.corrente_Media_co.text = str(self._dadosUteis['4X']['corrente_Media_co'])

        self._medidasTelaComp.ids.tensao_RS_co.text = str(self._dadosUteis['4X']['tensao_RS_co'])
        self._medidasTelaComp.ids.tensao_ST_co.text = str(self._dadosUteis['4X']['tensao_ST_co'])
        self._medidasTelaComp.ids.tensao_TR_co.text = str(self._dadosUteis['4X']['tensao_TR_co'])

        self._medidasTelaComp.ids.potencia_R_co.text = str(self._dadosUteis['4X']['potencia_R_co'])
        self._medidasTelaComp.ids.potencia_T_co.text = str(self._dadosUteis['4X']['potencia_T_co'])
        self._medidasTelaComp.ids.potencia_S_co.text = str(self._dadosUteis['4X']['potencia_S_co'])
        self._medidasTelaComp.ids.potencia_Total_co.text = str(self._dadosUteis['4X']['potencia_Total_co'])

        self._medidasTelaComp.ids.fp_R_co.text = str(self._dadosUteis['4X']['fp_R_co'])
        self._medidasTelaComp.ids.fp_T_co.text = str(self._dadosUteis['4X']['fp_T_co'])
        self._medidasTelaComp.ids.fp_S_co.text = str(self._dadosUteis['4X']['fp_S_co'])
        self._medidasTelaComp.ids.fp_Total_co.text = str(self._dadosUteis['4X']['fp_Total_co'])

        #medidas do ventilador
        self._medidasTelaVent.ids.corrente_R.text = str(self._dadosUteis['4X']['corrente_R'])
        self._medidasTelaVent.ids.corrente_T.text = str(self._dadosUteis['4X']['corrente_T'])
        self._medidasTelaVent.ids.corrente_S.text = str(self._dadosUteis['4X']['corrente_S'])
        self._medidasTelaVent.ids.corrente_N.text = str(self._dadosUteis['4X']['corrente_N'])
        self._medidasTelaVent.ids.corrente_Media.text = str(self._dadosUteis['4X']['corrente_Media'])

        self._medidasTelaVent.ids.tensao_RS.text = str(self._dadosUteis['4X']['tensao_RS'])
        self._medidasTelaVent.ids.tensao_ST.text = str(self._dadosUteis['4X']['tensao_ST'])
        self._medidasTelaVent.ids.tensao_TR.text = str(self._dadosUteis['4X']['tensao_TR'])

        self._medidasTelaVent.ids.potencia_R.text = str(self._dadosUteis['4X']['potencia_R'])
        self._medidasTelaVent.ids.potencia_T.text = str(self._dadosUteis['4X']['potencia_T'])
        self._medidasTelaVent.ids.potencia_S.text = str(self._dadosUteis['4X']['potencia_S'])
        self._medidasTelaVent.ids.potencia_Total.text = str(self._dadosUteis['4X']['potencia_Total'])

        self._medidasTelaVent.ids.fp_R.text = str(self._dadosUteis['4X']['fp_R'])
        self._medidasTelaVent.ids.fp_T.text = str(self._dadosUteis['4X']['fp_T'])
        self._medidasTelaVent.ids.fp_S.text = str(self._dadosUteis['4X']['fp_S'])
        self._medidasTelaVent.ids.fp_Total.text = str(self._dadosUteis['4X']['fp_Total'])


    def insereNoBD(self):
        for key,value in self._dadosUteis['FP'].items():
            self._dados2BD[key]=value
        for key,value in self._dadosUteis['4X'].items():
            self._dados2BD[key]=value
        self._persistencia.guardar_dados(self._dados2BD)

    def Partida(self,tipo):
        if tipo == 1: #soft
            self._escritas['4X']['1324']=tipo
        elif tipo == 2: #inversor
            self._escritas['4X']['1324']=tipo
        elif tipo == 3: #direta
            self._escritas['4X']['1324']=tipo
        self._status['driver']=tipo

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

            # #se o motor estiver ligado, desliga
            if self._status['motorInversor'] or self._status['motorSoft'] or self._status['motorDireta'] ==1:
                self._escritas['4X']['1312']=comando
                self._escritas['4X']['1316']=comando
                self._escritas['4X']['1319']=comando

            # #Lê o driver escolhido e liga o motor
            # ##caso soft
            if self._status['driver'] == 1:
                #print(self._status['driver'])
                self._escritas['4X']['1317']=int(self._ats48.ids.acc.text)
                self._escritas['4X']['1318']=int(self._ats48.ids.dcc.text)
                self._escritas['4X']['1316']=comando
            # ##caso inversor
            elif self._status['driver'] == 2:
                self._escritas['4X']['1314']=int(self._atv31.ids.acc.text)/10
                self._escritas['4X']['1315']=int(self._atv31.ids.dcc.text)/10
                #self._escritas['4X']['1313']=self._comandoVent.ids.vel.text
                self._escritas['4X']['1312']=comando

            ##caso direta
            elif self._status['driver'] == 3:
                self._escritas['4X']['1319']=comando
        
        elif comando == 2: #resetar
            self._escritas['4X']['1312']=comando
            self._escritas['4X']['1316']=comando
            self._escritas['4X']['1319']=comando

    def comandoUmi(self,comando):
        if comando == 1: #ligar
            self._status['aque_umi_com'][13] = 0
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
            

            self._status['aque_umi_com'][12] = 1
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
            
        if comando == 0: #desligar
            
            self._status['aque_umi_com'][12] = 1
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
            
            self._status['aque_umi_com'][13] = 0
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']

            # [0  1   2   3   4   5   6    7    8   9   10   11   12   13   14   15]
            # [15 14  13  12  11  10  9    8    7   6    5    4    3    2    1    0] byte
            
    def comandoAque1(self,comando,):
        if comando == 1: #ligar
            self._status['aque_umi_com'][11] = 0
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
                        
            self._status['aque_umi_com'][10] = 1
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
            
        if comando == 0: #desligar
            
            self._status['aque_umi_com'][11] = 1
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
                        
            self._status['aque_umi_com'][10] = 0
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
            
    def comandoAque2(self,comando,):
        if comando == 1: #ligar
            self._status['aque_umi_com'][9] = 0
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
                        
            self._status['aque_umi_com'][8] = 1
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
            
        if comando == 0: #desligar
            
            self._status['aque_umi_com'][9] = 1
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
                        
            self._status['aque_umi_com'][8] = 0
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
            
        
            
    def comandoComp(self, comando):
        if comando == 0: # desligar
            self._status['aque_umi_com'][15] = 0
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
            self._status['comp'][11] = 0
            self._escritas['HRBits']['1328']= self._status['comp']
            
        elif comando == 1: #ligar
            #self._escritas['4X']['1236'] = self._comandoComp.children.ids.comOnze.children[0].value
            self._status['comp'][11] = 1
            self._escritas['HRBits']['1328']= self._status['comp']
            self._status['aque_umi_com'][15] = 1
            self._escritas['HRBits']['1329']= self._status['aque_umi_com']
            
    def sel_Comp(self, comando):
        """
        Seleciona o tipo de compressor
        """
        if comando == 0: # scroll
            
            #print(self._status['comp'])
            #print(self._status['comp'][1])
            self._status['comp'][14] = comando
            self._escritas['HRBits']['1328']= self._status['comp']

        elif comando == 1: #hermetico
            
            #print(self._status['comp'])
            #
            # print(self._status['comp'][1])
            self._status['comp'][14] = comando
            self._escritas['HRBits']['1328']= self._status['comp']
    
    def testeMoverVenezianas(self):
        print((self.ids.slider.value))
        self._escritas['4X']['1332'] = 1
        self._escritas['FP']['1310'] = int(self.ids.slider.value)
        print(self._escritas['FP']['1310'])
        #self._conectaCLP.escreve4x(self._ClienteModbus,self._tagsVeneziana4X['ve.sel_pid'],1)
        ### FAZER DICT QUE ARMAZENA LEITURAS
        #self._conectaCLP.escreve4x(self._ClienteModbus, self._tagsVeneziana4X['ve.mv_escreve'],self.ids.slider.value)

    ####SLIDERS DE VELOCIDADE SÓ FUNCIONAM AO CLICAR EM LIGAR, FAZER METODO QUE OS ATUALIZA

    def venezianas(self, *args):
        self.ids.veneziana1.angle = (-1)*(args[1]/100)*90
        self.ids.veneziana2.angle = (-1)*(args[1]/100)*90
        self.ids.veneziana3.angle = (-1)*(args[1]/100)*90

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