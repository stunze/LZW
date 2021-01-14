import os
import time

from decoder import LZWDecoding
from encoder import LZWEncoding

if __name__ == "__main__":
    path = 'flowers.bmp'  # file to encode
    decoded_file = 'flowers_dec.bmp'  # file to decode
    parameter = 9
    encoding = LZWEncoding(path=path, param=parameter)
    decoding = LZWDecoding(path=path, param=parameter)  # n_bits temporary

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
