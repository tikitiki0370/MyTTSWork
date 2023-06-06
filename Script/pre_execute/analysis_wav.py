import glob
import os
import wave
from concurrent.futures import ProcessPoolExecutor
from struct import unpack

import matplotlib.pyplot as plt
import numpy as np
import volume_normalize as vn
from inaSpeechSegmenter import Segmenter


class AnalysisWav:

    def __init__(self, file_path):
        self.file_path = file_path
        self.seg_model = Segmenter(vad_engine="smn")
        self.__filereader()

    def __filereader(self):
        wf = wave.open(self.file_path, 'rb')
        self.getnframes = wf.getnframes()
        self.readframes = wf.readframes(self.getnframes)
        self.getframerate = wf.getframerate()
        self.getsampwidth = wf.getsampwidth()
        wf.close()

    def analysis_label(self):
        with open(f"{self.__mkdir('raw_label')}.txt", "w") as f:
            for i in self.seg_model(self.file_path):
                f.write(f"{i[0]} {i[1]} {i[2]}\n")


    def analysis_volume(self) -> int:
        return

    def gen_waveimg(self):
        if self.getsampwidth == 2:
            data = np.frombuffer(self.readframes, dtype='int16')
        elif self.getsampwidth == 3:
            self.readframes = [unpack("<i",
                                      bytearray([0]) + self.readframes[self.getsampwidth * i:self.getsampwidth * (i + 1)])[0]
                               for i in range(self.getnframes)]
            data = np.array(self.readframes)
            data = np.where(data > 0,
                            data / (2.0 ** 31 - 1),
                            data / (2.0 ** 31))
        t = np.arange(0, len(data)) / self.getframerate
        plt.plot(t, data)
        plt.grid()
        plt.savefig(f"{self.__mkdir('raw_img')}.png")
        plt.close()

    def __mkdir(self, name):
        path = ""
        file_ls = self.file_path.split("\\")
        path = f".\\output\\{name}\\" + file_ls[file_ls.index("raw")+1]
        os.makedirs(f"{path}", exist_ok=True)
        return f"{path}\{os.path.splitext(os.path.basename(self.file_path))[0]}"


def extract(file_path):
    vn.volume_normalize(file_path, -1)
    # analysis_wav = AnalysisWav(file_path=f"{file_path}")
    # analysis_wav.gen_waveimg()
    # print(analysis_wav.analysis_label())


if __name__ == '__main__':
    files = glob.glob(
        r"data\raw\2023_02_19\main\*.wav", recursive=True)
        # r"data\temp\*.wav", recursive=True)
    with ProcessPoolExecutor(max_workers=4) as executor:
        for file_path in files:
            executor.submit(extract, file_path)

