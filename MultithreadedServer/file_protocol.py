import json
import logging
from file_interface import FileInterface

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def processString(self, string_datamasuk=''):
        logging.warning(f"String processed: {string_datamasuk}")
        c = string_datamasuk.split(" ")

        try:
            c_request = c[0].strip()
            logging.warning(f"Processing request: {c_request}")

            if c_request == 'LIST':
                return json.dumps(self.file.list())
            elif c_request == 'GET':
                param1 = c[1].strip()
                return json.dumps(self.file.get(param1))
            else:
                return json.dumps(dict(status='ERROR', data='Request is not recognized'))
        except Exception:
            return json.dumps(dict(status='ERROR', data='Request is not recognized'))


if __name__ == '__main__':
    fp = FileProtocol()
    print(fp.processString("LIST"))
    print(fp.processString("GET pokijan.jpg"))