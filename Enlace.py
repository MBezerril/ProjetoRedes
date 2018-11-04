import Fisica as fis
import threading as thrd
from time import sleep
import Hamming as hamm
import random

class pacote:
    def __init__(self):
        self.origem = ''
        self.destino = ''
        self.tamanhoDados = 0
        self.dados = ''

    def setOrigem(self, num1, num2):
        self.origem = str(num1) + '.' + str(num2)

    def setDestino(self, num1, num2):
        self.destino = str(num1) + '.' + str(num2)

class camadaenlace:
    def __init__(self):
        self.camadafisica = fis.CamadaFisica() # camada física
        self.colision = False # variavel pra detectar colisão
        self.tries = 10 # quantidade de tentativas
        self.transmiting = False # caso a camada de enlace esteja fazendo tranmissão
        self.receiving = False #caso esteja recebendo dados

    def trasnmition(self, pacote):
        """
        quando receber um dado tenta transmistir os dados pela camada física
        quando consegiur, retorna verdadeiro, caso não consiga, retorna falso
        esta classe considera uma quantidade de tentativas como limite, e após essa quantidade, é dado como timeout
        :param data:
        :return:
        """
        destino = list(self.encodeEndereco(pacote.destino))
        destino = list(map(int, destino))

        origem = list(self.encodeEndereco(pacote.origem))
        origem = list(map(int, origem))

        tamanhodados = list(self.encode(pacote.tamanhodados))
        tamanhodados = list(map(int, tamanhodados))

        dadospacote = list(self.encode(pacote.dados))
        dadospacote = list(map(int, dadospacote))

        bytes = hamm.hammingCodes(destino)
        bytes += hamm.hammingCodes(origem)
        bytes += hamm.hammingCodes(tamanhodados)
        bytes += self.hammingDados(dadospacote)
        bytes.append('borda')
        bytes.insert(0, 'borda')

        t = 0
        while t < self.tries: # verifica a disponibilidade da rede uma certa quantidade de vezes antes de expirar
            lido = self.camadafisica.read()
            if lido is None:
                self.transmiting = True
                for bit in bytes:
                    self.camadafisica.write(bit)
                    if self.camadafisica.read() != bit:  # se foi lido algo diferente do que foi escrito, então houve colisão
                        print("colisão! emitindo jam")
                        self.camadafisica.write('borda')
                        self.camadafisica.write('borda')
                        self.transmiting = False
                        t = 0
                        sleep(random.randint(1, 5))
                    break
            else:
                t += 1
                sleep(random.randint(10, 25)) #espera aleatória para verificar novamente se o meio está livre

        if self.transmiting:
            self.transmiting = False
            return True
        else:
            print("excedeu as tentativas - camada de enlace")
            return False

    def listenpackage(self):
        x = True
        quadro = []
        while x:
            x = False
            recebido = 0
            quadro = []
            # self.executor = thrd.thread(target=self._writing, args=[data])
            while not self.transmiting:
                recebido = self.camadafisica.read()
                if recebido == 'borda':
                    self.receiving = True
                    break
            while not self.transmiting and self.receiving:
                recebido = self.camadafisica.read()
                if recebido != 'borda':
                    quadro.append(recebido)
                else:
                    recebido = self.camadafisica.read()
                    if recebido == 'borda':
                        x = True
                        self.receiving = False
                    else:
                        self.receiving = False

        partes = [quadro[x:x + 8] for x in range(0, len(quadro), 8)]

        destino = self.listToString(hamm.hammingCodes(partes[0]))
        origem = self.listToString(hamm.hammingCodes(partes[1]))

        pacoteretorno = pacote()
        pacoteretorno.setDestino(self.decodeInt(destino[:3]), self.decodeInt(destino[4:]))
        pacoteretorno.setOrigem(self.decodeInt(origem[:3]), self.decodeInt(origem[4:]))
        pacoteretorno.tamanhodados = self.decodeInt(self.listToString(hamm.hammingCodes(partes[2])))
        final = []
        for a in partes[3:]:
            final += self.decodeChar(self.listToString(hamm.hammingCodes(a)))
        pacoteretorno.dados = final
        # processar o quadro para retornar o pacote
        return pacoteretorno

    def encode(self, ascii):
        if type(ascii) is int:
            return "{0:08b}".format(ascii)
        else:
            bytes = ''.join('{0:08b}'.format(ord(x), 'b') for x in ascii)
            return bytes

    def encodeEndereco(self,ascii):
        ascii = ascii.split('.')
        return ''.join("{0:04b}".format(int(x),'b') for x in ascii)

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

    def listToString(self, dado):
        retorno = ''
        for x in dado:
            retorno += str(x)
        return retorno