
import glob
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

from tqdm import tqdm


file_wav = glob.glob(
        r".\output\**\2023_02_22\*.wav", recursive=True)

os.makedirs(fr".\output\cut_wavfile\2023_02_22", exist_ok=True)
for i in tqdm(file_wav, desc="cut wav"):
    tqdm.write(f"cut {i}")
    sound = AudioSegment.from_file(i, format="wav")
    chunks = split_on_silence(sound, min_silence_len=1500, silence_thresh=-40, keep_silence=400)
    for j, chunk in enumerate(chunks):
        chunk.export(f".\\output\\cut_wavfile\\2023_02_22\\{os.path.splitext(os.path.basename(i))[0]}+{j}.wav", format="wav")
        tqdm.write(f"make {i}+{j}")
    tqdm.write(f"cut {i} done")