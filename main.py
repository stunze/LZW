MAX_DICT_SIZE = 4096

def init_dictionary():
    return {format(i, "08b"): i for i in range(256)}


def check_dictionary(dictionary: dict, element: str):  # reik nepamirst daugiau checku uzdet
    if len(dictionary) < MAX_DICT_SIZE:
        return True


def bytes_from_file(filename):
    with open(filename, "rb") as input_stream:
        while True:
            byte = input_stream.read(1)
            if not byte:
                break
            yield byte


def find_in_dictionary(dictionary: dict, key):
    for k, v in dictionary.items():
        if k == key:
            return v


def encoded_to_file(filename: str, encoded):
    with open(filename,'wb') as output_stream:
        output_stream.write(encoded)


def encoder(filename_in: str, filename_out: str):
    dictionary = init_dictionary()
    code = ""
    encoded = bytearray()

    for byte in bytes_from_file(filename_in):
        # if not (check_dictionary(dictionary, code)):
        #     break
        if len(code) < 1:
            code += '{:08b}'.format(ord(byte))
        elif code in dictionary.keys():
            value = find_in_dictionary(dictionary, code)
            code += '{:08b}'.format(ord(byte))
        else:
            encoded += value.to_bytes(2, byteorder='big')
            dictionary.update({code: len(dictionary)})
            code = ""
    print(encoded)
    encoded_to_file(filename_out, encoded)

def read_from_file(filename: str):
    # perskaitom abeceles dydi
    try:
        with open(filename, mode='rb') as input_stream:  # reading characters from file

            entryNum = int.from_bytes(input_stream.read(1), "big")
            entryList = []
            for byte in input_stream.read(2**entryNum):
                entryList.append(int.from_bytes(byte, "big"))

            return entryList

    except OSError:
        print("Failas nerastas.")


def write_to_file(outputFile: str, text: str):
    try:
        with open(outputFile, "wb") as output_stream:
            output_stream.write(text)
        return True
    except OSError:
        print("Failas nerastas")
    return False


def decode(alphabet: dict, entryList: list) -> str:
    text = ""
    newWord = ""
    previousEntry = -1

    for entry in entryList:

        # print(text)
        if previousEntry > -1:
            if entry != len(alphabet):
                newWord += alphabet[previousEntry] + alphabet[entry][0]
            else:
                newWord += alphabet[previousEntry] + alphabet[previousEntry][0]
            # print(newWord)
            alphabet.update({len(alphabet): newWord})
            # print(alphabet)
            newWord = ""

        text += alphabet[entry]
        previousEntry = entry

    return text


def build_table() -> dict:
    alphabet = {}
    for i in range(0, 256):
        alphabet.update({i: chr(i)})

    return alphabet


def decoder(comprfile: str):
    # entryList = read_from_file(comprfile)
    entryList = [97, 98, 98, 256, 259, 99]
    alphabet = build_table()
    decode(alphabet, entryList)


if __name__ == '__main__':
    decoder("mhm.txt")
