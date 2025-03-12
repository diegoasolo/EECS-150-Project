# generate_music-2 allows for clipping and speed adjustment
import os
import numpy as np
import soundfile as sf
import librosa
from pydub import AudioSegment

# Set working directory and folder
os.chdir(r"C:\Users\ezgao\Desktop\EECS-150-Project-1")
folder_name = "Processed_Notes"
folder_path = os.path.join(os.getcwd(), folder_name)  # Ensure full path to the folder

def load_audio_files():
    """Prompts user for filenames, loads them individually, and asks for unique adjustments."""
    
    file_names = input("Enter the titles of the .wav files (separated by a comma and space): ").split(", ")

    audio_segments = []
    desired_durations = []
    playback_speeds = []

    for index, file_name in enumerate(file_names):
        file_path = os.path.join(folder_path, f"{file_name}.wav")
        if os.path.exists(file_path):
            audio = AudioSegment.from_wav(file_path)
            duration_ms = len(audio)
            print(f"Clip '{file_name}' (instance {index+1}) duration: {duration_ms} ms")

            # Ask user for unique duration and speed for each instance
            new_duration = int(input(f"Enter desired duration (ms) for '{file_name}' (instance {index+1}): "))
            speed_factor = float(input(f"Enter playback speed for '{file_name}' (instance {index+1}) (e.g., 0.5 for 50%, 1 for 100%, 1.5 for 150%): "))

            audio_segments.append((file_name, file_path, duration_ms))
            desired_durations.append(new_duration)
            playback_speeds.append(speed_factor)
        else:
            print(f"Error: {file_path} not found. Skipping this file.")

    return audio_segments, desired_durations, playback_speeds

def match_target_volume(audio, target_dBFS=-20.0):
    """Normalize the volume of a single audio segment."""
    change_in_dBFS = target_dBFS - audio.dBFS
    return audio.apply_gain(change_in_dBFS)

def adjust_speed_sox(audio_path, speed_factor):
    """Speeds up or slows down an audio clip using high-quality SoX resampling."""
    y, sr = librosa.load(audio_path, sr=None)

    if speed_factor == 1.0:
        return AudioSegment.from_wav(audio_path)  # No speed change needed

    # High-quality time stretching using SoX-style resampling
    y_resampled = librosa.effects.time_stretch(y, rate=speed_factor)

    temp_file = "temp_speed_adjusted.wav"
    sf.write(temp_file, y_resampled, sr)

    return AudioSegment.from_wav(temp_file)

def stretch_audio_sox(audio, target_duration_ms):
    """Stretches audio to match the target duration while preserving pitch naturally."""
    original_duration = len(audio)

    if target_duration_ms == original_duration:
        return audio  # No stretching needed

    stretch_factor = target_duration_ms / original_duration

    y = np.array(audio.get_array_of_samples(), dtype=np.float32) / 32768.0
    sr = audio.frame_rate

    # High-quality SoX stretching with better smoothing
    y_stretched = librosa.effects.time_stretch(y, rate=stretch_factor)

    temp_file = "temp_stretched.wav"
    sf.write(temp_file, y_stretched, sr)

    return AudioSegment.from_wav(temp_file)
    

def combine_audio(audio_segments, desired_durations, playback_speeds, output_file):
    """Processes each instance of an audio segment separately and combines them."""
    if not audio_segments:
        print("No valid audio files were loaded.")
        return
    
    processed_segments = []
    for index, (file_name, file_path, _) in enumerate(audio_segments):
        speed_adjusted_audio = adjust_speed_sox(file_path, playback_speeds[index])
        stretched_audio = stretch_audio_sox(speed_adjusted_audio, desired_durations[index])
        normalized_audio = match_target_volume(stretched_audio)
        processed_segments.append(normalized_audio)

    combined_audio = sum(processed_segments)

    music_directory = "music"
    os.makedirs(music_directory, exist_ok=True)
    output_path = os.path.join(music_directory, output_file)
    combined_audio.export(output_path, format="wav")
    print(f"Audio successfully exported as {output_path}")

if __name__ == "__main__":
    print(f"Looking for .wav files in: {folder_path}")

    audio_segments, desired_durations, playback_speeds = load_audio_files()
    
    if audio_segments:
        output_file = "combined_audio.wav"
        combine_audio(audio_segments, desired_durations, playback_speeds, output_file)
