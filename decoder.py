from bitarray._bitarray import bitarray

import commons
from encoder import ASCII_TO_INT

INT_TO_ASCII: dict = {i: b for b, i in ASCII_TO_INT.items()}  # for decoding


class LZWDecoding:

    def __init__(self, path, dict_max_size, n_bits):
        """
        :param path: file path to compress
        :param dict_max_size: max dictionary size
        :param n_bits: in how many bits all the codes are written
        """
        self.path = path
        self.n_bits = n_bits  # how many bits to write to file
        self.reverse_lzw_mapping = INT_TO_ASCII.copy()  # key = dictionary length
        self.rev_keys = len(INT_TO_ASCII)
        self.dict_max_size = dict_max_size

    def lzw_decompress(self, input_path, output_path):
        """
        decompress input_file
        :param output_path: file decompressed saved to filename
        :param input_path: the file to decompress using lzw
        """
        with open(input_path, 'rb') as file, open(output_path, 'wb') as output:
            tempBuffer = bitarray()
            decoded_text = bytearray()
            previous = -1
            encoded_text = ""
            padding = int.from_bytes(file.read(1), byteorder="big", signed=False)
            tempBuffer.fromfile(file, 1)
            del tempBuffer[:padding]
            scanned_bytes = commons.yield_bytes_from_stream(file)
            for chunk in scanned_bytes:
                tempBuffer.frombytes(chunk)
                encoded_text += tempBuffer.to01()
                del tempBuffer[:]
                while len(encoded_text) >= self.n_bits:
                    code = encoded_text[0:self.n_bits]  # reading n_bits at the time
                    key = int(code, 2)  # convert to code
                    if previous == -1:
                        previous = int(code, 2)
                    elif self.rev_keys != self.dict_max_size:
                        if key != self.rev_keys:
                            word = self.reverse_lzw_mapping[previous] + self.reverse_lzw_mapping[key][0:1]
                        else:
                            word = self.reverse_lzw_mapping[previous] + self.reverse_lzw_mapping[previous][0:1]
                        self.reverse_lzw_mapping[self.rev_keys] = word
                        self.rev_keys += 1
                        previous = key
                    decoded_text.extend(self.reverse_lzw_mapping[key])
                    encoded_text = encoded_text[self.n_bits:]  # skip n_bits
            output.write(decoded_text)  # write to file
            print("LZW Decompressed")
