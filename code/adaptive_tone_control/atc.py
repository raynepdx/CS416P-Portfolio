#I've been using simple audio, but I wanted to mess around with a different library. I'm going to use pyaudio, and I am using a fair bit of the syntax found here: https://people.csail.mit.edu/hubert/pyaudio/docs/#class-pyaudio
#I also needed to go off of https://docs.scipy.org/doc/scipy/tutorial/signal.html and https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html to use scipy.signal to filter for low, high, and mid bands, and to know
#how to use the butter function to create a butterworth filter, that way there are gradual transitions between the passband and stopband

import pyaudio
import numpy as np
import scipy.signal as signal
import scipy.fft as fft

#decided to use a class this time. I haven't touched OOP in python in a hot minute

class AdaptiveToneControl:
    def __init__(self, sample_rate=44100, chunk_size=1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.filters = self.create_filters()

    def create_filters(self):
        #tone control filters for low, mid, high

        low = 300 
        mid = (300, 2000)
        high = 2000

        #butterworth filters
        low_filter = signal.butter(4, low / (self.sample_rate / 2), 'low', output='sos')
        mid_filter = signal.butter(4, np.array(mid) / (self.sample_rate / 2), 'mid', output='sos')
        high_filter = signal.butter(4, high / (self.sample_rate / 2), 'high', output='sos')

        #using a dict to store the filters, so i can label their output
        return {'low': low_filter, 'mid': mid_filter, 'high': high_filter}
    

    def calc_signal_power(frequencies, fft_data, band):
        #calculating the power of the signal in a given band

        #mask band frequencies
        mask = (frequencies > band[0]) & (frequencies <= band[1])

        #sum of squared magnitudes of the fft data
        power = np.sum(np.abs(fft_data[mask])**2)

        return power
    


    def process(self, data):
        #adjusting the audio chunk to balance the power of the low, mid, and high bands

        #fft to analyze the frequencies
        fft_data = fft.rfft(data)
        frequencies = fft.rfftfreq(len(data), 1 / self.sample_rate)

        #definition of frequency bands
        low = (0, 300)
        mid = (300, 2000)
        high = (2000, self.sample_rate // 2) #nyquist frequency is half the sample rate

        #calculating the power of the signal in each band using the above function
        low_power = self.calc_signal_power(frequencies, fft_data, low)
        mid_power = self.calc_signal_power(frequencies, fft_data, mid)
        high_power = self.calc_signal_power(frequencies, fft_data, high)

        #using the average power across every band to normnalize the power of the signal. should i use '//' or '/'? maybe having a whole number is better?
        avg_power = (low_power + mid_power + high_power) / 3

        #nornalizing the power of the signal in each band. in the adjustment factor, I'm adding 1 **-9 to avoid dividing by zero
        normalized = {
            'low:': avg_power / (low_power + 1e-9),
            'mid': avg_power / (mid_power + 1e-9),
            'high': avg_power / (high_power + 1e-9)
        }

        #using sosfilt to apply my create_filters to the data
        filtered = {
            signal.sosfilt(self.filters['low'], data) * normalized['low'] + 
            signal.sosfilt(self.filters['mid'], data) * normalized['mid'] + 
            signal.sosfilt(self.filters['high'], data) * normalized['high'] 
        }

        return filtered
    

    def process_audio(self):
        #take audio input in real time from a mic, balance the frequency bands, and play the adjusted audio

        #initialize pyaudio for input and output
        p = pyaudio.PyAudio()

        #open a stream for input
        stream = p.open(format=pyaudio.paFloat32
                        channels = 1,
                        rate=self.sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=self.chunk_size)
        
        print("Stream started. Say something, or press ctrl+C to stop")

        try:
            while True:
                #read chunk of audio data from the mic
                data = np.frombuffer(stream.read(self.chunk_size), dtype=np.float32)

                #process the audio data to balance the frequency bands
                processed = self.process(data)

                #write the processed audio data to the output stream
                stream.write(processed.astype(np.float32).tobytes())

        except KeyboardInterrupt:
            print("Stream stopped")

        finally:
            #close the stream
            stream.stop_stream()
            stream.close()
            p.terminate()
        
    


def main():
    eq = AdaptiveToneControl()
    eq.process_audio()

if __name__ == '__main__':
    main()