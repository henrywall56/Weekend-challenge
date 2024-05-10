import wave

def bin_to_wav(bin_file, wav_file, sample_width, sample_rate, channels):
    with open(bin_file, 'rb') as f:
        data = f.read()

    # Assuming the data in the binary file is in little-endian format
    audio_data = np.frombuffer(data, dtype=np.int16)

    # Reshape the data according to the number of channels
    audio_data = audio_data.reshape((-1, channels))

    with wave.open(wav_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

# Example usage
bin_file = 'raw2.bin'
wav_file = 'output2.wav'
sample_width = 2  # in bytes (16-bit)
sample_rate = 48000  # in Hz
channels = 1  # stereo

bin_to_wav(bin_file, wav_file, sample_width, sample_rate, channels)