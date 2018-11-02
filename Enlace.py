import Fisica as fis
import threading as thrd
from time import sleep
class CamadaEnlace:
    def __init__(self):
        self.camadaFisica = fis.CamadaFisica() # Camada física
        self.colision = False # variavel pra detectar colisão
        self.tries = 10 # Quantidade de tentativas
        self.transmiting = False # Caso a camada de enlace esteja fazendo tranmissão
        self.bits = 10
    def trasnmition(self, data):
        """
        Quando receber um dado tenta transmistir os dados pela camada física
        Quando consegiur, retorna verdadeiro, caso não consiga, retorna falso
        Esta classe considera uma quantidade de tentativas como limite, e após essa quantidade, é dado como timeout
        :param data:
        :return:
        """
        # Deteccao de uso da rede
        # Tenta tramitir
        # Verifica colisão
        # Se houver retorna pra DETECCAO

        for t in range(self.tries): # Verifica a disponibilidade da rede uma certa quantidade de vezes antes de expirar
            lido = self.camadaFisica.read(self.bits)
            if 1 not in array:
                self.transmiting = True
                break
        if self.transmiting:
            writer = thrd.Thread(target=self.camadaFisica.write, args=(data,))
            writer.start()
            # self.camadaFisica.write(data)
        else:
            print("EXCEDEU AS TENTATIVAS - CAMADA DE ENLACE")
        #sleep(2)
        #self.camadaFisica.stopWrite()
        #while writer.is_alive():
        #   pass
        # Deteccao de colisão aqui <<<<<<<<<<<<<<<<<<<<<<<<
        # Para para a escrita, basta chamar self.camadaFisica.stopWrite()

teste1 = CamadaEnlace()

teste1.trasnmition([0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1])
teste2 = fis.CamadaFisica()