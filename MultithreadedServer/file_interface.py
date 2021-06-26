import os
import base64
from glob import glob

class FileInterface:
    def __init__(self):
        os.chdir('Files/')

    def list(self):
        try:
            fileList = glob('*.*')
            return dict(status='OK', data=fileList)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, filename=''):
        if filename == '':
            return None

        try:
            fp = open(f"{filename}", 'rb')
            name_arr = filename.split(".")
            nameonly = name_arr[0]
            ext = name_arr[1]
            content = base64.b64encode(fp.read()).decode()
            return dict(status='OK', data_namafile=filename, data_file=content, data_nama=nameonly, data_ext=ext)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

if __name__ == '__main__':
    f = FileInterface()
    print(f.list())
    print(f.get('pokijan.jpg'))