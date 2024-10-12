import numpy as np
import scipy.io.wavfile as wav

#specifications from the assignment prompt
sample_rate = 48000 #samples per second
duration = 1 #1 second duration
frequency = 440 #440 Hz frequency
amplitude = 8192 #1/4 the value of the max 16-bit signed

#creating the sample points of the file. The linspace function call will create an array of time values from 0 to duration.
#The time values will total out to sample_rate * duration = 48000. The endpoint parameter is set to False to exclude the endpoint.
sample_points = np.linspace(0, duration, sample_rate * duration, endpoint=False)

#creating the sine wave. To figure out how to code this, I referenced the following link: https://stackoverflow.com/questions/48043004/how-do-i-generate-a-sine-wave-using-python
#this will compute a sine wave with the specified frequency and sample points
sine_wave = np.sin(2 * np.pi * frequency * sample_points)

#to bring the sine wave to the correct amplitude, I multiply the sine wave by the amplitude
sine_wave_reduced = sine_wave * amplitude

#then, to bring the sine wave from floating point to 16-bit signed integers, I use numpy's built-in int16 function and apply it to the reduced sine wave
sine_wave_int = np.int16(sine_wave_reduced)

#now, i can write the resulting sine wave to a .wav file using scipy's wav.write function. I discovered this from the link: https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html
wav.write('sine_wave.wav', sample_rate, sine_wave_int)


#I'm using this print statement as a means to test the code execution
print(f"Sine wave written to file.\n")
print(f"Sample rate: {sample_rate}\nDuration: {duration}\nFrequency: {frequency}\nAmplitude: {amplitude}\n")