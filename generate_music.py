from pydub import AudioSegment
import os

#get user input on note + note duration
def user_input():
    notes = input("Enter the notes in order: ").split()
    durations_input = input("Enter the duration of each note in order (in seconds): ").split()
    durations = []
    for duration in durations_input:
        durations.append(float(duration))

    return notes, durations

#pair note input with note audio
def load_audio_files(notes):
    audio_files = {}
    for note in notes:
        file_name = f"{note}.wav"
        if os.path.exists(file_name):
            audio_files[note] = AudioSegment.from_wav(file_name)
        else:
            print(f"Error: {file_name} could not be found")
            return None
    return audio_files


def adjust_note_duration(audio, desired_duration):
    #get current note audio duration
    current_duration = len(audio) / 1000.0 #convert ms to s
    desired_duration_ms = desired_duration * 1000 #desired duration in ms

    if desired_duration < current_duration:
        audio = audio[:int(desired_duration_ms)]
    elif desired_duration > current_duration:
        repeat_count = int(desired_duration_ms / len(audio)) + 1
        audio = audio * repeat_count
        audio = audio[:int(desired_duration_ms)]
    return audio

def create_final_audio(notes, durations, audio_files):
    final_audio = audio_segment.silent(duration=0) #initialiaze empty audio for concatenation

    for note, duration in zip(notes, durations):
        audio = audio_files[note]
        audio_correct_duration = adjust_note_duration(audio, duration)
        final_audio += audio_correct_duration

    return final_audio

def main():
    #get user input
    notes, durations = user_input()

    #load audio files
    audio_files = load_audio_files(notes)
    if audio_files is None:
        return

    #create final audio
    final_audio = create_final_audio(notes, durations, audio_files)

    #create and export final audio file
    output_file = "custom_song.wav"
    final_audio.export(output_file, format="wav")
    print(f"Final audio saved to {output_file}")

if __name__ == "__main__":
    main()
