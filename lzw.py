import os
import time
import sys

from decoder import LZWDecoding
from encoder import LZWEncoding

if __name__ == "__main__":

    if sys.argv[1] == 'c' and len(sys.argv) == 4 and int(sys.argv[3]) >= 0:
        start_time = time.time()
        encoding = LZWEncoding(path=sys.argv[2], param=int(sys.argv[3]))
        encoded_path = encoding.lzw_compress()
        print(f'Compressed to {encoded_path}')
        print(f'Before compress: {os.path.getsize(sys.argv[2])}')
        print(f'After compress:  {os.path.getsize(encoded_path)}')
        print(f"--- {time.time() - start_time:.3f} seconds ---")
    elif sys.argv[1] == 'd' and len(sys.argv) == 4:
        start_time = time.time()
        encoded_path = sys.argv[2]
        decoded_file = sys.argv[3]
        decoding = LZWDecoding()
        decoding.lzw_decompress(encoded_path, decoded_file)
        print(f'Decompressed to {decoded_file}')
        print(f'Before decompress:     {os.path.getsize(encoded_path)}')
        print(f'After Decompressed:  {os.path.getsize(decoded_file)}')
        print(f"--- {time.time() - start_time:.3f} seconds ---")
        print("Dekoduota per" + f"--- {time.time() - start_time:.3f} seconds ---")
    else:
        sys.exit("Invalid arguments. Format [c|d] [inputFile.*] [|outputFile.*] [k| ]")

    # path = 'flowers.bmp'  # file to encode
    # decoded_file = 'flowers_dec.bmp'  # file to decode
    # parameter = 9
    # encoding = LZWEncoding(path=path, param=parameter)
    # decoding = LZWDecoding(path=path, param=parameter)
    #
    # start_time = time.time()
    # encoded_path = encoding.lzw_compress()
    # print(f'Compressed to {encoded_path}')
    # print(f'Before compress: {os.path.getsize(path)}')
    # print(f'After compress:  {os.path.getsize(encoded_path)}')
    # print(f"--- {time.time() - start_time:.3f} seconds ---")
    #
    # print()
    #
    # start_time = time.time()
    # decoding.lzw_decompress(encoded_path, decoded_file)
    # print(f'Decompressed to {decoded_file}')
    # print(f'Before compress:     {os.path.getsize(path)}')
    # print(f'After Decompressed:  {os.path.getsize(decoded_file)}')
    # print(f"--- {time.time() - start_time:.3f} seconds ---")
    #
    # print()

    with open(path, 'rb') as ori_file, open(decoded_file, 'rb') as deco_file:
        text1 = ori_file.read()
        text2 = deco_file.read()
        print('Before-After:')
        print('Identical files !' if text1 == text2 else 'Not identical files!')
