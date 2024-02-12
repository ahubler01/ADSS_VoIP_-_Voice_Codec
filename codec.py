from pydub import AudioSegment
import simpleaudio as sa
import threading

# Initialize a flag to control playback
playback_active = True

def simulate_codec_change(audio_segment, codec_name):
    """
    Simulates codec changes by altering audio properties.
    Returns the modified audio segment and its simulated bitrate.
    """
    # Example bitrates for simulation purposes
    codec_bitrates = {
        "G.711": 64,  # kbps
        "G.722": 128,  # kbps
        "G.729": 8,  # kbps
        "Opus": 48,  # Variable, example value
    }

    bitrate = codec_bitrates.get(codec_name, 64)

    return audio_segment, bitrate


def play_audio(audio_segment):
    """
    Plays the given audio segment.
    """
    global playback_active
    if not playback_active:
        return

    playback = sa.play_buffer(
        audio_segment.raw_data,
        num_channels=audio_segment.channels,
        bytes_per_sample=audio_segment.sample_width,
        sample_rate=audio_segment.frame_rate
    )
    playback.wait_done()


def user_input_listener():
    """
    Listens for user input to stop playback.
    """
    global playback_active
    while True:
        user_input = input().strip().lower()  # Read user input and normalize it
        if user_input == "stop":
            playback_active = False
            break


# Load the original audio file
audio_file = "music.wav"
original_audio = AudioSegment.from_file(audio_file, format="wav")

# Codecs
codecs = ["G.711", "G.722", "G.729", "Opus"]

# Start a thread to listen for user input to stop playback
input_thread = threading.Thread(target=user_input_listener, daemon=True)
input_thread.start()

# Segment and play the audio with simulated codec changes
segment_duration_ms = 5000  
for i in range(0, len(original_audio), segment_duration_ms):
    if not playback_active:
        print("Playback stopped by user.")
        break

    segment = original_audio[i:i + segment_duration_ms]
    codec_name = codecs[i // segment_duration_ms % len(codecs)]
    modified_segment, bitrate = simulate_codec_change(segment, codec_name)

    print(f"Playing segment with simulated {codec_name} codec at {bitrate} kbps")
    play_audio(modified_segment)
