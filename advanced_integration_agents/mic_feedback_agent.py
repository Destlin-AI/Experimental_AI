
import sounddevice as sd
import numpy as np
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

def listen(duration=3, fs=16000):
    print("🎙️ Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    return audio.flatten()

def transcribe(audio):
    inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    ids = torch.argmax(logits, dim=-1)
    return processor.batch_decode(ids)[0]

if __name__ == "__main__":
    audio = listen()
    text = transcribe(audio)
    print(f"🗣️ You said: {text}")
