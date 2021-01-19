import os
import sys
import time

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
    elif sys.argv[1] == 'd' and len(sys.argv) == 3:
        start_time = time.time()
        decoded_file = sys.argv[2]
        decoding = LZWDecoding(encoded_path=encoded_path)
        decoding.lzw_decompress(decoded_file)
        print(f'Decompressed to {decoded_file}')
        print(f'Before decompress:     {os.path.getsize(encoded_path)}')
        print(f'After Decompressed:  {os.path.getsize(decoded_file)}')
        print(f"--- {time.time() - start_time:.3f} seconds ---")
        print("Dekoduota per" + f"--- {time.time() - start_time:.3f} seconds ---")
    else:
        sys.exit("Invalid arguments. Format [c|d] [inputFile.*] [|outputFile.*] [k| ]")
