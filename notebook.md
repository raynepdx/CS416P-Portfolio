# Rayne Allen - PSU ID: 963230784

# *10/06/2024*
    * Created the README.md file with placeholder info.
    * Created a code directory where my programs and libraries will be held.
    * Created this notebook file, where dated entries of work and progress will be held.



# Friday, October 11th, 2024

I began creating the clipped.py program. This program generates a sine wave WAV file with the following specs:

* Channels per frame: 1 (mono)
* Sample format: 16 bit signed (values in the range -32767..32767)
* Amplitude: ¼ maximum possible 16-bit amplitude (values in the range -8192..8192)
* Duration: one second
* Frequency: 440Hz (440 cycles per second)
* Sample Rate: 48000 samples per second

I used the numpy and sciPy libraries to achieve this. I have little experience with the former,and no experience using the latter, but I found helpful info from these two links:
* https://stackoverflow.com/questions/48043004/how-do-i-generate-a-sine-wave-using-python
* https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html

Upon execution of the program, a wav file titled sine_wave.wav was added to the current directory. 

Takeaways:
* I desperately need to brush up on my knowledge of Python libraries and their corresponding usages and syntaxes. 

To-Do:
* Step 2 of the program specs, which is:
  * Extend the program to write a wave file called clipped.wav in the current directory. This file will consist of a 1/2-amplitude sine wave (values: -16384 to 16384). Samples that would be greater than 1/4 max amplitude should instead be maxed at 1/4 amplitude (8192), and those less than 1/4 min amplitude should be at -8192. Doing this will create a file where the Reaper (Audacity can suck it!) GUI displays it as a set of sine waves with their heads cut off. 




# Thursday, October 31st, 2024

It's been a while since the last entry in here. The last couple of weeks have been spent trying to understand the concepts presented in the class more comprehensively before trying my hand at coding again. Anyway, I created a program called audio_visualizer.py. This program allows a user to either load a file or generate a tone for a selected musical note. It uses the fft (fast Fourier transform) algorithm to display a visualization of the frequency spectrum of the chosen sound. To do this, I used matplotlib, scipy, and simpleaudio. Because I never worked with matplotlib before, I applied a lot of what I learned from the link: https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html

Here are my program functionalities so far:
* Audio generation: loads a wav file, converting it to mono if it is not natively stereo
* frequency spectrum visualization: converts the audio data from the time domain to the frequency domain using fft, focuses on a selected sound's frequency range, with a bandwidth range of +- 5 Hz, and updates the plot in real-time
* audio playback: plays the selected audio, synchronizing it with the visualizer

To Do:
* add a main function for the user interface
* create a function that allows the user to generate a tone from the spectrum of musical notes in the 4th octave 

# Tuesday, November 5th

I decided to remove functionality to load an audio file. It would have been redundant to load in a musical note when I can just use libraries like simpleaudio to play the selected frequency for me. I'm running into a bit of an issue with the matplot not plotting the frequency when I select a note. I think there could be a couple things causing this. I think I should try using plt.draw() to force the plot to update. Although, it could also be an issue of the tone generation happening quicker than the plot can update. To remedy this, I'll alter the program to ensure that the plot remains even after the tone goes away. 

# Wednesday, November 6th
I'm still running into the issues mentioned in my last entry. The sounds are generating correctly, and the plot window is appearing, but nothing appears on the plot, and the window closes automatically as well. I added 'plt.show(block=True)' to the function that generates the plot. No dice. I also added a prompt for user input that allows the user to exit the matplotlib window by pressing enter. Still no dice. I'll sift through the matplotlib documentation again tomorrow to see if I'm missing something. With that said, I've spent more time than I like on this program and want to start working on a program that adds various effects to a note.

# Friday, November 15th
I created a program using tkinter and simpleaudio that allows the user to select a musical note from a dropdown menu and then use checkboxes to apply distorion, delay, or reverb to the signal. To get a distorted signal, I used numpy to clip an audio signal to a specified threshold. This seemed to be the most apparent effect, as the delay and reverb options produce a subtle change. For delay, I appended a time-shifted copy of the original audio signal to itself, using the formula delayed_signal[i] = original_signal[i] + decay(signal(i - delay_samples)), with decay and delay_samples being parameters to the function. For reverb, I used the formula delay_samples = int(i * delay_ms * sample_rate / 1000) within a for-loop that goes from i to num_echoes + 1 (num_echoes is a parameter that I set to 5, although I may want to increase this to make the effect more apparent). This adds multiple delayed/decayed versions of the original signal to create an echo effect. I had to do some debugging when it didn't seem that checking off the fx options were having an impact on the sound. In the main function, I added print statements that returned true or false if an effect was checked off. The values returned were correct, so I could tell that the tkinter checkboxes were working correctly. In the play_with_fx function, I was initially using if-elif-elif statements to apply the fx. I realized that this prevented multiple fx from being applied at the same time, so I changed them all to if-statements. I then realized that the intensity of the fx wasn't high enough, so I lowered the distortion threshold to make the clipping more audible. I also increased the delay time and decay for the delay effect, and increased the number of echoes for the reverb function. This seemed to solve the problem, although I'm considering adjusting the latter two fx even more to make them more apparent.  

# Wednesday, Novermber 20th
I started on the adaptive tone control program that Bart recommended. I thought it would be cool to put a spin on it and take in real-time audio from the user's mic to process, as opposed to an input file. With that said, I'm planning on adding the latter functionality this week. I used pyaudio to capture the audio from a mic in chunks (got help from https://people.csail.mit.edu/hubert/pyaudio/docs/#class-pyaudio, https://docs.scipy.org/doc/scipy/tutorial/signal.html, and https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html) and then used my process function to adjust the power in the predefined bands. Even though it's redundant, I thought it'd be fun to make the ATC a class to keep all the functions in. I haven't done much OOP with Python since CS302 and I felt like it's good practice. I can also easily add more functionality to the program by creating other classes. My create_filters function uses the butter function of scipy.signal to create low, mid, and high-pass butterworth filters. Calc_signal_power finds the total power in a specific band from FFT data. Process_audio_chunk takes a chunk of audio (at 1024 samples each), finds its frequency, adjusts the power of each band, and uses FFT to reconstruct the time-domain sigtnal. Finally, process_audio takes in the real time pyaudio I/O stream. Some things I want to do next to it:

* Add the ability to input a file
  * definitely a wav file, but maybe figure out how to input an mp3?
  * output the audio from the file to speakers
* I'm thinking of using tkinter again to add a GUI for the program. Maybe let the user adjust the band weighting manually

# Tuesday, December 10th
I copied the popgen file from the class Github page and decided to focus on creating an envelope and creating functionality for choosing between different waveforms. I did this by taking the attack, release, and sustain and making them linear with np.linspace(args). The envelope function then returns each of the linear envelopes as a concatenation. I then altered the make_note function by creating the variable env and setting it to the returned result of the envelope function, and then made the make_note function return waveform * env. In addition, I altered the parameters of make_waveform to take in the type. This can be altered on like 220 for melody and 223 for bass. I made an if-elif-else statement that evaluates the type passed into the function and returns a different type of waveform (sine, square, sawtooth, and triangle).