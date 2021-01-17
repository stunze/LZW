import os
import commons
from encoder import ASCII_TO_INT

INT_TO_ASCII: dict = {i: b for b, i in ASCII_TO_INT.items()}  # for decoding


class BitReader(object):
    def __init__(self, f):
        self.input = f
        self.accumulator = 0
        self.bcount = 0
        self.read = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _readbit(self):
        if not self.bcount:
            a = self.input.read(1)
            if a:
                self.accumulator = ord(a)
            self.bcount = 8
            self.read = len(a)
        rv = (self.accumulator & (1 << self.bcount - 1)) >> self.bcount - 1
        self.bcount -= 1
        return rv

    def readbits(self, n):
        v = 0
        while n > 0:
            v = (v << 1) | self._readbit()
            n -= 1
        return v


class LZWDecoding:

    def __init__(self, path, param):
        """
        :param path: file path to compress
        :param param: parameter for max dictionary size
        """
        self.path = path
        self.reverse_lzw_mapping = INT_TO_ASCII.copy()  # key = dictionary length
        self.rev_keys = len(INT_TO_ASCII)
        self.param = param

    def lzw_decompress(self, input_path, output_path):
        """
        decompress input_file
        :param output_path: file decompressed saved to filename
        :param input_path: the file to decompress using lzw
        """
        module_name = os.path.splitext(os.path.basename(__file__))[0]
        bitIO = __import__(module_name)
        with open(input_path, 'rb') as file, open(output_path, 'wb') as output, bitIO.BitReader(file) as reader:
            self.param = ord(file.read(1))
            previous = -1
            decoded_text = bytearray()
            while True:

                number = commons.number_of_bits(self.rev_keys)
                key = reader.readbits(number)  # read as many bits as encoded dynamically
                if not reader.read:  # if end of file
                    break

                if self.rev_keys == 2 ** self.param:  # init dictionary
                    self.reverse_lzw_mapping = INT_TO_ASCII.copy()
                    self.rev_keys = len(INT_TO_ASCII)

                if previous == -1:  # aha kazko truksta:)
                    previous = key
                else:
                    if key != self.rev_keys:
                        word = self.reverse_lzw_mapping[previous] + self.reverse_lzw_mapping[key][0:1]
                    else:
                        word = self.reverse_lzw_mapping[previous] + self.reverse_lzw_mapping[previous][0:1]
                    self.reverse_lzw_mapping[self.rev_keys] = word
                    self.rev_keys += 1
                    previous = key
                decoded_text.extend(self.reverse_lzw_mapping[key])

            output.write(decoded_text)  # write to file
            print("LZW Decompressed")
