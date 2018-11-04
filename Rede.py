from asyncio import selector_events

import Enlace as enl
import threading as thr

class CamadaRede:
    def __init__(self, address='0.0', mask='255.0'):
        self.enlace = enl.CamadaEnlace() # Camada Enlace
        self.address = address # endereço a ser atribuido como próprio
        self.mask = mask
        self.listening = False

    def start(self):
        escritor = thr.Thread(target=self.getAndSend())
        self.startListen()

    def receiveAndPrint(self):
        self.listening = True
        while 1:
            pacoteRecebido = self.enlace.listenpackage()
            if pacoteRecebido is None:
                self.listening = False
                break
            if pacoteRecebido.destino == self.address:
                print(pacoteRecebido.dados)

    def startListen(self):
        leitor = thr.Thread(target=self.receiveAndPrint())

    def getAndSend(self):
        while 1:
            pacote = enl.pacote()
            pacote.destino = input("Diga ai o endereço do rapaz (Do tipo XX.XX onde XX é de 0 a 15): ")
            pacote.dados = input("Digite a mensagem: ")
            pacote.tamanhoDados = len(pacote.dados)
            pacote.origem = self.address
            self.enlace.send(pacote)
            if not self.listening:
                self.startListen()



