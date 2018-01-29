import pyaudio
import wave

# set desired values
start = 0
length = 1

# open wave file
wave = wave.open('output.wav', 'rb')

# initialize audio
py_audio = pyaudio.PyAudio()
stream = py_audio.open(format=py_audio.get_format_from_width(wave.getsampwidth()),
                       channels=wave.getnchannels(),
                       rate=wave.getframerate(),
                       output=True)

# skip unwanted frames
n_frames = int(start * wave.getframerate())
wave.setpos(n_frames)

# write desired frames to audio buffer
n_frames = int(length * wave.getframerate())
frames = wave.readframes(n_frames)
stream.write(frames)

# close and terminate everything properly
wave.close()
stream.close()
py_audio.terminate()
