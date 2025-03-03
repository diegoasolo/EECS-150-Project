import numpy as np
import math
import librosa
import librosa.display
import scipy.signal
import os
import matplotlib.pyplot as plt


def load_audio(file_path , sample_rate=22050):
    """ Load an audio file and return its waveform and sample rate. """
    audio, sr = librosa.load(file_path, sr=sample_rate)
    return audio, sr


def compute_fft(audio, sr):
    """ Compute and return the FFT frequency spectrum of the audio. """
    fft_spectrum = np.abs(np.fft.rfft(audio))
    freqs = np.fft.rfftfreq(len(audio), d=1/sr)
    return freqs, fft_spectrum


def plot_fft(freqs, spectrum, title="Frequency Spectrum"):
    """ Plot the FFT spectrum for visualization. """
    plt.figure(figsize=(10, 4))
    plt.plot(freqs, spectrum, color='blue')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.xlim(0, 5000)  # Limit to human hearing range
    plt.show()

def analyze_fft(freqs, spectrum):
    ''' Find Max freqnecy from fft plot'''
    max_index = np.argmax(spectrum)

    max_spec = spectrum[max_index]
    max_freq = freqs[max_index]
    
    return max_freq

def frequency_to_note(freq):
    '''converts freqnecy into its coresponding note in 12-tone equal temeperment'''
    
    A4 = 440.0 #refrence note
    n =  12 * np.log2(freq/ A4)
    n_rounded = int(round(n))

    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    note_index = (n_rounded + 9) % 12
    note = note_names[note_index]
    octave = (n_rounded + 9) // 12 + 4

    return note, octave 



def main():

    folder_name = "audio_files"  # Change this to your folder name
    file_name = "piano-a_A_major.wav"  # Insert File name to be analysiised

    
    file_path = os.path.join(folder_name, file_name)

    audio, sr = load_audio(file_path)
    freqs, spectrum = compute_fft(audio, sr)
    max_freq = analyze_fft(freqs, spectrum) 
    max_note, max_octave = frequency_to_note(max_freq)
    print("Max frequency is", int(max_freq) , f"Hz or {max_note}{max_octave}")
    plot_fft(freqs, spectrum, title=f"Frequency Spectrum of {file_name}")
   
      

if __name__ == "__main__":
    main()
