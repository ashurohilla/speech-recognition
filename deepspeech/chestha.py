from deepspeech import Model
import numpy as np
import os
import wave

from IPython.display import Audio
model_file_path = 'deepspeech-0.9.3-models.pbmm'
lm_file_path = 'deepspeech-0.9.3-models.scorer'
beam_width = 100
lm_alpha = 0.93
lm_beta = 1.18

model = Model(model_file_path)
model.enableExternalScorer(lm_file_path)
model.setScorerAlphaBeta(lm_alpha, lm_beta)
model.setBeamWidth(beam_width)
def read_wav_file(filename):
    with wave.open(filename, 'rb') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)
        print("Rate:", rate)
        print("Frames:", frames)
        print("Buffer Len:", len(buffer))
    return buffer, rate
 
def transcribe_batch(audio_file):
    buffer, rate = read_wav_file(audio_file)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    return print(model.stt(data16)) 
Audio('audio\._4507-16021-0012.wav')
Audio('speech_woman.wav')
transcribe_batch('audio/4507-16021-0012.wav')
stream = model.createStream()
from IPython.display import clear_output

def transcribe_streaming(audio_file):
    buffer, rate = read_wav_file(audio_file)
    offset=0
    batch_size=8196
    text=""

    while offset < len(buffer):
      end_offset=offset+batch_size
      chunk=buffer[offset:end_offset]
      data16 = np.frombuffer(chunk, dtype=np.int16)

      stream.feedAudioContent(data16)
      text=stream.intermediateDecode()
      clear_output(wait=True)
      print(text)
      offset=end_offset
    return True
transcribe_streaming('speech_man.wav')        