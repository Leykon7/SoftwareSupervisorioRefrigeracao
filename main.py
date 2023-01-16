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
        self._widget = Interface(scan_time=1000,server_ip='10.15.20.17', server_port=10012, 
        endTelaFP = {
            've.encoder':884,
            've.tit01':1220,            #
            've.pit01':1224,            #
            've.tit02':1218,            #
            've.pit02':1222,            #
            've.pit03':1226,            #
            've.vazao':714,             #
            've.velocidade':712,        #
            've.temperatura':710,       #
            've.torque_axial1':1424,
            've.torque_radial1 ':1422
        }, 
        endValvulas4X ={
            've.xv_scroll.0' :1230,
            've.xv_hermetico.1' :1230,
            've.xv5.7':1328
        },
        endPartida4X = {
            've.sel_driver' :1324,
            've.indica_driver' :1216,
            've.atv31' :1312,
            've.ats48' :1316,
            've.tesys' :1319,
        })
        modbus_enderecos4X={
            've.frequencia' :630,
            've.tipo_motor' :78,
            've.status_pid' :722,
            've.corrente_r_co' :726,
            've.corrente_s_co' :727,
            've.corrente_t_co' :728,
            've.corrente_n_co' :729,
            've.corrente_media_co' :731,
            've.tensao_rs_co' :732,
            've.tensao_st_co' :733,
            've.tensao_tr_co' :734,
            've.ativa_r_co' :735,
            've.ativa_s_co' :736,
            've.ativa_t_co' :737,
            've.ativa_total_co' :738,
            've.reativa_r_co' :739,
            've.reativa_s_co' :740,
            've.reativa_t_co' :741,
            've.reativa_total_co' :742,
            've.aparente_r_co' :743,
            've.aparente_s_co' :744,
            've.aparente_t_co' :745,
            've.aparente_total_co' :746,
            've.fp_r_co' :747,
            've.fp_s_co' :748,
            've.fp_t_co' :749,
            've.fp_total_co' :750,
            've.frequencia_co' :751,
            've.thd_corrente_r_co' :752,
            've.thd_corrente_s_co' :753,
            've.thd_corrente_t_co' :754,
            've.thd_corrente_n_co' :755,
            've.thd_tensao_rn_co' :756,
            've.thd_tensao_sn_co' :757,
            've.thd_tensao_tn_co' :758,
            've.thd_tensao_rs_co' :759,
            've.thd_tensao_st_co' :760,
            've.thd_tensao_tr_co' :761,
            've.demanda_anterior_co' :762,	
            've.demanda_atual_co' :763,
            've.demanda_media_co' :764,
            've.demanda_pico_co' :765,
            've.demanda_prevista_co' :766,	
            've.energia_ativa_co' :767,
            've.energia_reativa_co' :768,	
            've.energia_aparente_co' :769,	
            've.thd_tensao_rn' :800,
            've.thd_tensao_sn' :801,
            've.thd_tensao_tn' :802,
            've.thd_tensao_rs' :804,
            've.thd_tensao_st' :805,
            've.thd_tensao_tr' :806,
            've.corrente_r' :840,
            've.corrente_s' :841,
            've.corrente_t' :842,
            've.corrente_n' :843,
            've.corrente_media' :845,
            've.tensao_rs' :847,
            've.tensao_st' :848,
            've.tensao_tr' :849,
            've.ativa_r' :852,
            've.ativa_s' :853,
            've.ativa_t' :854,
            've.ativa_total' :855,
            've.reativa_r' :856,
            've.reativa_s' :857,
            've.reativa_t' :858,
            've.reativa_total' :859,
            've.aparente_r' :860,
            've.aparente_s' :861,
            've.aparente_t' :862,
            've.aparente_total' :863,
            've.fp_r' :868,
            've.fp_s' :869,
            've.fp_t' :870,
            've.fp_total' :871,
            've.thd_corrente_r' :874,
            've.thd_corrente_s' :875,
            've.thd_corrente_t' :876,
            've.thd_corrente_n' :877,
            've.status_ats48' :886,
            've.status_atv31' :888,
            've.status_tesys' :890,
            've.sel_driver' :1324,
            've.indica_driver' :1216,
            've.atv31' :1312,
            've.ats48' :1316,
            've.tesys' :1319,
            've.atv31_velocidade' :1313,
            've.atv31_acc' :1314,
            've.atv31_dcc' :1315,
            've.ats48_acc' :1317,
            've.ats48_dcc' :1318,
            've.sel_pid' :1332,
            've.demanda_anterior' :1204,
            've.demanda_atual' :1205,
            've.demanda_media' :1206,
            've.demanda_pico' :1208,
            've.demanda_prevista' :1207,
            've.energia_ativa' :1210,
            've.energia_reativa' :1212,
            've.energia_aparente' :1214,
            've.xv_scroll.0':1230,
            've.xv_hermetico.1':1230,
            've.status_m3.6':1230,
            've.status_umi.1':1231,
            've.alarme_termo.6':1231,
            've.st_aq1.2':1231,
            've.st_aq2.3':1231,
            've.st_compressor.5':1231,
            've.velocidade_scroll':1236,
            've.psl01.2':1230,
            've.psl02.3':1230,
            've.psh01.4':1230,
            've.psh02.5':1230,
            've.nb_umidificador.0':1231,
            've.baixa_vazao.4':1231,
            've.sel_tipo_ventilador.2':1328,
            've.sel_rendimento.5':1328,
            've.sel_tipo_compressor.1':1328,
            've.liga_compressor.4':1328,
            've.desliga_compressor.0' :1329,
            've.liga_umi.2':1329, 
            've.desliga_umi.3':1329,
            've.liga_aq1.4':1329,
            've.desliga_aq1.5':1329,
            've.liga_aq2.6':1329,
            've.desliga_aq2.7':1329,
            've.sp_termo' :1338,
            've.man_auto_scroll.3':1328,
            've.xv05_abre.0':1330,
            've.xv05_fecha.1':1330,
            've.habilita.3':1330,
            've.valv_inversor_pid.0':1328,
            've.xv5.7':1328,
            've.comutacao':1420}
        endFPrestantes = {
            've.temp_r':700,
            've.temp_s':702,
            've.temp_t':704,
            've.temp_carc':706,
            've.mv_le':614,
            've.mv_le':814,
            've.p':1304,
            've.i':1306,
            've.d':1308,
            've.mv_escreve':1310,
            've.sp_pid':1302,
            've.sp_termo':1338}
        endTempFP ={
            've.temp_r':700,
            've.temp_s':702,
            've.temp_t':704,
            've.temp_carc':706
        }
        """
        ve.temp_r	    ##Temperatura Enrolamento r			
        ve.temp_s	    ##Temperatura Enrolamento s			
        ve.temp_t   	##Temperatura Enrolamento t			
        ve.temp_carc	##Temperatura Carcaça			
        """
        endAqueUmidTerm4X={
            've.liga_umi.2':1329, 
            've.desliga_umi.3':1329,
            've.liga_aq1.4':1329,
            've.desliga_aq1.5':1329,
            've.liga_aq2.6':1329,
            've.desliga_aq2.7':1329,
            've.sp_termo':1338
        }
        """
        ve.liga_umi         0   ##Umidificador
        ve.desliga_umi      1
        ve.liga_aq1	        0   ##Aquecedor 1
        ve.desliga_aq1	    0   
        ve.liga_aq2	        0   ##Aquecedor 2
        ve.desliga_aq2	    0
        ve.sp_termo             ##Termostato
        """
        endComp4X = {
            've.sel_tipo_compressor.1':1328,
            've.liga_compressor.4':1328,
            've.desliga_compressor.0' :1329,
            've.velocidade_scroll':1236
        }
        """
        	                            Scroll	Hermético		
            ve.sel_tipo_compressor  #	  0	        1		
            ve.desliga_compressor	#     0			
            ve.liga_compressor	    #     1			
            ve.velocidade_scroll	#Velocidade do compressor Scroll
        """
        endMotor4X = {
            've.atv31' :1312,
            've.ats48' :1316,
            've.tesys' :1319,
            've.atv31_velocidade' :1313,
            've.atv31_acc' :1314,
            've.atv31_dcc' :1315,
            've.ats48_acc' :1317,
            've.ats48_dcc' :1318,
            've.sel_tipo_ventilador.2':1328,
            've.sel_rendimento.5':1328
        }
        """
        ve.acc	                  ##Tempo de aceleração inversor			
        ve.dcc	                  ##Tempo de desaceleração inversor			
        ve.atv31_velocidade	      ## 0 a 60			
                                    Axial	Radial		
        ve.sel_tipo_ventilador	  ##  1     	0		
                                    Alto	Convencional		
        ve.sel_rendimento	      ##  0            1		
        """
        
        """
        ve.sel_driver	##Soft	        1		
                          Inversor	    2		
                          Direta	    3		
                                        Liga    Desliga	Reset
        ve.ats48	  ##Liga Soft	     1	       0	 2
        ve.atv31	  ##Liga Inversor	 1	       0	 2
        ve.tesys	  ##Liga Direta	     1	       0	 2

        ve.indica_driver ##Indica driver selecionado?
        """
        endVeneziana = {
            've.sel_pid' :1332,
            've.mv_escreve':1310
        }
        """
        	                Automático	Manual
            ve.sel_pid	        0	      1
            ve.fv01	        MV
            ve.mv_escreve  escrever no MV?
        """
        
        """
        #Como controlar a veneziana : ve.fv01
        como funcionam os endereços com ponto??
        #como funcionam motores : slider vel do inversor, encoder para o mesmo,
        #que é temperatura do enrolamento : motor
        #aquecedores ligam ao mesmo tempo ; sim
        velocidade do scroll é para controlar(ve.velocidade_scroll) ; 
        que é o rendimento do motor
        #Como funciona soft start : acc e dcc apenas
        #A frequencia ve.encoder serve para os dois motores : sim
        ver grandezas eletricas
        xv hermetico e scroll : valvulas 
        """
        return self._widget

if __name__ == '__main__':
    Window.size=(1080, 720)
    #Window.resizable=False
    #Window.fullscreen = 'auto'
    Builder.load_string(open("interface.kv",encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("popups.kv",encoding="utf-8").read(),rulesonly=True)
    Principal().run()
