from time import sleep
import simpleaudio as sa

wave_obj = sa.WaveObject.from_wave_file("beep-04.wav")
play_obj = wave_obj.play()

x = [1,0,0,0,1,1,1,0,0,1,0]
x1 = [1,0,1,0,1,0,1,0,1,0,1]

for i in x:
	if(i==1):
		play_obj = wave_obj.play()
	sleep(1)