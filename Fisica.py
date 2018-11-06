import simpleaudio as sa
import threading as thrd
import pyaudio
import wave
import audioop
from time import sleep


class CamadaFisica:
    def __init__(self):
        self.executor = None
        self.chunkSize = 1024
        self.limite = 450
        self.rateValue = 48000
        self.intervalo = 1 #<<<<<<<<<<<<
        self.debug = False


    def write(self, data):
        self.executor = thrd.Thread(target=self._writing, args=[data])
        self.executor.start()

    def _writing(self, data):
        signal = []
        wave_obj = sa.WaveObject.from_wave_file("beep-04.wav")
        if data == 1:
            sleep(self.intervalo * 0.5)
            play_obj = wave_obj.play()
            sleep(self.intervalo * 0.5)
            play_obj.stop()

        elif data == 0:
            play_obj = wave_obj.play()
            sleep(self.intervalo * 0.5)
            play_obj.stop()
            sleep(self.intervalo * 0.5)
        elif data == 'borda':
            play_obj = wave_obj.play()
            sleep(self.intervalo * 0.5)
            play_obj.stop()
            play_obj = wave_obj.play()
            sleep(self.intervalo * 0.5)
            play_obj.stop()


    def read(self):
        """
        Lê uma amostra e diz se é uma borda de uma transmissão (iniciou ou final), se o meio está livre ou o bit 0 ou 1
        :param size:
        :return list[size]:
        """
        inicio = 0 #Qual bit foi lido
        final = 0
        resultado = 0
        quantLeitura = int(self.rateValue / self.chunkSize * self.intervalo) #Leituras a serem feitas para ser o equivalente a uma leitura de duração igual ao intervalo
        audioDrive = pyaudio.PyAudio()
        gravador = audioDrive.open(input=True, channels=1, rate=self.rateValue, format=pyaudio.paInt16, input_device_index=0)

        valor = 0 #Valor obtido pelas leituras da biblioteca no microfone
        for i in range(int(quantLeitura/2)): #controla o tempo de coleta de gravação pra equivaler a duração do invtervalo
            resultado = gravador.read(self.chunkSize)
            aux = audioop.rms(resultado, 2)
            if self.debug:
                print(aux)
            valor += aux
            #valor += audioop.rms(resultado, 2)
        valor /= int(quantLeitura/2)
        #print("Media: {}".format(valor))
        if valor > self.limite:
            inicio = 1
        valor = 0
        for i in range(int(quantLeitura/2)): #controla o tempo de coleta de gravação pra equivaler a duração do invtervalo
            resultado = gravador.read(self.chunkSize)
            aux = audioop.rms(resultado, 2)
            if self.debug:
                print(aux)
            valor += aux
            #valor += audioop.rms(resultado, 2)
        valor /= int(quantLeitura/2)
        #print("Media: {}".format(valor))
        if valor > self.limite:
            final = 1
        if inicio != final:
            return final
        else:
            if final is 0:
                return None
            else:
                return 'borda' #2

    def sincronizacao(self):
        limiteDesbloqueio = 500
        bonecoChuck = 128

        audioDrive = pyaudio.PyAudio()
        gravador = audioDrive.open(input=True, channels=1, rate=self.rateValue, format=pyaudio.paInt16, input_device_index=0)
        while 1:
            resultado = gravador.read(bonecoChuck)
            valor = audioop.rms(resultado, 2)
            if self.debug:
                print("Valor de bloqueio {}".format(valor))
            if (valor > limiteDesbloqueio):
                break
