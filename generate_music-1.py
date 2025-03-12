import os
from pydub import AudioSegment
# generate_music-1.py allows for a generalized volume adjustment and combining audio files together. this is best shortened version for class demo. 
# Set working directory and folder
os.chdir(r"C:\Users\ezgao\Desktop\EECS-150-Project-1")
folder_name = "Processed_Notes"
folder_path = os.path.join(os.getcwd(), folder_name)  # Ensure full path to the folder

def load_audio_files():
    """Prompts user for filenames, loads them, and returns a list of audio segments in order."""
    
    # Prompt user to enter file titles (comma-separated)
    file_names = input("Enter the titles of the .wav files (separated by a comma and space): ").split(", ")

    # Load audio files in the order they were typed
    audio_segments = []
    for file_name in file_names:
        file_path = os.path.join(folder_path, f"{file_name}.wav")  # Correctly join path
        if os.path.exists(file_path):
            audio_segments.append(AudioSegment.from_wav(file_path))
        else:
            print(f"Error: {file_path} not found. Skipping this file.")

    return audio_segments

def combine_audio(audio_segments, output_file):
    """Combines audio segments into one and exports it as a .wav file."""
    if not audio_segments:
        print("No valid audio files were loaded.")
        return

def match_target_volume(audio, target_dBFS=-20.0):
    """Normalize the volume of a single audio segment."""
    change_in_dBFS = target_dBFS - audio.dBFS
    return audio.apply_gain(change_in_dBFS)

def combine_audio(audio_segments, output_file):
    """Normalizes each audio segment, combines them, and exports as a .wav file."""
    if not audio_segments:
        print("No valid audio files were loaded.")
        return
    
    # Normalize each segment individually
    normalized_segments = [match_target_volume(audio) for audio in audio_segments]

    # Combine all normalized audio segments
    combined_audio = sum(normalized_segments)
  #  combined_audio = sum(audio_segments)  # Combine all audio segments

    music_directory = "music"
    os.makedirs(music_directory, exist_ok=True)

    # Prompt the user for the desired file name
    custom_name = input("Enter the desired name for the audio file (without extension): ").strip()
    if not custom_name:
        print("Invalid file name. Using 'untitled_audio' as default.")
        custom_name = "untitled_audio"

    output_file = f"{custom_name}.wav"
    output_path = os.path.join(music_directory, output_file)

    combined_audio.export(output_path, format="wav")
    print(f"Audio successfully exported as {output_path}")

   # output_path = os.path.join(folder_path, output_file)  # Save in the same Processed_Notes folder
   # combined_audio.export(output_path, format="wav")
   # print(f"Audio successfully exported as {output_path}")

if __name__ == "__main__":
    # Print the correct folder path for debugging
    print(f"Looking for .wav files in: {folder_path}")

    audio_segments = load_audio_files()
    
    if audio_segments:
        output_file = "combined_audio.wav"
        combine_audio(audio_segments, output_file)
