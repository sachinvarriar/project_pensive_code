# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:08:59 2024

@author: sachin
"""

from openai import OpenAI

client = OpenAI()

import pyaudio
import wave
from pydub import AudioSegment

def record_audio(file_path, duration=60, sample_rate=44100, channels=2, chunk=1024):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    print("Recording...")

    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio as a WAV file
    wave_file_path = file_path.replace(".mp3", ".wav")
    wf = wave.open(wave_file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Convert WAV to MP3 using pydub
    audio = AudioSegment.from_wav(wave_file_path)
    audio.export(file_path, format="mp3")

    print(f"Audio saved as {file_path}")

if __name__ == "__main__":
    file_path = "output.mp3"  # Change this to the desired output file path
    record_audio(file_path, duration=60)
