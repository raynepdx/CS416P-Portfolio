"""
This program is a musical note player with effects that the user can select to apply to the notes.
The user can:
1. Select a muscial note from a dropdown menu
2. play the selected note clean with no fx
3. Apply an audio effect to the note before playing it (reverse, echo, reverb, chorus, flanger, phaser, tremolo, vibrato)
"""

import tkinter as tk #using tkinter for GUI
from tkinter import ttk #for dropdown menu
import numpy as np #for mathematical operations and signal generation
import simpleaudio as sa #for audio playback

#dictionary of musical notes and their frequencies in Hz
notes = {'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'G4': 392.00, 'G#4': 415.30, 'A4': 440.00, 'A#4': 466.16, 'B4': 493.88, 'C5': 523.25}

# Function to generate a sine wave of a given frequency and duration
def generate_sine_wave(frequency, duration = 2, sample_rate = 44100):
    
    #generate time values from 0 to the duration with steps corresponding to the sample rate
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    #generate a sine wave with the given frequency and time values
    wave = 0.5 * np.sin(2 * np.pi * frequency * t) #using 0.5 to scale the amplitude to 0.5
    return wave #return the generated wave




#function to apply distorion by clipping the audio signal
def apply_distortion(samples, threshold = 0.3):
    
    #clip the audio signal to lie within -threshold and threshold
    distorted = np.clip(samples, -threshold, threshold)

    print("Distortion applied", distorted[:10]) #checking to see if distortion is applied. debugging purposes

    return distorted



#function to apply delay to the audio signal
def apply_delay(samples, delay_ms=1000, decay=0.8, sample_rate=44100):
    
    #calculate the number of samples corresponding to the delay in milliseconds
    delay_samples = int(sample_rate * delay_ms / 1000)

    #create an array of zeros to hold the original signal and delayed signal
    delayed_signal = np.zeros(len(samples) + delay_samples)

    #add the original signal to the delayed signal array
    delayed_signal[:len(samples)] += samples

    #add the delayed, decayed version of the signal
    delayed_signal[delay_samples:] += decay * samples

    print("Delay applied", delayed_signal[:10]) #checking to see if delay is applied. debugging purposes

    #return only the part matching the original length
    return delayed_signal[:len(samples)]



#function to apply reverb to the audio signal
def apply_reverb(samples, decay=0.6, num_echoes=10, delay_ms=100, sample_rate=44100):
    
    #create a copy of the original signal to modify
    reverb_signal = np.copy(samples)

    #loop to add multiple delayed/decyed versions of the signal
    for i in range(1, num_echoes + 1):
        #calculate the delay for each echo
        delay_samples = int(i * delay_ms * sample_rate / 1000)

        #ensure that delay deosnt exceed the length of the signal
        if delay_samples < len(samples):
            #add the delayed, decayed version of the signal
            reverb_signal[delay_samples:] += samples[:-delay_samples] * (decay ** i)

    print("Reverb applied", reverb_signal[:10]) #checking to see if reverb is applied. debugging purposes

    return reverb_signal


#function to play the note without any fx
def play_clean():

    #get the selected note from the dropdown menu
    note = note_dropdown.get()

    #ensure the selected note is valid
    if note in notes:

        #get the frequency of the selected note
        frequency = notes[note]

        #generate a sine wave of the selected frequency
        samples = generate_sine_wave(frequency)

        #play the generated sine wave
        play_audio(samples)

#function to normalize audio signal after all fx are applied to make sure the signal is within the range of -1 to 1
def normalize(samples):
    #get the maximum absolute value of the signal
    max_val = np.max(np.abs(samples))

    #normalize the signal by dividing by the maximum value
    if max_val > 0:
        return samples / max_val

    return samples


#function to play the note with the selected fx
def play_with_fx():

    #get the selected note from the dropdown menu
    note = note_dropdown.get()

    #make sure that the selected note is valid
    if note in notes:

        #get the frequency of the selected note
        frequency = notes[note]

        #generate a sine wave of the selected frequency
        samples = generate_sine_wave(frequency)

        #adding print statements to debug. currently having an issue where the audio doesnt sound different with fx
        print("Distortion: ", fx_vars["Distortion"].get())
        print("Delay: ", fx_vars["Delay"].get())
        print("Reverb: ", fx_vars["Reverb"].get())


        #apply fx based on the user's selection in the dropdown menu
        if fx_vars["Distortion"].get():
            samples = apply_distortion(samples)

        if fx_vars["Delay"].get():
            samples = apply_delay(samples)

        if fx_vars["Reverb"].get():
            samples = apply_reverb(samples)

        #normalize the signal after applying all fx
        samples = normalize(samples)

        #play the generated sine wave with the selected fx
        play_audio(samples)



#function to play the audio signal
def play_audio(samples, sample_rate=44100):
    
    #convert float samples to 16-bit integers
    audio = (samples * 32767).astype(np.int16)

    #play the audio with the simpleaudio library
    sa.play_buffer(audio, num_channels=1, bytes_per_sample=2, sample_rate=sample_rate)



#main function to create the GUI
def main():

    global note_dropdown, fx_vars #making globals for GUI components

    #create the main window
    root = tk.Tk()
    root.title("Musical Note Player with Effects") #set the title of the window

    #add a label for the note dropdown menu
    note_label = tk.Label(root, text="Select a note:")
    #place the label in the window
    note_label.pack()

    #create a dropdown menu for selecting a note
    note_dropdown = ttk.Combobox(root, values=list(notes.keys()))
    #place the dropdown menu in the window
    note_dropdown.pack()


    #create checkboxes for selecting fx
    fx_vars = {"Distortion": tk.BooleanVar(), "Delay": tk.BooleanVar(), "Reverb": tk.BooleanVar()}

    #loop through each effect
    for effect, var in fx_vars.items():
        #create a checkbox for each effect
        checkbox = tk.Checkbutton(root, text=effect, variable=var)
        #place the checkbox in the window
        checkbox.pack()


    #add a button to play the selected note clean
    play_clean_button = tk.Button(root, text="Play Clean", command=play_clean)
    #place the button in the window
    play_clean_button.pack()

    #add a button to play the selected note with fx
    play_with_fx_button = tk.Button(root, text="Play with FX", command=play_with_fx)
    #place the button in the window
    play_with_fx_button.pack()

    #add button to close the application
    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    #place the button in the window
    exit_button.pack()

    root.mainloop() #run the main loop of the window


if __name__ == "__main__":
    main() #run the main function