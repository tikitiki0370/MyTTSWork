from espnet2.bin.tts_inference import Text2Speech
import time
import torch
import numpy as np

fs, lang = 44100, "Japanese"
model= "./100epoch.pth"


text2speech = Text2Speech.from_pretrained(
    model_file=model,
    device="cpu",
    speed_control_alpha=1.0,
    noise_scale=0.333,
    noise_scale_dur=0.333,
)
pause = np.zeros(30000, dtype=np.float32)
x = "これはテストメッセージです"

with torch.no_grad():
    start = time.time()
    wav = text2speech(x)["wav"]
rtf = (time.time() - start) / (len(wav) / text2speech.fs)
print(f"RTF = {rtf:5f}")

from scipy.io.wavfile import write
wav_list = []
wav_list.append(np.concatenate([wav.view(-1).cpu().numpy(), pause]))
final_wav = np.concatenate(wav_list)
write("gen_file.wav", rate=text2speech.fs, data=final_wav)