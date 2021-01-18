import os
import commons

ASCII_TO_INT: dict = {i.to_bytes(1, 'big'): i for i in range(256)}  # for encoding


class BitWriter(object):
    def __init__(self, f):
        self.accumulator = 0
        self.bcount = 0
        self.out = f

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()

    def __del__(self):
        try:
            self.flush()
        except ValueError:  # I/O operation on closed file.
            pass

    def _writebit(self, bit):
        if self.bcount == 8:
            self.flush()
        if bit > 0:
            self.accumulator |= 1 << 7 - self.bcount
        self.bcount += 1

    def writebits(self, bits, n):
        while n > 0:
            self._writebit(bits & 1 << n - 1)
            n -= 1

    def flush(self):
        self.out.write(bytearray([self.accumulator]))
        self.accumulator = 0
        self.bcount = 0


class LZWEncoding:
    def __init__(self, path, param):
        """
        :param path: file path to compress
        :param param: max dictionary size
        """
        self.path = path
        self.keys = ASCII_TO_INT.copy()  # key = bytes
        self.n_keys = len(ASCII_TO_INT)  # length of dictionary
        self.param = param

    def lzw_compress(self):
        """
        compress the file located in self.path using lzw.
        :return: output_path. saving the compressed data into filename + ".lzw"
        """
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".lzw"
        module_name = os.path.splitext(os.path.basename(__file__))[0]
        bitIO = __import__(module_name)
        data = commons.yield_from_file(self.path)
        word = b''
        with open(output_path, 'wb') as output, bitIO.BitWriter(output) as writer:
            writer.writebits(self.param, 8)
            for chunk in data:
                for byte in chunk:
                    new_word = word + byte.to_bytes(1, byteorder='big')

                    if self.n_keys == 2**self.param:
                        self.keys = ASCII_TO_INT.copy()  # key = bytes
                        self.n_keys = len(ASCII_TO_INT)  # length of dictionary

                    if new_word in self.keys:
                        word = new_word
                    else:
                        number_of_bits = commons.number_of_bits(self.n_keys)
                        writer.writebits(self.keys[word], number_of_bits)
                        self.keys[new_word] = self.n_keys
                        self.n_keys += 1
                        word = byte.to_bytes(1, byteorder='big')

            if word in self.keys:  # for last string
                number_of_bits = commons.number_of_bits(self.n_keys)
                writer.writebits(self.keys[word], number_of_bits)

        print("LZW Compressed")
        return output_path
