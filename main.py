import os
import time

ASCII_TO_INT: dict = {i.to_bytes(1, 'big'): i for i in range(256)}  # for encoding
INT_TO_ASCII: dict = {i: b for b, i in ASCII_TO_INT.items()}  # for decoding


def pad_encoded_text(encoded_text):
    """
    padding the encoded text to bytes. if bit string is 14 we need 2 bits padding
    :param encoded_text: the encoded text without padding
    :return: padded encoded text
    """
    padding = 8 - len(encoded_text) % 8
    for i in range(padding):
        encoded_text += "0"

    padded_info = "{0:08b}".format(padding)
    encoded_text = padded_info + encoded_text
    return encoded_text


def remove_padding(padded_encoded_text):
    """
    removing the extra padded bits from encoded_text
    :param padded_encoded_text: encoded string in bits
    :return: encoded text without padding
    """
    padded_text = padded_encoded_text[:8]
    padding = int(padded_text, 2)

    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1 * padding]

    return encoded_text


def get_byte_array(padded_encoded_text):
    """
    creating bytes array from bits string
    :param padded_encoded_text: string of bits
    :return: bytearray()
    """
    if len(padded_encoded_text) % 8 != 0:
        print("Encoded text not padded properly")
        exit(0)

    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i + 8]
        b.append(int(byte, 2))
    return b


class LZW_Coding:
    def __init__(self, path):
        """
        :param path: file path to compress
        """
        self.path = path
        self.n_bits = None  # how many bits to write to file
        self.keys = ASCII_TO_INT.copy()  # key = bytes
        self.reverse_lzw_mapping = INT_TO_ASCII.copy()  # key = dictionary length
        self.n_keys = len(ASCII_TO_INT)  # length of dictionary
        self.rev_keys = len(INT_TO_ASCII)

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
            padded_text = pad_encoded_text(encoded_text=bits)  # add padding for decoding in bytes
            b = get_byte_array(padded_encoded_text=padded_text)  # padding size and encoded text
            output.write(b)
        print("LZW Compressed")
        return output_path

    def lzw_decompress(self, input_path, output_path):
        """
        decompress input_file
        :param input_path: the file to decompress using lzw
        :return: output_path. file decompressed saved to filename + "_decompressed" + ".bmp"
        """

        with open(input_path, 'rb') as file, open(output_path, 'wb') as output:
            bit_string_list = []

            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string_list.append(bits)  # bytes and converting to bit string
                byte = file.read(1)

            padded_encoded_text = ''.join(bit_string_list)  # list with padding

            encoded_text = remove_padding(padded_encoded_text)  # without

            decoded_text = b''
            word = b''
            previous = -1
            start = 0
            while start < len(encoded_text):
                code = encoded_text[start:start + self.n_bits]  # reading n_bits at the time
                key = int(code, 2)  # convert to code
                if previous > -1:
                    if key != self.rev_keys:
                        word += self.reverse_lzw_mapping[previous] + self.reverse_lzw_mapping[key][0:8]
                    else:
                        word += self.reverse_lzw_mapping[previous] + self.reverse_lzw_mapping[previous][0:8]
                    self.reverse_lzw_mapping[self.rev_keys] = word
                    self.rev_keys += 1
                previous = key
                decoded_text += self.reverse_lzw_mapping[key]
                word = b''
                start += self.n_bits  # skip n_bits
            print(self.n_keys)
            print(self.rev_keys)
            output.write(decoded_text)  # write to file
            print("LZW Decompressed")
            return output_path


path = 'img.jpg'  # file to encode
decoded_file = 'img_dec.jpg'  # file to decode

lzw = LZW_Coding(path=path)

start_time = time.time()
encoded_path = lzw.lzw_compress()
print(f'Compressed to {encoded_path}')
print(f'Before compress: {os.path.getsize(path)}')
print(f'After compress:  {os.path.getsize(encoded_path)}')
print(f"--- {time.time() - start_time:.3f} seconds ---")

print()

start_time = time.time()
output_path = lzw.lzw_decompress(encoded_path, decoded_file)  # blogas
print(f'Decompressed to {decoded_file}')
print(f'Before compress:     {os.path.getsize(path)}')
print(f'After Decompressed:  {os.path.getsize(decoded_file)}')
print(f"--- {time.time() - start_time:.3f} seconds ---")
