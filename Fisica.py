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
        self.limite = 500
        self.rateValue = 48000
        self.intervalo = 1 #<<<<<<<<<<<<


    def write(self, data):
        self.executor = thrd.Thread(target=self._writing, args=[data])
        self.executor.start()

    def _writing(self, data):
        signal = []
        wave_obj = sa.WaveObject.from_wave_file("beep-04.wav")
        play_obj = wave_obj.play()
        if data == 1:
            signal = [0,1]
        elif data == 0:
            signal = [1, 0]
        elif data == 'borda':
            signal = [1, 1]
        for i in signal:
            if i == 1:
                play_obj = wave_obj.play()
                sleep(self.intervalo/2)
                play_obj.stop()
            else:
                sleep(self.intervalo/2)


    def read(self):
        """
        Lê uma amostra e diz se é uma borda de uma transmissão (iniciou ou final), se o meio está livre ou o bit 0 ou 1
        :param size:
        :return list[size]:
        """
        valor = 0 #Valor obtido pelas leituras da biblioteca no microfone
        inicio = 0 #Qual bit foi lido
        final = 0
        resultado = 0
        quantLeitura = int(self.rateValue / self.chunkSize * self.intervalo) #Leituras a serem feitas para ser o equivalente a uma leitura de duração igual ao intervalo
        audioDrive = pyaudio.PyAudio()
        gravador = audioDrive.open(input=True, channels=1, rate=self.rateValue, format=pyaudio.paInt16, input_device_index=0)

        for i in range(quantLeitura/2): #controla o tempo de coleta de gravação pra equivaler a duração do invtervalo
            resultado = gravador.read(self.chunkSize)
            valor = audioop.rms(resultado, 2)
            if valor > self.limite:
                inicio = 1
        for i in range(quantLeitura/2): #controla o tempo de coleta de gravação pra equivaler a duração do invtervalo
            resultado = gravador.read(self.chunkSize)
            valor = audioop.rms(resultado, 2)
            if valor > self.limite:
                final = 1

        if(inicio!=final):
            return final
        else:
            if final is 0: # TESTAR SE É ==
                return None
            else:
                return 'borda' #2
