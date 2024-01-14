class File_C():
    def __init__(self):
        self.file_name = ""

    def w_mode(self, filename, value, encodingf='utf-8'):
        try:
            with open(filename, 'w', encoding=encodingf) as f:
                return eval(f"f.write({value})")

        except:
            return "FATAL ERROR filewere construction or library construction"

    def r_mode(self, filename, encodingf='utf-8'):
        try:
            with open(filename, 'r', encoding=encodingf) as f:
                return eval(f"f.read()")

        except:
            return "FATAL ERROR filewere construction or library construction"

    def do_mode(self, filename, modeOpen='r', modeCommand='read', value='', encodingf='utf-8'):
        try:
            with open(filename, modeOpen, encoding=encodingf) as f:
                if value == '':
                    return eval(f"f.{modeCommand}()")
                else:
                    return eval(f"f.{modeCommand}('{value}')")

        except:
            return "FATAL ERROR filewere construction or library construction"