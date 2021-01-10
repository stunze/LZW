    def lzw_decompress(self, input_path, output_path):
        """
        decompress input_file
        :param input_path: the file to decompress using lzw
        :return: output_path. file decompressed saved to filename + ".bmp"
        """
        with open(input_path, 'rb') as file, open(output_path, 'wb') as output:
            tempBuffer = bitarray()
            decoded_text = b''
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
                start_time = time.time()
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
                    decoded_text += self.reverse_lzw_mapping[key]
                    encoded_text = encoded_text[self.n_bits:]  # skip n_bits
                print(f"--- {time.time() - start_time:.3f} seconds ---")
            if key in self.keys:  # for last string
                decoded_text += self.reverse_lzw_mapping[key]
            output.write(decoded_text)  # write to file
            print("LZW Decompressed")
