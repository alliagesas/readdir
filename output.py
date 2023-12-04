class Output:
    def __init__(self, file):
        self.file = file;

    def open(self, mode = 'a'):
        return open(self.file, mode)

    def truncate(self):
        handle = self.open()
        handle.truncate(0)
        handle.close()

    def write(self, string):
        handle = self.open()
        handle.write(string)
        handle.close()

    def writelines(self, lines):
        handle = self.open()
        handle.writelines(lines)
        handle.close()