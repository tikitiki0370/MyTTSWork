import glob
import os
import shutil

import speech_recognition as sr
from tqdm import tqdm

r = sr.Recognizer()

files = glob.glob(r"output\cut_wavfile\2023_02_22\*.wav", recursive=True)

for audio_file in tqdm(files):
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    text = r.recognize_google(audio, language="ja-JP", show_all=True)
    text = text["alternative"][0]["transcript"]
    folder_name = text[0:5].replace(" ", "_")

    os.makedirs(rf"output\speech\{folder_name}", exist_ok=True)

    if not os.path.exists(r"output\speech\result.txt"):
        with open(r"output\speech\result.txt", "w", encoding="utf-8"):
            pass

    with open(r"output\speech\result.txt", "a", encoding="utf-8") as f:
        f.write(f"{os.path.basename(audio_file)}:{text}\n")

    shutil.copy(audio_file, rf"output\speech\{folder_name}")
