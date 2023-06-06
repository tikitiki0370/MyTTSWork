import sys
import os

def volume_normalize(file_path, volume=2):
    path = ""
    file_ls =  file_path.split("\\")
    path = ".\\output\\volume_normalize\\" + file_ls[file_ls.index("raw")+1]
    # path = ".\\output\\volume_normalize\\" + "temp"
    os.makedirs(f"{path}", exist_ok=True)
    file_out  = f"{path}\{os.path.basename(file_path)}"
    os.system(f"ffmpeg -y -i {file_path} -af volume={volume}dB {file_out}")