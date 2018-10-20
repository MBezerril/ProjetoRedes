import simpleaudio as sa
import threading as thrd
import pyaudio
import wave
import audioop
from time import sleep


class CamadaFisica:
    def __init__(self):
        self.canPlay = False
        self.executor = None
        self.chunkSize = 1024
        self.limite = 500
        self.rateValue = 48000
        self.intervalo = 0.5


    def stopWrite(self):
        self.canPlay = False

    def write(self, data):
        print(type(data))
        self.canPlay = True
        self.executor = thrd.Thread(target=self._writing, args=(data,))
        self.executor.start()

    def _writing(self, data):
        wave_obj = sa.WaveObject.from_wave_file("beep-04.wav")
        play_obj = wave_obj.play()
        for i in data:
            play_obj.stop()
            if i == 1:
                play_obj = wave_obj.play()
            sleep(self.intervalo)
            if not self.canPlay:
                break

    def read(self, size):
        """
        Recebe a quantidade de bits a serem lidos (size) e retorna o array de bits lidos
        Caso precise apenas de uma leitura instatanea, passar 0 ou 1
        :param size:
        :return list[size]:
        """
        valor = 0 #Valor obtido pelas leituras da biblioteca no microfone
        lido = 0 #Qual bit foi lido
        resultado = 0
        arrayRetorno = []#array resultado das leituras de tamanho size que será o retorno
        if size < 1:
            size = 1
        quantLeitura = int(self.rateValue / self.chunkSize * self.intervalo) #Leituras a serem feitas para ser o equivalente a uma leitura de duração igual ao intervalo
        audioDrive = pyaudio.PyAudio()
        gravador = audioDrive.open(input=True, channels=1, rate=self.rateValue, format=pyaudio.paInt16, input_device_index=0)
        """while 1:
            resultado = gravador.read(self.chunkSize)
            valor = audioop.rms(resultado, 2)
            if valor > self.limite:
                break     
        """
        for r in range(size): #controla a quantidade de bits a serem lidos
            for i in range(quantLeitura): #controla o tempo de coleta de gravação pra equivaler a duração do invtervalo
                resultado = gravador.read(self.chunkSize)
                valor = audioop.rms(resultado, 2)
                if valor > self.limite:
                    lido = 1
            arrayRetorno.append(lido) #Insercao na list de retorno
            lido = 0
        return arrayRetorno