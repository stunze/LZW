import os
import time
from bitarray._bitarray import bitarray
import commons

ASCII_TO_INT: dict = {i.to_bytes(1, 'big'): i for i in range(256)}  # for encoding
INT_TO_ASCII: dict = {i: b for b, i in ASCII_TO_INT.items()}  # for decoding


class LZW_Coding:
    def __init__(self, path, dict_max_size):
        """
        :param path: file path to compress
        :param dict_max_size: max dictionary size
        """
        self.path = path
        self.n_bits = None  # how many bits to write to file
        self.keys = ASCII_TO_INT.copy()  # key = bytes
        self.reverse_lzw_mapping = INT_TO_ASCII.copy()  # key = dictionary length
        self.n_keys = len(ASCII_TO_INT)  # length of dictionary
        self.rev_keys = len(INT_TO_ASCII)
        self.dict_max_size = dict_max_size

    def lzw_compress(self):
        """
                compress the file located in self.path using lzw.
                :return: output_path. saving the compressed data into filename + ".lzw"
                """

        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".lzw"
        with open(self.path, 'rb') as file, open(output_path, 'wb') as output:
            data = file.read()

            compressed: list = []
            string = b''
            for symbol in data:
                string_plus_symbol = string + symbol.to_bytes(1, 'big')  # get input symbol and add to previous string
                if self.n_keys == self.dict_max_size:
                    if string_plus_symbol in self.keys:  # if we already have new string of bytes
                        string = string_plus_symbol  # update string
                    else:
                        compressed.append(self.keys[string])  # to compressed list add key[string]
                        string = symbol.to_bytes(1, 'big')  # new string in bytes
                else:
                    if string_plus_symbol in self.keys:  # if we already have new string of bytes
                        string = string_plus_symbol  # update string
                    else:
                        compressed.append(self.keys[string])  # to compressed list add key[string]
                        self.keys[string_plus_symbol] = self.n_keys  # update dictionary key[new_string]
                        self.n_keys += 1  # update dictionary size
                        string = symbol.to_bytes(1, 'big')  # new string in bytes
            if string in self.keys:  # for last string
                compressed.append(self.keys[string])
            self.n_bits = len(bin(self.n_keys)[2:])  # how many bits to write to file for one symbol
            bits: str = ''.join([bin(i)[2:].zfill(self.n_bits) for i in compressed])  # to bits
            print(len(bits))
            padded_text = commons.pad_encoded_text(encoded_text=bits)  # add padding for decoding in bytes
            b = commons.get_byte_array(padded_encoded_text=padded_text)  # padding size and encoded text
            output.write(b)
        print("LZW Compressed")
        return output_path

    def lzw_decompress(self, input_path, output_path):
        """
        decompress input_file
        :param input_path: the file to decompress using lzw
        :return: output_path. file decompressed saved to filename + ".bmp"
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


path = 'big_bmp.bmp'  # file to encode
decoded_file = 'big_bmp_dec.bmp'  # file to decode
dict_max_size = 1024
lzw = LZW_Coding(path=path, dict_max_size=dict_max_size)

start_time = time.time()
encoded_path = lzw.lzw_compress()
print(f'Compressed to {encoded_path}')
print(f'Before compress: {os.path.getsize(path)}')
print(f'After compress:  {os.path.getsize(encoded_path)}')
print(f"--- {time.time() - start_time:.3f} seconds ---")

print()

start_time = time.time()
lzw.lzw_decompress(encoded_path, decoded_file)  # blogas
print(f'Decompressed to {decoded_file}')
print(f'Before compress:     {os.path.getsize(path)}')
print(f'After Decompressed:  {os.path.getsize(decoded_file)}')
print(f"--- {time.time() - start_time:.3f} seconds ---")
