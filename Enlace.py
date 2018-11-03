import Fisica as fis
import threading as thrd
from time import sleep
import Hamming as hamm
import random

class pacote:
    def __init__(self):
        self.origem = ''
        self.destino = ''
        self.tamanhoDados = ''
        self.dados = ''

class CamadaEnlace:
    def __init__(self):
        self.camadaFisica = fis.CamadaFisica() # Camada física
        self.colision = False # variavel pra detectar colisão
        self.tries = 10 # Quantidade de tentativas
        self.transmiting = False # Caso a camada de enlace esteja fazendo tranmissão
        self.receiving = False #caso esteja recebendo dados
    def trasnmition(self, pacote):
        """
        Quando receber um dado tenta transmistir os dados pela camada física
        Quando consegiur, retorna verdadeiro, caso não consiga, retorna falso
        Esta classe considera uma quantidade de tentativas como limite, e após essa quantidade, é dado como timeout
        :param data:
        :return:
        """
        destino = list(self.encode(pacote.destino))
        destino = list(map(int, destino))

        origem = list(self.encode(pacote.origem))
        origem = list(map(int, origem))

        tamanhoDados = list(self.encode(pacote.tamanhoDados))
        tamanhoDados = list(map(int, tamanhoDados))

        dadosPacote = list(self.encode(pacote.dados))
        dadosPacote = list(map(int, dadosPacote))

        bytes = hamm.hammingCodes(destino)
        bytes += hamm.hammingCodes(origem)
        bytes += hamm.hammingCodes(tamanhoDados)
        bytes += self.hammingDados(dadosPacote)
        bytes.append('borda')
        bytes.insert(0, 'borda')

        t = 0
        while t < self.tries: # Verifica a disponibilidade da rede uma certa quantidade de vezes antes de expirar
            lido = self.camadaFisica.read()
            if lido is None:
                self.transmiting = True
                for bit in bytes:
                    self.camadaFisica.write(bit)
                    if self.camadaFisica.read() != bit:  # Se foi lido algo diferente do que foi escrito, então houve colisão
                        print("COLISÃO! EMITINDO JAM")
                        self.camadaFisica.write('borda')
                        self.camadaFisica.write('borda')
                        self.transmiting = False
                        t = 0
                        sleep(random.randint(1, 5))
                    break
            else:
                t += 1
                sleep(random.randint(10, 25)) #Espera aleatória para verificar novamente se o meio está livre

        if self.transmiting:
            self.transmiting = False
            return True
        else:
            print("EXCEDEU AS TENTATIVAS - CAMADA DE ENLACE")
            return False

    def listenPackage(self):
        x = True
        while x:
            x = False
            recebido = 0
            quadro = []
            # self.executor = thrd.Thread(target=self._writing, args=[data])
            while not self.transmiting:
                recebido = self.camadaFisica.read()
                if recebido == 'borda':
                    self.receiving = True
                    break
            while not self.transmiting and self.receiving:
                recebido = self.camadaFisica.read()
                if recebido != 'borda':
                    quadro.append(recebido)
                else:
                    recebido = self.camadaFisica.read()
                    if recebido == 'borda':
                        x = True
                        self.receiving = False
                    else:
                        self.receiving = False

        partes = [quadro[x:x + 8] for x in range(0, len(quadro), 8)]
        pacoteRetorno = pacote()
        pacoteRetorno.destino = self.decodeInt(hamm.hammingCodes(partes[0]))
        pacoteRetorno.origem = self.decodeInt(hamm.hammingCodes(partes[1]))
        pacoteRetorno.tamanhoDados = self.decodeInt(hamm.hammingCodes(partes[2]))
        final = []
        for a in partes[3:]:
            final += self.decodeChar(hamm.hammingCodes(a))

        # Processar o quadro para retornar o pacote
        return quadro

    def encode(self, ascii):
        if type(ascii) is int:
            return "{0:08b}".format(ascii)
        else:
            bytes = ' '.join('{0:08b}'.format(ord(x), 'b') for x in ascii)
            return bytes.replace(' ', '')

    def decodeChar(self, bytes):
        return ''.join(chr(int(bytes[i*8:i*8+8], 2)) for i in range(len(bytes)//8))

    def decodeInt(self, bytes):
        return int(bytes, 2)

    def hammingDados(self, dados):
        partes = [dados[x:x+8] for x in range(0, len(dados), 8)]
        final = []
        for a in partes:
            final += hamm.hammingCodes(a)
        return final


