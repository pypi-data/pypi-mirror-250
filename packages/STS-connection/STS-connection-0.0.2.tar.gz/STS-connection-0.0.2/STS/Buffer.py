class CircularBuffer:
    def __init__(self, max_size):
        self.buffer = bytearray(max_size)
        self.start = 0
        self.end = 0
        self.size = 0
        self.max_size = max_size

    def append(self, data):
        data_len = len(data)
        if data_len > self.max_size:
            raise ValueError("Data size exceeds buffer size")

        if self.size + data_len > self.max_size:
            self.start = (self.start + data_len) % self.max_size
            self.size = self.max_size

        if self.end + data_len > self.max_size:
            overlap = (self.end + data_len) - self.max_size
            self.buffer[self.end:] = data[:data_len - overlap]
            self.buffer[:overlap] = data[data_len - overlap:]
            self.end = overlap
        else:
            self.buffer[self.end:self.end + data_len] = data
            self.end = (self.end + data_len) % self.max_size

        self.size += data_len

    def get_contents(self):
        if self.size == 0:
            return bytes()

        if self.start < self.end:
            return bytes(self.buffer[self.start:self.end])
        else:
            return bytes(self.buffer[self.start:] + self.buffer[:self.end])

    def find(self, string):
        search_len = len(string)
        if search_len > self.size:
            return False

        if self.start <= self.end:
            content = self.buffer[self.start:self.end]
        else:
            content = self.buffer[self.start:] + self.buffer[:self.end]

        if string in content.decode('utf-8', errors='ignore'):
            return True

        return False

    def clear(self):
        self.start = 0
        self.end = 0
        self.size = 0
