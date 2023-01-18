from datetime import datetime
from threading import Thread
from threading import Lock
from tabulate import tabulate
from db import Base,Session,engine
from models import DadoCLP

class Persistencia(object):
    """
    Classe que implementa funcionalidade de persistência de dados 
    lidos a partir do protocolo Modbus
    """
    def __init__(self): 
        """
        Construtor
        """
        self._session = Session()
        Base.metadata.create_all(engine)
        self._threads = []
        self._lock = Lock()

    def guardar_dados(self,data):
        """
        Método que guarda informações lidas
        """
        try:
            data['timestamp'] = datetime.now()
            dado = DadoCLP(**data)
            self._lock.acquire()
            self._session.add(dado)
            self._session.commit()
            self._lock.release()
        except Exception as e:
            print("Erro: ", e.args)

    def acesso_dados_historicos(self):
        """
        Método que permite ao usuário acessar dados históricos
        """
        try:
            print("Bem vindo ao sistema de busca de dados históricos")
            while True:
                init = input("Digite o horário inicial para a busca (DD/MM/AAAA HH:MM:SS):")
                final = input("Digite o horário final para a busca (DD/MM/AAAA HH:MM:SS):")
                init = datetime.strptime(init, '%d/%m/%Y %H:%M:%S')
                final = datetime.strptime(final, '%d/%m/%Y %H:%M:%S')
                self._lock.acquire()
                results = self._session.query(DadoCLP).filter(DadoCLP.timestamp.between(init,final)).all()
                self._lock.release()
                results_fmt_lst = [reg.get_attr_printable_list() for reg in results]
                print(tabulate(results_fmt_lst,headers=DadoCLP.__table__.columns.keys()))
        except Exception as e:
            print("Erro: ", e.args)

    # def run(self):
    #     self._threads.append(Thread(target=self.guardar_dados))
    #     self._threads.append(Thread(target=self.acesso_dados_historicos))
    #     for t in self._threads:
    #         t.start()

    
