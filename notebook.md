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