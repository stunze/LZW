import os
import time

from decoder import LZWDecoding
from encoder import LZWEncoding

if __name__ == "__main__":
    path = 'flowers.bmp'  # file to encode
    decoded_file = 'flowers_dec.bmp'  # file to decode
    parameter = 9
    encoding = LZWEncoding(path=path, param=parameter)
    decoding = LZWDecoding(path=path, param=parameter)

    start_time = time.time()
    encoded_path = encoding.lzw_compress()
    print(f'Compressed to {encoded_path}')
    print(f'Before compress: {os.path.getsize(path)}')
    print(f'After compress:  {os.path.getsize(encoded_path)}')
    print(f"--- {time.time() - start_time:.3f} seconds ---")

    print()

    start_time = time.time()
    decoding.lzw_decompress(encoded_path, decoded_file)
    print(f'Decompressed to {decoded_file}')
    print(f'Before compress:     {os.path.getsize(path)}')
    print(f'After Decompressed:  {os.path.getsize(decoded_file)}')
    print(f"--- {time.time() - start_time:.3f} seconds ---")

    print()

    with open(path, 'rb') as ori_file, open(decoded_file, 'rb') as deco_file:
        text1 = ori_file.read()
        text2 = deco_file.read()
        print('Before-After:')
        print('Identical files !' if text1 == text2 else 'Not identical files!')
