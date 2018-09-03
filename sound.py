import pyaudio
import wave
import audioop
from time import sleep

tempo = 0.5
chunkSize = 1024
limite = 500
rateValue = 48000
resultado = 0
valor = 0
lido = 0
quantLeitura = int(rateValue/chunkSize*tempo)

audioDrive = pyaudio.PyAudio()
gravador = audioDrive.open(input=True, channels=1, rate=rateValue, format=pyaudio.paInt16, input_device_index = 0)
min = audioop.rms(gravador.read(chunkSize), 2)
max = audioop.rms(gravador.read(chunkSize), 2)
while 1:
	resultado = gravador.read(chunkSize)
	valor = audioop.rms(resultado, 2)
	if(valor >  limite):
		break
while 1:
	for i in range(quantLeitura):
		resultado = gravador.read(chunkSize)
		valor = audioop.rms(resultado, 2)
		if(valor >  limite):
			lido = 1
	if(lido ==1):
		print("1 : ", valor)
	else:
		print("0 : ", valor)
	lido = 0

exit()