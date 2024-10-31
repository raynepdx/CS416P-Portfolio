#this program is going to take in an audio file and create a visual representation
#of the audio file using the fast fourier transform
#I'm also going to use a dictionary of note frequencies to let the user pick a note to be played and 
#perform the fft on.
# #to help with this I used the following documentation: https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html

import numpy as np
import matplotlib.pyplot as plt #for plotting the spectrogram
import scipy.io.wavfile as wav
import scipy.fftpack as fft #to perform fft on audio data
import simpleaudio as audio
import os


#dictionary of 4th octave note frequencies
note_freqs = {
    'C': 261.63,
    'C#': 277.18,
    'D': 293.66,
    'D#': 311.13,
    'E': 329.63,
    'F': 349.23,
    'F#': 369.99,
    'G': 392.00,
    'G#': 415.30,
    'A': 440.00,
    'A#': 466.16,
    'B': 493.88
}

CHUNK = 1024 #number of samples to read at a time
DURATION = 2 #duration of the audio playback

#function to filter the fft data around a specific frequency. bandwidth is the upper and lower bound of the target frequency
def filter_fft(fft_data, frequencies, target_freq, bandwidth=5):
    #set the range around the target frequency
    lower = target_freq - bandwidth
    upper = target_freq + bandwidth

    #mask the fft data to only include the target frequency
    mask = (frequencies >= lower) & (frequencies <= upper)

    return fft_data[mask], frequencies[mask]



def load_file(file_path):
    #loading the audio file
    if not os.path.isfile(file_path) or not file_path.lower().endswith('.wav'):
        raise ValueError("Invalid file path. Please provide a valid .wav file.")
        return None, None
    
    sample_rate, audio_data = wav.read(file_path)

    #converting to mono if the audio is native stereo
    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1) / 2

    return sample_rate, audio_data


#function to play the audio and visualize the frequency spectrum  around the target frequency
def visualize_spectrum(audio_data, sample_rate, target_freq, bandwidth=5):
    #setting up a plot using matplotlib
    plt.ion() #turning on interactive mode
    fig, ax = plt.subplots() #creating a figure and axis object
    x = np.linspace(0, sample_rate / 2, CHUNK // 2) #creating the x-axis for the plot
    line, = ax.plot(x, np.zeros(CHUNK // 2)) #creating the line object for the plot
    ax.set_xlim(target_freq - 10, target_freq + 10) #setting the x-axis limits
    ax.set_ylim(0, 1) #setting the y-axis limits
    ax.set_xlabel("Frequency (Hz)") #setting the x-axis label
    ax.set_ylabel("Amplitude") #setting the y-axis label

    #setting up playback of the audio
    playback = audio.play_buffer(audio_data, 1, 2, sample_rate)

    #process, visualize in chunks
    try:
        for i in range(0, len(audio_data), CHUNK):
            if not playback.is_playing(): #if the audio is done playing, break out of the loop
                break

            chunk_data = audio_data[i:i + CHUNK] #getting the chunk of audio data
            if len(chunk_data) < CHUNK: #if the chunk is less than the chunk size, break out of the loop
                break

            fft_data = np.abs(fft.fft(chunk_data))[:CHUNK // 2] #performing the fft on the chunk of audio data
            frequencies = np.linspace(0, sample_rate / 2, CHUNK // 2) #creating the x-axis for the fft data

            #filtering the fft data around the target frequency
            filtered_fft, filtered_freqs = filter_fft(fft_data, frequencies, target_freq, bandwidth)

            #updating the plot with the filtered fft data
            line.set_xdata(filtered_freqs)
            line.set_ydata(filtered_fft)
            plt.pause(0.01) #pausing for a short time to allow the plot to update

    except KeyboardInterrupt: #if the user interrupts the program, stop the audio playback
        playback.stop()
        plt.close() #close the plot

    finally:
        plt.ioff() #turn off interactive mode
        plt.show() #show the plot


#main function to handle user interface