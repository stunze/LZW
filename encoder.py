import os
import commons

ASCII_TO_INT: dict = {i.to_bytes(1, 'big'): i for i in range(256)}  # for encoding


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
        print(self.param)
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".lzw"
        with open(self.path, 'rb') as file, open(output_path, 'wb') as output:
            data = file.read()
            compressed: list = []
            string = b''
            for symbol in data:
                string_plus_symbol = string + symbol.to_bytes(1, 'big')  # get input symbol and add to previous string
                if self.n_keys == 2**self.param:
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
            bits: str = ''.join([bin(i)[2:].zfill(self.param) for i in compressed])  # to bits
            padded_text = commons.pad_encoded_text(encoded_text=bits)  # add padding for decoding in bytes
            b = commons.get_byte_array(padded_encoded_text=padded_text)  # padding size and encoded text
            output.write(b)
        print("LZW Compressed")
        return output_path
