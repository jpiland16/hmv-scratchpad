class QuatReader:
    def get_quaternions(self):
        """Load the quaternions from the file"""
        pass

class DirectQuatReader(QuatReader):
    def __init__(self, filepath, col_offset):
        self.filepath = filepath


    def get_quaternions(self):
        """Reads the quaternions directly from the file"""
        pass 